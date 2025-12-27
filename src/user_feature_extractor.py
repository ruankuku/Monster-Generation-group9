"""
User Feature Extractor - Simplified Version
"""

import sys
from pathlib import Path

# Add config directory to path
config_path = str(Path(__file__).parent.parent / "config")
if config_path not in sys.path:
    sys.path.insert(0, config_path)

import pandas as pd
import json
import logging
import os
import random

# Import mappings with fallback
try:
    from mappings import (
        MOVIE_GAME_KEYWORD_MAPPING,
        CHARACTER_KEYWORD_MAPPING,
        COLOR_KEYWORD_MAPPING,
        STYLE_KEYWORD_MAPPING
    )
except ImportError:
    # Fallback mappings if import fails
    MOVIE_GAME_KEYWORD_MAPPING = {
        'Science Fiction': ['futuristic', 'technological', 'alien'],
        'Fantasy': ['magical', 'mystical', 'enchanted'],
        'Horror': ['dark', 'frightening', 'mysterious']
    }
    CHARACTER_KEYWORD_MAPPING = {
        'Dragon': ['draconic', 'powerful', 'ancient'],
        'Alien': ['extraterrestrial', 'otherworldly'],
        'Robot': ['mechanical', 'artificial']
    }
    COLOR_KEYWORD_MAPPING = {
        'Dark': ['shadowy', 'dim'],
        'Bright': ['luminous', 'radiant']
    }
    STYLE_KEYWORD_MAPPING = {
        'Fantasy': ['magical', 'mystical'],
        'Sci-fi': ['futuristic', 'technological']
    }

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UserFeatureExtractor:
    """User feature extractor that extracts user features from CSV files and generates prompts"""
    
    def __init__(self, csv_path, images_dir=None, input_seeds_dir=None):
        self.csv_path = csv_path
        self.images_dir = images_dir
        self.input_seeds_dir = input_seeds_dir
        self.user_data = None
        
        # Use imported keyword mappings
        self.keyword_mapping = MOVIE_GAME_KEYWORD_MAPPING
        self.character_mapping = CHARACTER_KEYWORD_MAPPING
        self.color_mapping = COLOR_KEYWORD_MAPPING
        self.style_mapping = STYLE_KEYWORD_MAPPING
        
        # Quality enhancement words
        self.quality_enhancers = [
            "highly detailed", "masterpiece", "best quality", "4k", "8k",
            "extremely detailed", "intricate", "professional", "award winning",
            "stunning", "beautiful lighting", "sharp focus", "studio quality"
        ]
        
        # Negative prompts
        self.negative_prompts = [
            "low quality", "bad anatomy", "worst quality", "poorly drawn", 
            "blurry", "distorted", "deformed", "disfigured", "mutated", 
            "text", "watermark", "signature", "cropped", "jpeg artifacts",
            "out of frame", "ugly", "duplicate", "morbid", "mutilated",
            "extra limbs", "missing limbs", "disconnected limbs",
            "malformed hands", "malformed fingers", "extra fingers",
            "fused fingers", "too many fingers", "long neck"
        ]
    
    def load_data(self):
        """Load CSV data"""
        try:
            self.user_data = pd.read_csv(self.csv_path)
            logging.info(f"Successfully loaded user data with {len(self.user_data)} records")
            return True
        except Exception as e:
            logging.error(f"Failed to load CSV file: {str(e)}")
            return False
    
    def extract_user_features(self, row):
        """Extract features from user row data"""
        preferences = row["What is your favorite type of movies or games?"]
        character_prefs = row["Which character or monster type do you like best?"]
        
        # Split preferences
        pref_keywords = [keyword.strip() for keyword in preferences.split('/')]
        character_keywords = [keyword.strip() for keyword in character_prefs.split('/')] if pd.notna(character_prefs) else []
        
        # Get related visual and conceptual features from keyword mappings
        visual_features = []
        for keyword in pref_keywords:
            for map_key, features in self.keyword_mapping.items():
                if map_key in keyword:
                    visual_features.extend(features)
        
        # Process character keywords
        character_features = []
        for keyword in character_keywords:
            for map_key, features in self.character_mapping.items():
                if map_key in keyword:
                    character_features.extend(features)
        
        # If no mapping found, use original keywords
        if not visual_features:
            visual_features = pref_keywords
        
        # Remove duplicates
        visual_features = list(set(visual_features))
        character_features = list(set(character_features))
        
        # Add user's other preferences
        color_pref = row["User color preference"] if pd.notna(row["User color preference"]) else ""
        visual_style = row["User visual style preference"] if pd.notna(row["User visual style preference"]) else ""
        
        # Split color and visual style preferences
        color_keywords = [color.strip() for color in color_pref.split('/')] if color_pref else []
        style_keywords = [style.strip() for style in visual_style.split('/')] if visual_style else []
        
        # Extract color and style features
        color_features = []
        for keyword in color_keywords:
            for map_key, features in self.color_mapping.items():
                if map_key in keyword:
                    color_features.extend(features)
        
        style_features = []
        for keyword in style_keywords:
            for map_key, features in self.style_mapping.items():
                if map_key in keyword:
                    style_features.extend(features)
        
        # If no mapping found, use original keywords
        if not color_features:
            color_features = color_keywords
        if not style_features:
            style_features = style_keywords
        
        # Combine all text features
        text_features = visual_features + character_features + color_features + style_features
        
        return {
            "user_id": row["number"],
            "preferences": pref_keywords,
            "character_preferences": character_keywords,
            "visual_features": visual_features,
            "character_features": character_features,
            "color_features": color_features,
            "style_features": style_features,
            "color_preferences": color_keywords,
            "style_preferences": style_keywords,
            "text_features": text_features
        }
    
    def process_user(self, row):
        """Process single user data"""
        text_features = self.extract_user_features(row)
        user_id = text_features["user_id"]
        
        combined_features = {**text_features}
        combined_features["combined_keywords"] = text_features["text_features"]
        
        return combined_features
    
    def process_all_users(self):
        """Process all user data and return results"""
        if self.user_data is None:
            if not self.load_data():
                return []
        
        results = []
        for _, row in self.user_data.iterrows():
            user_features = self.process_user(row)
            results.append(user_features)
        
        return results
    
    def save_results(self, results, output_path):
        """Save processing results to JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            logging.info(f"Results saved to {output_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to save results: {str(e)}")
            return False
    
    def load_input_seed_text(self, seed_id):
        """Load input seed text content"""
        if not self.input_seeds_dir:
            return None
            
        text_file = os.path.join(self.input_seeds_dir, "texts", f"{seed_id}.txt")
        
        if not os.path.exists(text_file):
            return None
            
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                text_content = f.read().strip()
                
            text_features = self.parse_seed_text(text_content)
            text_features["raw_text"] = text_content
            text_features["seed_id"] = seed_id
            
            return text_features
        except Exception:
            return None
    
    def parse_seed_text(self, text_content):
        """Parse seed text content and extract keywords and features"""
        lines = text_content.strip().split('\n')
        
        keywords = []
        descriptions = []
        
        for line in lines:
            line_keywords = [kw.strip() for kw in line.split(',')]
            keywords.extend(line_keywords)
            descriptions.append(line)
        
        keywords = list(set([kw for kw in keywords if kw]))
        
        return {
            "keywords": keywords,
            "descriptions": descriptions,
            "text_features": keywords
        }
    
    def process_input_seed(self, seed_id):
        """Process single input seed"""
        text_features = self.load_input_seed_text(seed_id)
        
        input_seed_features = {
            "seed_id": seed_id,
            "text_features": text_features["keywords"] if text_features else [],
            "raw_text": text_features["raw_text"] if text_features else ""
        }
        
        input_seed_features["combined_keywords"] = input_seed_features["text_features"]
        
        return input_seed_features
    
    def process_all_input_seeds(self):
        """Process all input seeds"""
        if not self.input_seeds_dir:
            return []
            
        import glob
        text_pattern = os.path.join(self.input_seeds_dir, "texts", "*.txt")
        text_files = glob.glob(text_pattern)
        
        if not text_files:
            return []
            
        seed_ids = [os.path.splitext(os.path.basename(f))[0] for f in text_files]
        
        results = []
        for seed_id in seed_ids:
            seed_features = self.process_input_seed(seed_id)
            results.append(seed_features)
            
        return results
    
    def fusion_prompts(self, personalization_seeds, input_seeds):
        """Fuse personalization seeds and input seeds features to generate prompts"""
        # Extract user features
        user_features = {}
        for p_seed in personalization_seeds:
            user_id = p_seed["user_id"]
            user_features[user_id] = {
                "keywords": p_seed.get("combined_keywords", []),
                "character_prefs": p_seed.get("character_preferences", []),
                "visual_features": p_seed.get("visual_features", []),
                "color_features": p_seed.get("color_features", []),
                "style_features": p_seed.get("style_features", [])
            }
        
        # Extract input seed features
        seed_features = {}
        for i_seed in input_seeds:
            seed_id = i_seed["seed_id"]
            raw_text = i_seed.get("raw_text", "").split('\n') if "raw_text" in i_seed else []
            style_keywords = [line.strip() for line in raw_text if line.strip()]
            seed_features[seed_id] = {"style_keywords": style_keywords}
        
        # Fuse prompts
        fused_prompts = {}
        
        for p_id, p_data in user_features.items():
            for i_id, i_data in seed_features.items():
                key = f"{p_id}_{i_id}"
                
                # Basic creature type
                creature_type = "creature"
                if p_data["character_prefs"]:
                    main_char = p_data["character_prefs"][0].lower()
                    if "alien" in main_char:
                        creature_type = "alien creature"
                    elif "robot" in main_char or "mech" in main_char:
                        creature_type = "biomechanical entity"
                    elif "monster" in main_char or "beast" in main_char:
                        creature_type = "monstrous being"
                    elif "dragon" in main_char:
                        creature_type = "draconic creature"
                    else:
                        creature_type = f"{main_char} creature"
                
                # Combine feature descriptions
                features = []
                if p_data["visual_features"]:
                    features.extend(p_data["visual_features"][:3])
                if p_data["color_features"]:
                    features.extend(p_data["color_features"][:2])
                if p_data["style_features"]:
                    features.extend(p_data["style_features"][:2])
                
                # Build main description
                main_description = f"a {creature_type}"
                if features:
                    main_description += f" with {', '.join(features)}"
                
                # Add quality descriptors
                quality_desc = "highly detailed, professional, masterpiece, best quality"
                
                # Style description
                style_desc = "detailed artistic style"
                if i_data["style_keywords"]:
                    style_content = ', '.join(i_data["style_keywords"])
                    style_desc = f"in style of {style_content}"
                
                # Combine final prompt
                full_prompt = f"{main_description}, {quality_desc}, {style_desc}"
                
                # Generate negative prompt
                negative_prompt = ", ".join(random.sample(self.negative_prompts, min(15, len(self.negative_prompts))))
                
                fused_prompts[key] = {
                    "personalization_seed_id": p_id,
                    "input_seed_id": i_id,
                    "prompt": full_prompt,
                    "negative_prompt": negative_prompt
                }
        
        return fused_prompts
    
    def save_simple_prompts(self, prompts, output_path):
        """Save simplified prompts to JSON file"""
        simple_prompts = {}
        simple_negative_prompts = {}
        
        for key, prompt_data in prompts.items():
            simple_prompts[key] = prompt_data["prompt"]
            simple_negative_prompts[key] = prompt_data["negative_prompt"]
        
        result = {
            "prompts": simple_prompts,
            "negative_prompts": simple_negative_prompts
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            logging.info(f"Simplified prompts saved to {output_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to save simplified prompts: {str(e)}")
            return False

def main():
    """Main function"""
    # Get current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(current_dir)  # Workspace directory
    
    # Build data paths
    data_dir = os.path.join(workspace_dir, "data")
    personalization_seeds_dir = os.path.join(data_dir, "personalization_seeds")
    input_seeds_dir = os.path.join(data_dir, "input_seeds")
    
    # CSV file paths
    original_csv_path = os.path.join(personalization_seeds_dir, "monster.csv")
    simplified_csv_path = os.path.join(personalization_seeds_dir, "user_preferences.csv")
    
    # Choose CSV file based on parameters
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--simplified":
        csv_path = simplified_csv_path
        logging.info("Using simplified CSV file")
    else:
        csv_path = original_csv_path
        logging.info("Using original CSV file")
    
    # Image directory path
    p_images_dir = os.path.join(personalization_seeds_dir, "images")
    
    # Output directory
    output_dir = os.path.join(data_dir, "generated_outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    # Output file paths
    features_output = os.path.join(output_dir, "user_features.json")
    fused_prompts_output = os.path.join(output_dir, "fused_prompts.json")
    simple_prompts_output = os.path.join(output_dir, "simple_prompts.json")
    
    # Check if files and directories exist
    if not os.path.exists(csv_path):
        logging.error(f"CSV file does not exist: {csv_path}")
        return
    
    if not os.path.exists(p_images_dir):
        logging.warning(f"Personalization seed image directory does not exist: {p_images_dir}")
        p_images_dir = None
    
    if not os.path.exists(input_seeds_dir):
        logging.warning(f"Input seeds directory does not exist: {input_seeds_dir}")
        input_seeds_dir = None
    
    logging.info(f"CSV file path: {csv_path}")
    if p_images_dir:
        logging.info(f"Personalization seed image directory: {p_images_dir}")
    if input_seeds_dir:
        logging.info(f"Input seeds directory: {input_seeds_dir}")
    
    # Create feature extractor
    extractor = UserFeatureExtractor(csv_path, p_images_dir, input_seeds_dir)
    
    # Process personalization seeds
    personalization_seeds = extractor.process_all_users()
    
    if not personalization_seeds:
        logging.error("Failed to extract personalization seed features")
        return
    
    # Save personalization seed features
    extractor.save_results(personalization_seeds, features_output)
    
    # Process input seeds
    if input_seeds_dir:
        input_seeds = extractor.process_all_input_seeds()
        
        if input_seeds:
            # Fuse and save final prompts
            fused_prompts = extractor.fusion_prompts(personalization_seeds, input_seeds)
            extractor.save_results(fused_prompts, fused_prompts_output)
            
            # Save simplified prompts
            extractor.save_simple_prompts(fused_prompts, simple_prompts_output)
            
            logging.info(f"Generated {len(fused_prompts)} fused prompts")
            logging.info(f"Fused prompts saved to: {fused_prompts_output}")
            logging.info(f"Simplified prompts saved to: {simple_prompts_output}")
        else:
            logging.warning("Failed to extract input seed features")
    
    logging.info(f"Processing complete! Features saved to: {features_output}")

if __name__ == "__main__":
    main() 