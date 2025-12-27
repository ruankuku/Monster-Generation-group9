"""
Monster Generation Project Main Program - One-click execution of complete workflow
"""

import sys
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent / "config"))

# Import path configuration
from config.settings import initialize_paths

def setup_logging():
    """Setup logging system"""
    from config.settings import LOG_FILE
    
    # Ensure log directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure log format
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def validate_setup():
    """Validate project setup"""
    logger = logging.getLogger(__name__)
    
    from config.settings import validate_setup
    issues = validate_setup()
    
    if issues:
        logger.error("Project setup validation failed:")
        for issue in issues:
            logger.error(f"  - {issue}")
        return False
    
    logger.info("Project setup validation passed")
    return True

def run_feature_extraction():
    """Run feature extraction"""
    logger = logging.getLogger(__name__)
    
    try:
        from config.settings import USER_DATA_SIMPLIFIED_CSV, USER_IMAGES_DIR, INPUT_SEEDS_DIR, FUSED_PROMPTS_OUTPUT
        from user_feature_extractor import UserFeatureExtractor
        
        # Check if fused prompts file already exists
        if FUSED_PROMPTS_OUTPUT.exists():
            logger.info("Fused prompts file already exists, skipping feature extraction step")
            return True
        
        extractor = UserFeatureExtractor(
            csv_path=USER_DATA_SIMPLIFIED_CSV,
            images_dir=USER_IMAGES_DIR,
            input_seeds_dir=INPUT_SEEDS_DIR
        )
        
        # Process personalization seeds
        logger.info("Processing personalization seeds...")
        personalization_results = extractor.process_all_users()
        
        # Process input seeds
        logger.info("Processing input seeds...")
        input_results = extractor.process_all_input_seeds()
        
        # Fuse prompts
        logger.info("Fusing prompts...")
        fused_results = extractor.fusion_prompts(personalization_results, input_results)
        
        # Save results
        success = extractor.save_simple_prompts(fused_results, FUSED_PROMPTS_OUTPUT)
        
        if success:
            logger.info("Feature extraction completed")
            return True
        else:
            logger.error("Feature extraction failed")
            return False
            
    except Exception as e:
        logger.error(f"Feature extraction process error: {str(e)}")
        return False

def run_workflow_generation():
    """Run workflow generation"""
    logger = logging.getLogger(__name__)
    
    try:
        from config.settings import COMFYUI_WORKFLOW_TEMPLATE, get_workspace_dir, WORKFLOWS_OUTPUT_DIR
        from comfyui_integration import ComfyUIIntegrator
        
        # Check if workflow files already exist
        workflow_files = list(WORKFLOWS_OUTPUT_DIR.glob("workflow_*.json"))
        if workflow_files:
            logger.info(f"⏭{len(workflow_files)} workflow files already exist, skipping workflow generation step")
            return True
        
        logger.info("⚙️ Starting workflow generation...")
        
        workspace_dir = get_workspace_dir()
        integrator = ComfyUIIntegrator(workspace_dir, COMFYUI_WORKFLOW_TEMPLATE)
        
        results = integrator.generate_batch_workflows()
        
        if results and results.get("successful_count", 0) > 0:
            logger.info(f"Workflow generation completed: {results['successful_count']}/{results['total_combinations']}")
            return True
        else:
            logger.error("Workflow generation failed")
            return False
            
    except Exception as e:
        logger.error(f"Workflow generation process error: {str(e)}")
        return False

def run_image_generation():
    """Run image generation"""
    logger = logging.getLogger(__name__)
    
    try:
        from config.settings import get_workspace_dir
        from automated_monster_generator import AutomatedMonsterGenerator
        
        logger.info("Starting image generation...")
        
        workspace_dir = get_workspace_dir()
        generator = AutomatedMonsterGenerator(workspace_dir=workspace_dir)
        
        # Check ComfyUI server
        if not generator.check_comfyui_server():
            logger.warning("ComfyUI server not running, skipping image generation")
            logger.info("Please start ComfyUI server and run again")
            return True  # Not a failure, just skipped
        
        results = generator.generate_all_combinations()
        
        if results:
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            logger.info(f"Image generation completed: {successful}/{total}")
            return True
        else:
            logger.error("Image generation failed")
            return False
            
    except Exception as e:
        logger.error(f"Image generation process error: {str(e)}")
        return False

def run_character_generation():
    """Run character generation"""
    logger = logging.getLogger(__name__)
    
    try:
        from config.settings import get_workspace_dir
        from simple_character_generator import SimpleCharacterGenerator
        
        logger.info("Starting character generation...")
        
        workspace_dir = get_workspace_dir()
        generator = SimpleCharacterGenerator(workspace_dir)
        
        characters = generator.generate_all_characters()
        
        if characters:
            logger.info(f"Character generation completed: {len(characters)} characters")
            return True
        else:
            logger.error("Character generation failed")
            return False
            
    except Exception as e:
        logger.error(f"Character generation process error: {str(e)}")
        return False

def run_card_generation():
    """Run card generation"""
    logger = logging.getLogger(__name__)
    
    try:
        from config.settings import get_workspace_dir
        from user_card import IntegratedMonsterCardGenerator
        
        logger.info("Starting card generation...")
        
        workspace_dir = get_workspace_dir()
        generator = IntegratedMonsterCardGenerator(workspace_dir)
        
        results = generator.generate_all_cards()
        
        if results and results.get("successful_count", 0) > 0:
            logger.info(f"Card generation completed: {results['successful_count']}/{results['total_count']}")
            return results
        else:
            logger.error("Card generation failed")
            return {"total_count": 0, "successful_count": 0, "failed_count": 0}
            
    except Exception as e:
        logger.error(f"Card generation process error: {str(e)}")
        return {"total_count": 0, "successful_count": 0, "failed_count": 0}

def main():
    """Main function - run complete generation workflow"""
    print("Starting Monster Generation Project...")
    
    # Initialize system
    initialize_paths()
    logger = setup_logging()
    
    logger.info("=" * 50)
    logger.info("Monster Generation Project - Complete Workflow")
    logger.info("=" * 50)
    
    # Step 1: Validate project setup
    logger.info("Step 1: Validate project setup")
    if not validate_setup():
        logger.error("Project setup validation failed, program terminated")
        return False
    
    # Step 2: Feature extraction
    logger.info("Step 2: User feature extraction")
    if not run_feature_extraction():
        logger.error("Feature extraction failed, program terminated")
        return False
    
    # Step 3: Workflow generation
    logger.info("Step 3: ComfyUI workflow generation")
    if not run_workflow_generation():
        logger.error("Workflow generation failed, program terminated")
        return False
    
    # Step 4: Image generation
    logger.info("Step 4: ComfyUI image generation")
    run_image_generation()  # Not mandatory for success, as ComfyUI might not be running
    
    # Step 5: Character generation
    logger.info("Step 5: Character description generation")
    if not run_character_generation():
        logger.warning("Character generation failed, continuing with next steps")
    
    # Step 6: Card generation
    logger.info("Step 6: User card generation")
    card_results = run_card_generation()
    
    # Final summary
    logger.info("=" * 50)
    success = True
    if card_results and card_results.get("successful_count", 0) > 0:
        logger.info("Complete generation workflow finished!")
        logger.info("Check results:")
        from config.settings import FEATURES_OUTPUT_DIR, WORKFLOWS_OUTPUT_DIR, get_workspace_dir
        logger.info(f"   - Feature extraction results: {FEATURES_OUTPUT_DIR}")
        logger.info(f"   - Workflow files: {WORKFLOWS_OUTPUT_DIR}")
        logger.info(f"   - Generated images: {get_workspace_dir()}/outputs/generated_outputs/final_images/")
        logger.info(f"   - User cards: {get_workspace_dir()}/outputs/generated_outputs/final_cards/")
    else:
        logger.warning("Workflow completed, but some steps might not have succeeded")
        success = False
    
    logger.info("=" * 50)
    return success

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n Program execution completed!")
        else:
            print("\n Program execution completed with issues, please check logs")
    except KeyboardInterrupt:
        print("\n User interrupted program")
    except Exception as e:
        print(f"\n Program execution failed: {str(e)}")
        import traceback
        traceback.print_exc() 
