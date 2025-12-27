#!/usr/bin/env python3
"""
Automated Monster Generator - Complete automated generation workflow integrated with ComfyUI
"""

import sys
from pathlib import Path

# Add config directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "config"))

import json
import websockets
import uuid
import urllib.request
import urllib.parse
import requests
import logging
import os
import time
import threading
import datetime
import copy
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutomatedMonsterGenerator:
    """Automated monster image generator"""
    
    def __init__(self, comfyui_url: str = "http://127.0.0.1:8188", workspace_dir: str = None):
        self.comfyui_url = comfyui_url
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path(__file__).parent.parent
        
        # Directory configuration
        try:
            # Add config directory to path
            config_path = str(self.workspace_dir / "config")
            if config_path not in sys.path:
                sys.path.insert(0, config_path)
            
            from settings import WORKFLOWS_OUTPUT_DIR, GENERATED_IMAGES_DIR
            self.workflows_output_dir = WORKFLOWS_OUTPUT_DIR
            self.input_images_dir = self.workflows_output_dir / "input_images"
            self.generated_images_dir = GENERATED_IMAGES_DIR
        except ImportError:
            self.workflows_output_dir = self.workspace_dir / "outputs" / "workflows"
            self.input_images_dir = self.workflows_output_dir / "input_images"
            self.generated_images_dir = self.workspace_dir / "outputs" / "generated_outputs" / "final_images"
        
        # Create output directory
        self.generated_images_dir.mkdir(parents=True, exist_ok=True)
        
        # Work status
        self.ws = None
        self.is_connected = False
        
    def check_comfyui_server(self) -> bool:
        """Check if ComfyUI server is running"""
        try:
            response = requests.get(f"{self.comfyui_url}/system_stats", timeout=5)
            if response.status_code == 200:
                logging.info("ComfyUI server connection successful")
                return True
        except Exception:
            pass
        return False
    
    def setup_websocket(self):
        """Setup WebSocket connection to monitor generation progress"""
        import websocket
        
        def on_open(ws):
            self.is_connected = True
        
        def on_close(ws, close_status_code, close_msg):
            self.is_connected = False
        
        def on_message(ws, message):
            pass  # Simplified message handling
        
        def on_error(ws, error):
            pass  # Simplified error handling
        
        ws_url = self.comfyui_url.replace("http://", "ws://") + "/ws"
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        
        def run_ws():
            self.ws.run_forever()
        
        ws_thread = threading.Thread(target=run_ws, daemon=True)
        ws_thread.start()
        
        # Wait for connection to establish
        for _ in range(10):
            if self.is_connected:
                break
            time.sleep(0.5)
    
    def upload_images_to_comfyui(self) -> bool:
        """Upload images to ComfyUI server"""
        try:
            upload_url = f"{self.comfyui_url}/upload/image"
            uploaded_count = 0
            
            for image_file in self.input_images_dir.glob("*"):
                if image_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                    with open(image_file, 'rb') as f:
                        files = {'image': (image_file.name, f, 'image/png')}
                        response = requests.post(upload_url, files=files)
                        if response.status_code == 200:
                            uploaded_count += 1
            
            logging.info(f"Successfully uploaded {uploaded_count} image files")
            return uploaded_count > 0
        except Exception:
            return False
    
    def convert_workflow_for_api(self, workflow):
        """Convert workflow format to ComfyUI API format"""
        api_workflow = {}
        
        if not workflow or "nodes" not in workflow:
            return {}
        
        unsupported_nodes = {"Note", "Reroute"}
        
        for node in workflow.get("nodes", []):
            node_id = str(node.get("id"))
            node_type = node.get("type")
            
            if not node_type or node_type in unsupported_nodes:
                continue
                
            api_node = {
                "class_type": node_type,
                "inputs": {}
            }
            
            # Process input connections
            inputs = node.get("inputs", [])
            if inputs:
                for input_info in inputs:
                    if not input_info:
                        continue
                    input_name = input_info.get("name")
                    link_id = input_info.get("link")
                    
                    if link_id and input_name:
                        source_node_id, output_index = self.find_link_source(workflow, link_id)
                        if source_node_id is not None:
                            api_node["inputs"][input_name] = [str(source_node_id), output_index]
            
            # Process widget values
            widget_values = node.get("widgets_values", [])
            if widget_values:
                if node_type == "LoadImage" and len(widget_values) >= 1:
                    api_node["inputs"]["image"] = widget_values[0]
                elif node_type == "CLIPTextEncode" and len(widget_values) >= 1:
                    api_node["inputs"]["text"] = widget_values[0]
                elif node_type == "KSampler":
                    if len(widget_values) >= 7:
                        api_node["inputs"]["seed"] = int(widget_values[0]) if str(widget_values[0]).replace('.','').isdigit() else 123456
                        api_node["inputs"]["control_after_generate"] = str(widget_values[1]) if len(widget_values) > 1 else "fixed"
                        api_node["inputs"]["steps"] = int(widget_values[2]) if len(widget_values) > 2 and str(widget_values[2]).replace('.','').isdigit() else 20
                        api_node["inputs"]["cfg"] = float(widget_values[3]) if len(widget_values) > 3 and isinstance(widget_values[3], (int, float)) else 8.0
                        api_node["inputs"]["sampler_name"] = str(widget_values[4]) if len(widget_values) > 4 else "euler"
                        api_node["inputs"]["scheduler"] = str(widget_values[5]) if len(widget_values) > 5 else "normal"
                        api_node["inputs"]["denoise"] = float(widget_values[6]) if len(widget_values) > 6 and isinstance(widget_values[6], (int, float)) else 1.0
                elif node_type == "EmptyLatentImage":
                    if len(widget_values) >= 3:
                        api_node["inputs"]["width"] = int(widget_values[0]) if isinstance(widget_values[0], (int, float)) else 512
                        api_node["inputs"]["height"] = int(widget_values[1]) if isinstance(widget_values[1], (int, float)) else 512
                        api_node["inputs"]["batch_size"] = int(widget_values[2]) if isinstance(widget_values[2], (int, float)) else 1
                elif node_type == "Canny":
                    if len(widget_values) >= 2:
                        api_node["inputs"]["low_threshold"] = float(widget_values[0]) if isinstance(widget_values[0], (int, float)) else 0.4
                        api_node["inputs"]["high_threshold"] = float(widget_values[1]) if isinstance(widget_values[1], (int, float)) else 0.8
                elif node_type == "SaveImage" and len(widget_values) >= 1:
                    api_node["inputs"]["filename_prefix"] = widget_values[0]
                elif node_type == "IPAdapterAdvanced" and len(widget_values) >= 1:
                    api_node["inputs"]["weight"] = float(widget_values[0]) if isinstance(widget_values[0], (int, float)) else 1.0
                    api_node["inputs"]["weight_type"] = str(widget_values[1]) if len(widget_values) > 1 else "original"
                    api_node["inputs"]["combine_embeds"] = str(widget_values[2]) if len(widget_values) > 2 else "concat"
                    api_node["inputs"]["start_at"] = float(widget_values[3]) if len(widget_values) > 3 and isinstance(widget_values[3], (int, float)) else 0.0
                    api_node["inputs"]["end_at"] = float(widget_values[4]) if len(widget_values) > 4 and isinstance(widget_values[4], (int, float)) else 1.0
                    api_node["inputs"]["embeds_scaling"] = str(widget_values[5]) if len(widget_values[5]) > 0 else "V only"
                elif node_type == "ControlNetApply" and len(widget_values) >= 1:
                    api_node["inputs"]["strength"] = float(widget_values[0]) if isinstance(widget_values[0], (int, float)) else 1.0
            
            api_workflow[node_id] = api_node
        
        return api_workflow
    
    def find_link_source(self, workflow, link_id):
        """Find link source node and output index"""
        if not workflow or "nodes" not in workflow:
            return None, 0
            
        for node in workflow.get("nodes", []):
            if not node:
                continue
            outputs = node.get("outputs", [])
            if not outputs:
                continue
                
            for output_idx, output_info in enumerate(outputs):
                if not output_info:
                    continue
                links = output_info.get("links", [])
                if links and link_id in links:
                    return node.get("id"), output_idx
        return None, 0
    
    def submit_workflow_api(self, api_workflow):
        """Submit API format workflow to ComfyUI"""
        try:
            client_id = str(uuid.uuid4())
            prompt_data = {
                "prompt": api_workflow,
                "client_id": client_id
            }
            
            response = requests.post(f"{self.comfyui_url}/prompt", json=prompt_data)
            if response.status_code == 200:
                result = response.json()
                return result.get("prompt_id")
        except Exception:
            pass
        return None
    
    def wait_for_completion(self, prompt_id, timeout=300):
        """Wait for workflow completion"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.comfyui_url}/history/{prompt_id}")
                if response.status_code == 200:
                    history = response.json()
                    if prompt_id in history:
                        prompt_info = history[prompt_id]
                        if prompt_info.get("status", {}).get("completed", False):
                            return True
                        elif "error" in prompt_info.get("status", {}):
                            return False
                
                time.sleep(2)
            except Exception:
                time.sleep(2)
        
        return False
    
    def download_generated_image(self, prompt_id, combination_key):
        """Download generated image"""
        try:
            response = requests.get(f"{self.comfyui_url}/history/{prompt_id}")
            if response.status_code != 200:
                return False
            
            history = response.json()
            if prompt_id not in history:
                return False
            
            outputs = history[prompt_id].get("outputs", {})
            if not outputs:
                return False
            
            for node_id, node_output in outputs.items():
                if "images" in node_output:
                    for image_info in node_output["images"]:
                        filename = image_info.get("filename")
                        if filename:
                            image_url = f"{self.comfyui_url}/view?filename={filename}"
                            img_response = requests.get(image_url)
                            if img_response.status_code == 200:
                                output_filename = f"monster_{combination_key}.png"
                                output_path = self.generated_images_dir / output_filename
                                with open(output_path, 'wb') as f:
                                    f.write(img_response.content)
                                return True
            
            return False
        except Exception:
            return False
    
    def get_enhanced_prompt_for_combination(self, combination_key):
        """Get enhanced prompt for specified combination"""
        try:
            # Add config directory to path if not already done
            config_path = str(self.workspace_dir / "config")
            if config_path not in sys.path:
                sys.path.insert(0, config_path)
            
            from settings import FUSED_PROMPTS_OUTPUT
            
            if FUSED_PROMPTS_OUTPUT.exists():
                with open(FUSED_PROMPTS_OUTPUT, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "prompts" in data and "negative_prompts" in data:
                    prompts = data["prompts"]
                    negative_prompts = data["negative_prompts"]
                    
                    if combination_key in prompts and combination_key in negative_prompts:
                        return {
                            "prompt": prompts[combination_key],
                            "negative_prompt": negative_prompts[combination_key]
                        }
                elif combination_key in data:
                    prompt_data = data[combination_key]
                    return {
                        "prompt": prompt_data.get("prompt", ""),
                        "negative_prompt": prompt_data.get("negative_prompt", "")
                    }
                    
        except Exception:
            pass
        
        # Default prompts
        return {
            "prompt": "monster, creature, fantasy beast, digital art, highly detailed, professional",
            "negative_prompt": "blurry, low quality, deformed, mutated, extra limbs, bad anatomy, worst quality"
        }
    
    def modify_workflow_prompts(self, workflow, prompt_info):
        """Modify prompts in workflow"""
        try:
            modified_workflow = copy.deepcopy(workflow)
            
            for node in modified_workflow.get("nodes", []):
                node_type = node.get("type")
                widget_values = node.get("widgets_values", [])
                
                if node_type == "CLIPTextEncode" and len(widget_values) > 0:
                    current_text = str(widget_values[0]).lower()
                    
                    if any(neg_word in current_text for neg_word in ["blurry", "deformed", "bad", "low quality", "worst"]):
                        widget_values[0] = prompt_info["negative_prompt"]
                    else:
                        widget_values[0] = prompt_info["prompt"]
            
            return modified_workflow
        except Exception:
            return None
    
    def generate_single_combination(self, workflow_file, use_enhanced_prompts=True):
        """Generate image for single combination"""
        try:
            combination_key = workflow_file.stem.replace("workflow_", "")
            
            with open(workflow_file, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
            
            if not workflow:
                return False
            
            prompt_info = self.get_enhanced_prompt_for_combination(combination_key)
            
            modified_workflow = self.modify_workflow_prompts(workflow, prompt_info)
            if not modified_workflow:
                return False
            
            api_workflow = self.convert_workflow_for_api(modified_workflow)
            if not api_workflow:
                return False
            
            prompt_id = self.submit_workflow_api(api_workflow)
            if not prompt_id:
                return False
            
            if not self.wait_for_completion(prompt_id):
                return False
            
            return self.download_generated_image(prompt_id, combination_key)
            
        except Exception:
            return False
    
    def generate_all_combinations(self, limit=None, start_from=None):
        """Generate images for all combinations"""
        if not self.check_comfyui_server():
            return {}
        
        self.setup_websocket()
        
        if not self.upload_images_to_comfyui():
            return {}
        
        workflow_files = list(self.workflows_output_dir.glob("workflow_*.json"))
        workflow_files.sort()
        
        if start_from:
            start_idx = 0
            for i, wf in enumerate(workflow_files):
                if start_from in wf.name:
                    start_idx = i
                    break
            workflow_files = workflow_files[start_idx:]
        
        if limit:
            workflow_files = workflow_files[:limit]
        
        total_files = len(workflow_files)
        results = {}
        
        logging.info(f"Starting generation of {total_files} combination images...")
        
        for i, workflow_file in enumerate(workflow_files):
            combination_key = workflow_file.stem.replace("workflow_", "")
            
            # Check if already exists
            output_filename = f"monster_{combination_key}.png"
            output_path = self.generated_images_dir / output_filename
            if output_path.exists():
                results[combination_key] = True
                continue
            
            logging.info(f"Processing progress: {i+1}/{total_files} - {combination_key}")
            
            success = self.generate_single_combination(workflow_file)
            results[combination_key] = success
            
            if success:
                logging.info(f"✅ Successfully generated: {combination_key}")
            
            time.sleep(1)
        
        successful = sum(1 for success in results.values() if success)
        logging.info(f"Generation completed: success {successful}/{total_files}")
        
        return results
    
    def test_single_combination(self, combination_key):
        """Test single combination"""
        workflow_file = self.workflows_output_dir / f"workflow_{combination_key}.json"
        if not workflow_file.exists():
            return False
        
        if not self.check_comfyui_server():
            return False
        
        self.setup_websocket()
        
        if not self.upload_images_to_comfyui():
            return False
        
        return self.generate_single_combination(workflow_file)

def main():
    """Main function"""
    import sys
    
    # Get workspace directory
    current_dir = Path(__file__).parent
    workspace_dir = current_dir.parent
    
    # Create generator
    generator = AutomatedMonsterGenerator(workspace_dir=workspace_dir)
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test" and len(sys.argv) > 2:
            # Test single combination
            combination_key = sys.argv[2]
            logging.info(f"Testing single combination: {combination_key}")
            success = generator.test_single_combination(combination_key)
            if success:
                print(f"✅ Test successful: {combination_key}")
            else:
                print(f"❌ Test failed: {combination_key}")
        elif sys.argv[1] == "--test-enhanced" and len(sys.argv) > 2:
            # Test single combination with enhanced prompts
            combination_key = sys.argv[2]
            logging.info(f"Testing single combination (enhanced prompts): {combination_key}")
            
            # Find corresponding workflow file
            workflow_file = generator.workflows_output_dir / f"workflow_{combination_key}.json"
            if not workflow_file.exists():
                print(f"❌ Workflow file does not exist: {workflow_file}")
                return
            
            # Generate with enhanced prompts
            success = generator.generate_single_combination(workflow_file, use_enhanced_prompts=True)
            if success:
                print(f"✅ Enhanced prompt test successful: {combination_key}")
            else:
                print(f"❌ Enhanced prompt test failed: {combination_key}")
        elif sys.argv[1] == "--limit" and len(sys.argv) > 2:
            # Limit generation count
            try:
                limit = int(sys.argv[2])
                logging.info(f"Limiting generation to {limit} images")
                results = generator.generate_all_combinations(limit=limit)
                success_count = sum(1 for success in results.values() if success)
                print(f"✅ Successfully generated {success_count}/{len(results)} images")
            except ValueError:
                print("❌ Invalid limit count")
        elif sys.argv[1] == "--from" and len(sys.argv) > 2:
            # Start from specified combination
            start_key = sys.argv[2]
            logging.info(f"Starting generation from combination {start_key}")
            results = generator.generate_all_combinations(start_from=start_key)
            success_count = sum(1 for success in results.values() if success)
            print(f"✅ Successfully generated {success_count}/{len(results)} images")
        else:
            print("Usage:")
            print("  python automated_monster_generator.py                        # Generate all combinations")
            print("  python automated_monster_generator.py --test 1_1             # Test single combination")
            print("  python automated_monster_generator.py --test-enhanced 1_1    # Test enhanced prompts")
            print("  python automated_monster_generator.py --limit 10             # Limit generation to 10")
            print("  python automated_monster_generator.py --from 5_1             # Start from 5_1")
    else:
        # Generate all combinations
        results = generator.generate_all_combinations()
        
        # Print final statistics
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        print(f"\n🎯 Final result: success {successful}/{total} combinations")
        
        if successful < total:
            failed_combinations = [key for key, success in results.items() if not success]
            print("❌ Failed combinations:")
            for combo in failed_combinations[:10]:  # Only show first 10
                print(f"  - {combo}")
            if len(failed_combinations) > 10:
                print(f"  ... and {len(failed_combinations) - 10} more")

if __name__ == "__main__":
    main() 