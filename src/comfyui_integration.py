"""
ComfyUI Integration Module - Integrate with ComfyUI API for automatic image generation
"""

import sys
from pathlib import Path

# Add config directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "config"))

import json
import os
import logging
import shutil
import random
import copy

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ComfyUIIntegrator:
    """ComfyUI integrator that applies user features to image generation workflows"""
    
    def __init__(self, workspace_dir, comfyui_workflow_path):
        self.workspace_dir = Path(workspace_dir)
        self.comfyui_workflow_path = Path(comfyui_workflow_path)
        
        # Import path configuration
        try:
            # Add config directory to path
            config_path = str(self.workspace_dir / "config")
            if config_path not in sys.path:
                sys.path.insert(0, config_path)
            
            from settings import (
                FUSED_PROMPTS_OUTPUT, 
                WORKFLOWS_OUTPUT_DIR,
                USER_IMAGES_DIR,
                INPUT_SEEDS_DIR
            )
            self.fused_prompts_path = FUSED_PROMPTS_OUTPUT
            self.workflows_output_dir = WORKFLOWS_OUTPUT_DIR
            self.user_images_dir = USER_IMAGES_DIR  
            self.input_seeds_dir = INPUT_SEEDS_DIR
        except ImportError:
            # If path configuration not available, use default paths
            self.data_dir = self.workspace_dir / "data"
            self.fused_prompts_path = self.data_dir / "generated_outputs" / "fused_prompts.json"
            self.workflows_output_dir = self.workspace_dir / "outputs" / "workflows"
            self.user_images_dir = self.data_dir / "personalization_seeds" / "images"
            self.input_seeds_dir = self.data_dir / "input_seeds"
        
        # Ensure output directory exists
        self.workflows_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load workflow template and prompts
        self.workflow_template = self.load_workflow_template()
        self.fused_prompts = self.load_fused_prompts()
        
    def load_workflow_template(self):
        """Load ComfyUI workflow template"""
        try:
            with open(self.comfyui_workflow_path, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
            logging.info(f"Successfully loaded workflow template: {self.comfyui_workflow_path}")
            return workflow
        except Exception as e:
            logging.error(f"Failed to load workflow template: {str(e)}")
            return None
    
    def load_fused_prompts(self):
        """Load fused prompts"""
        try:
            with open(self.fused_prompts_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check file format
            if "prompts" in data and "negative_prompts" in data:
                # New format: convert to expected format
                converted_prompts = {}
                prompts = data["prompts"]
                negative_prompts = data["negative_prompts"]
                
                for key in prompts.keys():
                    if key in negative_prompts:
                        converted_prompts[key] = {
                            "prompt": prompts[key],
                            "negative_prompt": negative_prompts[key]
                        }
                
                logging.info(f"Successfully loaded fused prompts: {len(converted_prompts)} items")
                return converted_prompts
            else:
                # Old format: use directly
                logging.info(f"Successfully loaded fused prompts: {len(data)} items")
                return data
                
        except Exception as e:
            logging.error(f"Failed to load fused prompts: {str(e)}")
            return {}
    
    def find_node_by_type(self, workflow, node_type):
        """Find nodes of specified type in workflow"""
        nodes = []
        for node in workflow.get("nodes", []):
            if node.get("type") == node_type:
                nodes.append(node)
        return nodes
    
    def update_text_prompts(self, workflow, positive_prompt, negative_prompt):
        """Update text prompts in workflow"""
        clip_nodes = self.find_node_by_type(workflow, "CLIPTextEncode")
        
        if len(clip_nodes) >= 2:
            for i, node in enumerate(clip_nodes):
                if i == 0:  # Negative prompt
                    node["widgets_values"] = [negative_prompt]
                elif i == 1:  # Positive prompt
                    node["widgets_values"] = [positive_prompt]
    
    def get_input_seed_image_path(self, input_seed_id):
        """Get input seed image path"""
        image_extensions = ['.png', '.jpg', '.jpeg']
        seed_dir = self.input_seeds_dir / "images" / str(input_seed_id)
        
        if not seed_dir.exists():
            return None
        
        for image_file in seed_dir.glob(f"{input_seed_id}.*"):
            if image_file.suffix.lower() in image_extensions:
                return str(image_file)
        
        return None

    def get_multiple_input_seed_images(self, input_seed_id, count=3):
        """Get multiple image paths for specified input seed"""
        image_extensions = ['.png', '.jpg', '.jpeg']
        seed_dir = self.input_seeds_dir / "images" / str(input_seed_id)
        
        if not seed_dir.exists():
            return []
        
        image_files = []
        for image_file in seed_dir.glob(f"{input_seed_id}.*"):
            if image_file.suffix.lower() in image_extensions:
                image_files.append(str(image_file))
        
        image_files.sort()
        
        result = []
        for i in range(count):
            if image_files:
                result.append(image_files[i % len(image_files)])
            else:
                result.append(None)
        
        return result
    
    def get_personalization_seed_image_path(self, user_id):
        """Get personalization seed image path"""
        image_extensions = ['.png', '.jpg', '.jpeg']
        base_path = self.user_images_dir / f"P{user_id}"
        
        for ext in image_extensions:
            image_path = base_path.with_suffix(ext)
            if image_path.exists():
                return str(image_path)
        
        return None
    
    def update_ipadapter_images(self, workflow, input_seed_ids):
        """Update IPAdapter node reference images"""
        load_image_nodes = self.find_node_by_type(workflow, "LoadImage")
        
        seed_load_nodes = []
        for node in load_image_nodes:
            pos_y = node.get("pos", [0, 0])[1]
            if pos_y < 500:  # Assume input seed nodes are at the top
                seed_load_nodes.append(node)
        
        if len(input_seed_ids) == 1 or all(seed_id == input_seed_ids[0] for seed_id in input_seed_ids):
            input_seed_id = input_seed_ids[0]
            image_paths = self.get_multiple_input_seed_images(input_seed_id, len(seed_load_nodes))
            
            for i, image_path in enumerate(image_paths):
                if i < len(seed_load_nodes) and image_path:
                    filename = os.path.basename(image_path)
                    seed_load_nodes[i]["widgets_values"] = [filename, "image"]
        else:
            available_seeds = input_seed_ids[:len(seed_load_nodes)]
            
            for i, seed_id in enumerate(available_seeds):
                if i < len(seed_load_nodes):
                    image_path = self.get_input_seed_image_path(seed_id)
                    if image_path:
                        filename = os.path.basename(image_path)
                        seed_load_nodes[i]["widgets_values"] = [filename, "image"]
        
        return len(seed_load_nodes)
    
    def update_controlnet_image(self, workflow, user_id):
        """Update ControlNet reference image"""
        load_image_nodes = self.find_node_by_type(workflow, "LoadImage")
        
        controlnet_load_node = None
        max_y = -1
        for node in load_image_nodes:
            pos_y = node.get("pos", [0, 0])[1]
            if pos_y > max_y:
                max_y = pos_y
                controlnet_load_node = node
        
        if controlnet_load_node:
            image_path = self.get_personalization_seed_image_path(user_id)
            if image_path:
                filename = os.path.basename(image_path)
                controlnet_load_node["widgets_values"] = [filename, "image"]
                return True
        
        return False
    
    def update_seed_and_filename(self, workflow, combination_key):
        """Update random seed and save filename"""
        ksampler_nodes = self.find_node_by_type(workflow, "KSampler")
        if ksampler_nodes:
            random_seed = random.randint(1, 999999)
            ksampler_nodes[0]["widgets_values"][0] = random_seed
        
        save_image_nodes = self.find_node_by_type(workflow, "SaveImage")
        if save_image_nodes:
            filename_prefix = f"monster_{combination_key}"
            save_image_nodes[0]["widgets_values"] = [filename_prefix]
    
    def generate_single_image(self, combination_key, prompt_data):
        """Generate image for single combination"""
        if not self.workflow_template:
            return False
        
        workflow = copy.deepcopy(self.workflow_template)
        
        parts = combination_key.split('_')
        if len(parts) < 2:
            return False
        
        user_id = parts[0]
        input_seed_id = '_'.join(parts[1:])
        
        # Update text prompts
        positive_prompt = prompt_data.get("prompt", "")
        negative_prompt = prompt_data.get("negative_prompt", "")
        self.update_text_prompts(workflow, positive_prompt, negative_prompt)
        
        # Update IPAdapter images
        self.update_ipadapter_images(workflow, [input_seed_id, input_seed_id, input_seed_id])
        
        # Update ControlNet image
        self.update_controlnet_image(workflow, user_id)
        
        # Update seed and filename
        self.update_seed_and_filename(workflow, combination_key)
        
        # Save workflow file
        output_workflow_path = self.workflows_output_dir / f"workflow_{combination_key}.json"
        try:
            with open(output_workflow_path, 'w', encoding='utf-8') as f:
                json.dump(workflow, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def generate_batch_workflows(self, limit=None, specific_combo=None):
        """Batch generate workflows for all combinations"""
        if not self.fused_prompts:
            return None
        
        if specific_combo:
            if specific_combo in self.fused_prompts:
                prompt_data = self.fused_prompts[specific_combo]
                if self.generate_single_image(specific_combo, prompt_data):
                    return {
                        "total_combinations": 1,
                        "successful_count": 1,
                        "failed_count": 0
                    }
                else:
                    return {
                        "total_combinations": 1,
                        "successful_count": 0,
                        "failed_count": 1
                    }
            else:
                return None
        
        items = list(self.fused_prompts.items())
        if limit:
            items = items[:limit]
        
        success_count = 0
        total_count = len(items)
        
        for combination_key, prompt_data in items:
            if self.generate_single_image(combination_key, prompt_data):
                success_count += 1
        
        logging.info(f"Batch generation completed: success {success_count}/{total_count}")
        
        # Copy required image files
        self.copy_required_images()
        
        return {
            "total_combinations": total_count,
            "successful_count": success_count,
            "failed_count": total_count - success_count
        }
    
    def copy_required_images(self, specific_combo=None):
        """Copy required image files to ComfyUI accessible location"""
        images_output_dir = self.workflows_output_dir / "input_images"
        images_output_dir.mkdir(exist_ok=True)
        
        copied_count = 0
        
        if specific_combo:
            if specific_combo in self.fused_prompts:
                parts = specific_combo.split('_')
                user_id = parts[0]
                input_seed_id = '_'.join(parts[1:])
                
                # Copy multiple input seed images
                input_seed_images = self.get_multiple_input_seed_images(input_seed_id, 3)
                for source_path in input_seed_images:
                    if source_path:
                        dest_path = images_output_dir / os.path.basename(source_path)
                        try:
                            shutil.copy2(source_path, dest_path)
                            copied_count += 1
                        except Exception:
                            pass
                
                # Copy personalization seed image
                source_path = self.get_personalization_seed_image_path(user_id)
                if source_path:
                    dest_path = images_output_dir / os.path.basename(source_path)
                    try:
                        shutil.copy2(source_path, dest_path)
                        copied_count += 1
                    except Exception:
                        pass
            
            return copied_count
        
        # Batch copy
        input_seeds_used = set()
        personalization_seeds_used = set()
        
        for combination_key in self.fused_prompts.keys():
            parts = combination_key.split('_')
            user_id = parts[0]
            input_seed_id = '_'.join(parts[1:])
            
            input_seeds_used.add(input_seed_id)
            personalization_seeds_used.add(user_id)
        
        # Copy input seed images
        for seed_id in input_seeds_used:
            input_seed_images = self.get_multiple_input_seed_images(seed_id, 3)
            for source_path in input_seed_images:
                if source_path:
                    dest_path = images_output_dir / os.path.basename(source_path)
                    if not dest_path.exists():
                        try:
                            shutil.copy2(source_path, dest_path)
                            copied_count += 1
                        except Exception:
                            pass
        
        # Copy personalization seed images
        for user_id in personalization_seeds_used:
            source_path = self.get_personalization_seed_image_path(user_id)
            if source_path:
                dest_path = images_output_dir / os.path.basename(source_path)
                if not dest_path.exists():
                    try:
                        shutil.copy2(source_path, dest_path)
                        copied_count += 1
                    except Exception:
                        pass
        
        logging.info(f"Image copy completed: {copied_count} files")
        return copied_count

def main():
    """Main function"""
    # Get current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(current_dir)  # Workspace directory
    
    # ComfyUI workflow file path
    workflow_path = os.path.join(workspace_dir, "controlnet2.json")
    
    # Check if file exists
    if not os.path.exists(workflow_path):
        logging.error(f"ComfyUI workflow file does not exist: {workflow_path}")
        return
    
    # Create integrator
    integrator = ComfyUIIntegrator(workspace_dir, workflow_path)
    
    # Check if there are fused prompts
    if not integrator.fused_prompts:
        logging.error("Please run user_feature_extractor.py first to generate fused prompts")
        return
    
    # Parse command line arguments
    import sys
    limit = None
    specific_combo = None
    
    # Parse parameters
    for i, arg in enumerate(sys.argv):
        if arg.isdigit() and i == 1:  # First parameter is a number, indicating limit
            limit = int(arg)
        elif arg == "--combo" and i + 1 < len(sys.argv):
            specific_combo = sys.argv[i + 1]
            logging.info(f"Processing specific combination: {specific_combo}")
    
    # Copy required images
    integrator.copy_required_images(specific_combo)
    
    # Generate workflows
    result = integrator.generate_batch_workflows(limit, specific_combo)
    
    logging.info(f"ComfyUI integration completed!")
    logging.info(f"Successfully generated {result['successful_count']} workflow files")
    logging.info(f"Output directory: {integrator.workflows_output_dir}")
    
    if specific_combo:
        print(f"\n=== Specific combination processing completed ===")
        print(f"Combination: {specific_combo}")
        print(f"Workflow file: workflow_{specific_combo}.json")
        print(f"Expected output: monster_{specific_combo}.png")
    else:
        print("\n=== Next steps guide ===")
        print("1. Import the generated workflow files into ComfyUI")
        print("2. Make sure ComfyUI can access the image files in the input_images directory")
        print("3. Run the workflow in ComfyUI to generate images")
        print("4. Generated image file names format: monster_[user_id]_[input_seed_id]")

if __name__ == "__main__":
    main() 