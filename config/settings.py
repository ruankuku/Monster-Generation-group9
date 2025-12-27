"""
Path Configuration File - Provides unified path management for the feature/ directory original code
"""

import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_workspace_dir():
    """Get workspace directory"""
    current_file = Path(__file__).resolve()
    workspace_dir = current_file.parent.parent
    return workspace_dir

# Base directory paths
WORKSPACE_DIR = get_workspace_dir()
DATA_DIR = WORKSPACE_DIR / "data"
OUTPUTS_DIR = WORKSPACE_DIR / "outputs"

# Data subdirectories
PERSONALIZATION_SEEDS_DIR = DATA_DIR / "personalization_seeds"
INPUT_SEEDS_DIR = DATA_DIR / "input_seeds"

# Output subdirectories
FEATURES_OUTPUT_DIR = OUTPUTS_DIR / "features"
WORKFLOWS_OUTPUT_DIR = OUTPUTS_DIR / "workflows"
LOGS_OUTPUT_DIR = OUTPUTS_DIR / "logs"
GENERATED_IMAGES_DIR = OUTPUTS_DIR / "generated_outputs" / "final_images"
GENERATED_CARDS_DIR = OUTPUTS_DIR / "generated_outputs" / "final_cards"

# Input file paths
USER_DATA_CSV = PERSONALIZATION_SEEDS_DIR / "monster.csv"
USER_DATA_SIMPLIFIED_CSV = PERSONALIZATION_SEEDS_DIR / "user_preferences.csv"
USER_IMAGES_DIR = PERSONALIZATION_SEEDS_DIR / "images"
INPUT_SEEDS_IMAGES_DIR = INPUT_SEEDS_DIR / "images"
INPUT_SEEDS_TEXTS_DIR = INPUT_SEEDS_DIR / "texts"

# Output file paths
PERSONALIZED_PROMPTS_OUTPUT = FEATURES_OUTPUT_DIR / "personalized_prompts.json"
FUSED_PROMPTS_OUTPUT = FEATURES_OUTPUT_DIR / "fused_prompts.json"
LOG_FILE = LOGS_OUTPUT_DIR / "monster_generation.log"

# ComfyUI related paths
COMFYUI_WORKFLOW_TEMPLATE = DATA_DIR / "comfyui_template.json"
COMFYUI_INPUT_IMAGES_DIR = WORKFLOWS_OUTPUT_DIR / "input_images"

def ensure_directories():
    """Ensure all necessary directories exist"""
    directories = [
        OUTPUTS_DIR,
        FEATURES_OUTPUT_DIR,
        WORKFLOWS_OUTPUT_DIR,
        LOGS_OUTPUT_DIR,
        COMFYUI_INPUT_IMAGES_DIR,
        GENERATED_IMAGES_DIR,
        GENERATED_CARDS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def initialize_paths():
    """Initialize path system"""
    ensure_directories()
    logging.info("Path system initialization completed")

# Validate critical files and directories
def validate_setup():
    """Validate project setup"""
    issues = []
    
    # Check required files
    required_files = [
        USER_DATA_SIMPLIFIED_CSV,
        COMFYUI_WORKFLOW_TEMPLATE
    ]
    
    for file_path in required_files:
        if not file_path.exists():
            issues.append(f"Missing file: {file_path}")
    
    # Check required directories
    required_dirs = [
        PERSONALIZATION_SEEDS_DIR,
        INPUT_SEEDS_DIR,
        USER_IMAGES_DIR
    ]
    
    for dir_path in required_dirs:
        if not dir_path.exists():
            issues.append(f"Missing directory: {dir_path}")
    
    return issues

if __name__ == "__main__":
    initialize_paths()
    issues = validate_setup()
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ All paths configured correctly") 