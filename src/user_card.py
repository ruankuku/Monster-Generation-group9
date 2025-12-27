"""
Integrated Monster Card Generator
"""

from PIL import Image, ImageDraw, ImageFont
import os
import json
import logging
import glob
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IntegratedMonsterCardGenerator:
    """Integrated monster character card generator"""
    
    def __init__(self, workspace_dir=None):
        """Initialize generator"""
        if workspace_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            workspace_dir = os.path.dirname(current_dir)
        
        self.workspace_dir = Path(workspace_dir)
        self.setup_paths()
        self.load_character_data()
    
    def setup_paths(self):
        """Setup paths"""
        try:
            import sys
            config_path = str(Path(__file__).parent.parent / "config")
            if config_path not in sys.path:
                sys.path.insert(0, config_path)
            
            from settings import (
                FEATURES_OUTPUT_DIR,
                GENERATED_IMAGES_DIR,
                GENERATED_CARDS_DIR,
                get_workspace_dir
            )
            
            workspace_dir = get_workspace_dir()
            
            self.template_path = workspace_dir / "data" / "card.png"
            self.comfyui_output_dir = GENERATED_IMAGES_DIR
            self.final_output_dir = GENERATED_CARDS_DIR
            self.final_output_dir.mkdir(parents=True, exist_ok=True)
            
            self.characters_file = FEATURES_OUTPUT_DIR / "monster_characters_simple.json"
            
        except ImportError:
            # Fallback to old path configuration
            self.template_path = self.workspace_dir / "data" / "card.png"
            self.comfyui_output_dir = self.workspace_dir / "data" / "generated_outputs" / "final_images"
            self.final_output_dir = self.workspace_dir / "data" / "generated_outputs" / "final_cards"
            self.final_output_dir.mkdir(parents=True, exist_ok=True)
            self.characters_file = self.workspace_dir / "data" / "generated_outputs" / "monster_characters_simple.json"
        
        # Font paths
        self.font_title_path = self.workspace_dir / "models" / "blackletter_ds" / "BLACEB_.TTF"
        self.font_desc_path = self.workspace_dir / "models" / "kalina_2" / "Kalina - PERSONAL USE ONLY.ttf"
    
    def load_character_data(self):
        """Load character data"""
        try:
            if self.characters_file.exists():
                with open(self.characters_file, 'r', encoding='utf-8') as f:
                    self.characters_data = json.load(f)
                logging.info(f"Successfully loaded character data: {len(self.characters_data)} characters")
            else:
                self.characters_data = {}
        except Exception:
            self.characters_data = {}
    
    def find_generated_images(self):
        """Find ComfyUI generated images"""
        image_files = {}
        
        for ext in ['*.png', '*.jpg', '*.jpeg']:
            pattern = str(self.comfyui_output_dir / f"monster_*{ext}")
            files = glob.glob(pattern)
            
            for file_path in files:
                filename = os.path.basename(file_path)
                if filename.startswith('monster_'):
                    name_without_ext = os.path.splitext(filename)[0]
                    parts = name_without_ext.split('_')
                    if len(parts) >= 3:
                        combination_key = f"{parts[1]}_{parts[2]}"
                        image_files[combination_key] = file_path
        
        logging.info(f"Found {len(image_files)} generated images")
        return image_files
    
    def find_optimal_font_size(self, draw, text, font_path, max_width, max_height):
        """Dynamically adjust font size"""
        font_size = 1
        while True:
            try:
                font = ImageFont.truetype(str(font_path), font_size)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                if text_width > max_width or text_height > max_height:
                    font_size -= 1
                    break
                font_size += 1
            except:
                font_size -= 1
                break

        try:
            return ImageFont.truetype(str(font_path), max(font_size, 1))
        except:
            return ImageFont.load_default()
    
    def wrap_text(self, text, font, max_width, draw):
        """Auto-wrap text"""
        lines = []
        words = text.split()
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]

            if w <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        return lines
    
    def generate_card(self, combination_key, character_data, monster_image_path):
        """Generate single character card"""
        try:
            if not self.template_path.exists():
                return False
            
            background = Image.open(self.template_path).convert("RGBA")
            
            if not os.path.exists(monster_image_path):
                return False
            
            monster = Image.open(monster_image_path).convert("RGBA")
            
            # Adjust monster image size and paste to background
            monster_resized = monster.resize((765, 765))
            monster_position = (58, 222)
            background.paste(monster_resized, monster_position, monster_resized)
            
            # Get character information
            monster_name = character_data.get("name", "UNKNOWN")
            description = character_data.get("description", "A mysterious creature.")
            
            # Set text area
            box_x, box_y = 58, 1000
            box_width, box_height = 600, 136
            
            # Initialize drawing object
            draw = ImageDraw.Draw(background)
            
            # Load fonts
            try:
                dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
                font_title = self.find_optimal_font_size(dummy_draw, monster_name, self.font_title_path, box_width, box_height)
                font_desc = ImageFont.truetype(str(self.font_desc_path), 28)
            except:
                font_title = ImageFont.load_default()
                font_desc = ImageFont.load_default()
            
            # Draw title
            bbox = draw.textbbox((0, 0), monster_name, font=font_title)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = box_x + (box_width - text_width) // 2
            text_y = box_y + (box_height - text_height) // 2 - 20
            
            draw.text((text_x, text_y), monster_name, font=font_title, fill="black")
            
            # Set description text area
            desc_box_x, desc_box_y = 73, 1177
            desc_box_width = 656 - 73   
            desc_box_height = 1455 - 1177  
            
            # Draw description text
            wrapped_lines = self.wrap_text(description, font_desc, desc_box_width, draw)
            
            line_spacing = 6
            line_height = font_desc.getbbox("A")[3] - font_desc.getbbox("A")[1] + line_spacing
            total_text_height = len(wrapped_lines) * line_height
            
            start_y = desc_box_y + (desc_box_height - total_text_height) // 2
            
            for i, line in enumerate(wrapped_lines):
                y = start_y + i * line_height
                draw.text((desc_box_x, y), line, font=font_desc, fill="black")
            
            # Save final image
            output_filename = f"monster_card_{combination_key}.png"
            output_path = self.final_output_dir / output_filename
            background.save(str(output_path))
            
            return True
            
        except Exception:
            return False
    
    def generate_all_cards(self):
        """Generate all character cards"""
        image_files = self.find_generated_images()
        
        if not image_files:
            return {
                "total_count": 0,
                "successful_count": 0,
                "failed_count": 0
            }
        
        if not self.characters_data:
            return {
                "total_count": len(image_files),
                "successful_count": 0,
                "failed_count": len(image_files)
            }
        
        success_count = 0
        total_count = 0
        
        for combination_key, image_path in image_files.items():
            total_count += 1
            
            character_data = self.characters_data.get(combination_key)
            if not character_data:
                continue
            
            if self.generate_card(combination_key, character_data, image_path):
                success_count += 1
        
        failed_count = total_count - success_count
        logging.info(f"Complete! Successfully generated {success_count}/{total_count} character cards")
        
        return {
            "total_count": total_count,
            "successful_count": success_count,
            "failed_count": failed_count
        }
    
    def generate_single_card(self, combination_key):
        """Generate single character card"""
        image_files = self.find_generated_images()
        image_path = image_files.get(combination_key)
        
        if not image_path:
            return False
        
        character_data = self.characters_data.get(combination_key)
        if not character_data:
            return False
        
        return self.generate_card(combination_key, character_data, image_path)

def main():
    """Main function"""
    generator = IntegratedMonsterCardGenerator()
    generator.generate_all_cards()

if __name__ == "__main__":
    main()
