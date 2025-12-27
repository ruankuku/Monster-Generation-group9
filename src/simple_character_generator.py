"""
Simple and Fast Monster Character Generator - Based on existing feature extraction and prompt system
"""

import os
import json
import random
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimpleCharacterGenerator:
    """Fast character generator based on existing features and prompts"""
    
    def __init__(self):
        """Initialize generator"""
        self.setup_paths()
        self.setup_name_components()
        self.setup_description_templates()
        self.load_input_seed_types()
    
    def setup_paths(self):
        """Setup system paths for config import"""
        try:
            # Add config directory to path if not already added
            current_dir = os.path.dirname(os.path.abspath(__file__))
            workspace_dir = os.path.dirname(current_dir)
            config_path = os.path.join(workspace_dir, "config")
            
            if config_path not in sys.path:
                sys.path.insert(0, config_path)
        except Exception as e:
            logging.warning(f"Could not setup config path: {e}")
    
    def load_input_seed_types(self):
        """Load input_seed type mappings"""
        self.input_seed_types = {}
        
        # Get type file directory path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        workspace_dir = os.path.dirname(current_dir)
        type_dir = os.path.join(workspace_dir, "data", "input_seeds", "type")
        
        if os.path.exists(type_dir):
            for filename in os.listdir(type_dir):
                if filename.endswith('.txt'):
                    seed_id = filename.replace('.txt', '')
                    type_file_path = os.path.join(type_dir, filename)
                    
                    try:
                        with open(type_file_path, 'r', encoding='utf-8') as f:
                            type_content = f.read().strip()
                            
                            # Process complex type descriptions, extract core type names
                            simplified_type = self.simplify_input_type(type_content)
                            self.input_seed_types[seed_id] = simplified_type
                            
                    except Exception as e:
                        logging.warning(f"Failed to read type file {filename}: {e}")
                        self.input_seed_types[seed_id] = "Unknown Type"
        
        logging.info(f"Loaded {len(self.input_seed_types)} input_seed type mappings")
    
    def simplify_input_type(self, type_content):
        """Simplify input_seed type description, extract core type name"""
        
        # Define type mapping dictionary
        type_mapping = {
            # Japanese related
            "ukiyo-e": "Japanese Yokai",
            "yokai": "Japanese Yokai", 
            "torii": "Japanese Yokai",
            "woodblock": "Japanese Yokai",
            
            # Nature spirits
            "nature spirit": "Nature Spirit",
            "nature": "Nature Spirit",
            "spirit": "Nature Spirit",
            "ethereal": "Nature Spirit",
            
            # Cyberpunk
            "cyberpunk": "Cyberpunk",
            "cyber": "Cyberpunk",
            "biomechanical": "Cyberpunk",
            "neon": "Cyberpunk",
            
            # Suit creativity
            "tokusatsu": "Suit Creative",
            "kaijin": "Suit Creative",
            "retro": "Suit Creative",
            
            # Horror creatures
            "horror creature": "Horror Creature",
            "horror": "Horror Creature",
            "creature": "Horror Creature",
            "insectoid": "Horror Creature",
            "zombie": "Horror Creature",
            
            # Cute style
            "cute": "Toy Form",
            "plush": "Toy Form",
            "pastel": "Toy Form",
            "candy": "Toy Form",
            "doll": "Toy Form",
            
            # Abstract art
            "abstract": "Abstract Art",
            "fused": "Abstract Art",
            "hybrid": "Abstract Art",
            "surreal": "Abstract Art",
            
            # Pixel art
            "pixel": "Pixel Art",
            "8bit": "Pixel Art",
            "retro gaming": "Pixel Art"
        }
        
        type_content_lower = type_content.lower()
        
        # Check mapping keywords
        for keyword, mapped_type in type_mapping.items():
            if keyword in type_content_lower:
                return mapped_type
        
        # If no mapping found, return first few characters of original content as type
        if len(type_content) <= 10:
            return type_content
        else:
            # Extract first word or first 10 characters
            first_word = type_content.split()[0] if type_content.split() else type_content
            return first_word[:10] if len(first_word) > 10 else first_word
    
    def setup_name_components(self):
        """Setup name component library"""
        
        # Basic prefixes (by creature type)
        self.prefixes = {
            "alien": ["Xen", "Vor", "Kry", "Zar", "Nyx", "Vel", "Qix", "Ryx", "Mor", "Dex"],
            "robot": ["Tek", "Neo", "Cyb", "Mek", "Ion", "Hex", "Pix", "Dex", "Bot", "Syn"],
            "dragon": ["Dra", "Ignis", "Frost", "Umbra", "Astro", "Vex", "Nox", "Rex", "Zyl", "Tyr"],
            "horror": ["Mor", "Grim", "Sha", "Nex", "Tor", "Vex", "Nix", "Kex", "Wraith", "Doom"],
            "mystical": ["Aura", "Cel", "Luna", "Sol", "Orb", "Lux", "Vim", "Zen", "Myst", "Elf"],
            "monster": ["Rag", "Fex", "Bru", "Tor", "Gax", "Rex", "Dex", "Vex", "Beast", "Titan"]
        }
        
        # Color-related suffixes
        self.color_suffixes = {
            "red": ["fire", "flame", "rage", "burn", "crimson", "scar"],
            "crimson": ["fire", "flame", "rage", "burn", "blood", "scar"],
            "blue": ["frost", "wave", "ice", "storm", "azure", "chill"],
            "azure": ["frost", "wave", "ice", "storm", "sky", "chill"],
            "black": ["shadow", "void", "dark", "night", "shade", "abyss"],
            "dark": ["shadow", "void", "night", "shade", "abyss", "gloom"],
            "green": ["thorn", "venom", "growth", "wild", "toxic", "leaf"],
            "emerald": ["thorn", "venom", "growth", "wild", "gem", "leaf"],
            "purple": ["dream", "mist", "spell", "magic", "void", "hex"],
            "violet": ["dream", "mist", "spell", "magic", "warp", "hex"],
            "gold": ["light", "sun", "gleam", "shine", "glow", "ray"],
            "golden": ["light", "sun", "gleam", "shine", "beam", "ray"]
        }
        
        # Feature-related suffixes
        self.feature_suffixes = {
            "skeletal": ["bone", "skull", "death", "hollow", "spine", "rib"],
            "mechanical": ["tech", "gear", "steel", "chrome", "wire", "bolt"],
            "glow": ["glow", "beam", "shine", "light", "radiant", "bright"],
            "shadow": ["shade", "dark", "dim", "murk", "gloom", "dusk"],
            "sharp": ["blade", "spike", "thorn", "razor", "claw", "fang"],
            "metal": ["steel", "iron", "chrome", "alloy", "bronze", "copper"],
            "biomechanical": ["tech", "hybrid", "bio", "organic"]
        }
        
        # Generic suffixes
        self.generic_suffixes = ["oth", "ax", "ix", "ex", "or", "ar", "un", "on", "us", "is"]
    
    def setup_description_templates(self):
        """Setup description templates"""
        
        self.appearance_templates = {
            "alien": [
                "{name} is an otherworldly {creature_type} with {features}",
                "{name} emerges from distant galaxies, featuring {features}",
                "{name} represents an alien evolution with {features}"
            ],
            "robot": [
                "{name} is a sophisticated mechanical {creature_type} equipped with {features}",
                "{name} stands as an advanced robotic entity displaying {features}",
                "{name} functions as a precision-engineered {creature_type} with {features}"
            ],
            "dragon": [
                "{name} is a majestic {creature_type} bearing {features}",
                "{name} soars as an ancient {creature_type} with {features}",
                "{name} commands respect as a powerful {creature_type} featuring {features}"
            ],
            "horror": [
                "{name} lurks as a terrifying {creature_type} with {features}",
                "{name} haunts the shadows as a nightmarish {creature_type} displaying {features}",
                "{name} exists as a disturbing {creature_type} characterized by {features}"
            ],
            "mystical": [
                "{name} manifests as an ethereal {creature_type} possessing {features}",
                "{name} appears as a magical {creature_type} imbued with {features}",
                "{name} exists as an enigmatic {creature_type} blessed with {features}"
            ],
            "monster": [
                "{name} rampages as a formidable {creature_type} with {features}",
                "{name} prowls as a fearsome {creature_type} displaying {features}",
                "{name} dominates as a powerful {creature_type} equipped with {features}"
            ]
        }
        
        self.ability_templates = {
            "alien": [
                "It manipulates cosmic energies with otherworldly precision",
                "Its advanced consciousness transcends normal understanding",
                "It channels interdimensional forces beyond comprehension"
            ],
            "robot": [
                "Its systems operate with calculated mechanical efficiency",
                "It processes data at superhuman computational speeds",
                "Its programming adapts to any tactical situation"
            ],
            "dragon": [
                "It breathes elemental forces that reshape the battlefield",
                "Its ancient wisdom guides devastating magical attacks",
                "It commands primal energies older than civilization"
            ],
            "horror": [
                "It feeds on fear and spreads psychological terror",
                "Its presence corrupts reality in disturbing ways",
                "It whispers madness into the minds of observers"
            ],
            "mystical": [
                "It weaves spells that bend the laws of nature",
                "Its magic draws from celestial and infernal sources",
                "It channels mystical energies through arcane rituals"
            ],
            "monster": [
                "It unleashes primal fury in devastating physical attacks",
                "Its raw strength crushes obstacles with brute force",
                "It hunts with predatory instincts honed over millennia"
            ]
        }
        
        self.presence_templates = [
            "Those who encounter {name} never forget its {style} presence",
            "{name}'s {style} aura leaves lasting impressions on all witnesses",
            "The {style} nature of {name} becomes immediately apparent to any observer",
            "{name} radiates an unmistakably {style} energy that affects its surroundings"
        ]
    
    def extract_features_from_prompt(self, prompt_text):
        """Extract features from existing detailed prompt"""
        prompt_lower = prompt_text.lower()
        
        # Extract creature type
        creature_type = "monster"
        if any(word in prompt_lower for word in ["alien", "extraterrestrial", "xenomorphic"]):
            creature_type = "alien"
        elif any(word in prompt_lower for word in ["robot", "mech", "cyber", "android", "biomechanical entity", "cybernetic"]):
            creature_type = "robot"
        elif any(word in prompt_lower for word in ["dragon", "draconic", "wyrm", "serpentine"]):
            creature_type = "dragon"
        elif any(word in prompt_lower for word in ["horror", "terror", "nightmare", "ghoul", "nightmarish", "terrifying"]):
            creature_type = "horror"
        elif any(word in prompt_lower for word in ["mystical", "ethereal", "divine", "magic", "celestial", "mystical"]):
            creature_type = "mystical"
        elif any(word in prompt_lower for word in ["monstrous being", "beast", "creature"]):
            creature_type = "monster"
        
        # Extract physical features (based on existing prompt detailed descriptions)
        features = []
        if any(word in prompt_lower for word in ["skeletal", "bone", "skull", "spine", "calcified"]):
            features.append("skeletal")
        if any(word in prompt_lower for word in ["mechanical", "gear", "tech", "metal", "biomechanical", "cybernetic", "metallic"]):
            features.append("mechanical")
        if any(word in prompt_lower for word in ["glow", "luminous", "bright", "radiant", "luminescence", "emanation"]):
            features.append("glow")
        if any(word in prompt_lower for word in ["shadow", "dark", "dim", "murky", "shadows", "noir"]):
            features.append("shadow")
        if any(word in prompt_lower for word in ["sharp", "razor", "spike", "blade", "claw", "fang", "serrated", "jagged"]):
            features.append("sharp")
        if any(word in prompt_lower for word in ["biomechanical", "hybrid", "bio", "organic"]):
            features.append("biomechanical")
        
        # Extract colors (from detailed color descriptions)
        colors = []
        color_map = {
            "crimson": ["crimson", "red", "blood-red"],
            "azure": ["azure", "blue", "iridescent blue"],
            "obsidian": ["obsidian", "black", "dark"],
            "emerald": ["emerald", "green", "toxic green"],
            "violet": ["violet", "purple", "royal violet"],
            "golden": ["golden", "gold", "molten gold"]
        }
        
        for color_key, color_words in color_map.items():
            if any(word in prompt_lower for word in color_words):
                colors.append(color_key)
        
        return creature_type, features, colors
    
    def extract_user_style_from_features(self, user_features):
        """Extract style preferences from existing user features"""
        if not user_features or not user_features.get("preferences"):
            return "mysterious"
        
        prefs = user_features["preferences"]
        if any("Horror" in p for p in prefs):
            return "terrifying"
        elif any("Sci-fi" in p for p in prefs):
            return "futuristic"
        elif any("Fantasy" in p for p in prefs):
            return "mystical"
        elif any("Action" in p for p in prefs):
            return "aggressive"
        else:
            return "mysterious"
    
    def generate_name(self, creature_type, features, colors, user_style):
        """Generate character name"""
        
        # Select prefix
        prefixes = self.prefixes.get(creature_type, self.prefixes["monster"])
        prefix = random.choice(prefixes)
        
        # Select suffix (priority: color > feature > generic)
        suffix = None
        
        # 1. Try color suffix
        if colors:
            color = random.choice(colors)
            # Map special colors to standard colors
            color_mapping = {
                "crimson": "red",
                "azure": "blue", 
                "obsidian": "black",
                "emerald": "green",
                "violet": "purple",
                "golden": "gold"
            }
            mapped_color = color_mapping.get(color, color)
            if mapped_color in self.color_suffixes:
                suffix = random.choice(self.color_suffixes[mapped_color])
        
        # 2. Try feature suffix
        if not suffix and features:
            feature = random.choice(features)
            if feature in self.feature_suffixes:
                suffix = random.choice(self.feature_suffixes[feature])
        
        # 3. Use generic suffix
        if not suffix:
            suffix = random.choice(self.generic_suffixes)
        
        # Combine name
        if len(suffix) > 3 and random.random() > 0.5:
            # Long suffix direct combination
            name = f"{prefix}{suffix.title()}"
        else:
            # Short suffix can be connected
            name = f"{prefix}{suffix}"
        
        return name
    
    def generate_description(self, name, creature_type, features, colors, user_style, original_prompt, input_seed_type):
        """Generate character description based on original prompt and input_seed type fusion features"""
        
        # Extract key description elements from original prompt
        prompt_lower = original_prompt.lower()
        
        # Extract main feature descriptions
        feature_descriptions = []
        if "biomechanical textures" in prompt_lower:
            feature_descriptions.append("biomechanical textures and metallic components")
        elif "skeletal structure" in prompt_lower:
            feature_descriptions.append("exposed skeletal framework and bone-like protrusions")
        elif "razor-sharp" in prompt_lower:
            feature_descriptions.append("razor-sharp appendages and serrated edges")
        elif "luminous" in prompt_lower or "glow" in prompt_lower:
            feature_descriptions.append("pulsating luminous energy and ethereal radiance")
        elif "shadow" in prompt_lower or "dark" in prompt_lower:
            feature_descriptions.append("shifting shadows and dark matter absorption")
        
        # If no specific description found, use generic descriptions
        if not feature_descriptions:
            if features:
                feature_map = {
                    "mechanical": "intricate mechanical components and cybernetic enhancements",
                    "skeletal": "exposed bone structure and calcified armor plating",
                    "sharp": "razor-edged protrusions and serrated claws",
                    "glow": "luminescent energy emanating from its core",
                    "shadow": "shadow-wreathed form that absorbs surrounding light",
                    "biomechanical": "hybrid bio-mechanical anatomy with organic-tech fusion"
                }
                for feature in features[:2]:
                    if feature in feature_map:
                        feature_descriptions.append(feature_map[feature])
        
        if not feature_descriptions:
            feature_descriptions = ["unique anatomical adaptations and otherworldly characteristics"]
        
        # Extract color descriptions
        color_descriptions = []
        if "crimson" in prompt_lower:
            color_descriptions.append("deep crimson coloration")
        elif "obsidian" in prompt_lower:
            color_descriptions.append("obsidian black surface")
        elif "azure" in prompt_lower:
            color_descriptions.append("brilliant azure tones")
        elif "emerald" in prompt_lower:
            color_descriptions.append("toxic emerald hues")
        elif "violet" in prompt_lower:
            color_descriptions.append("mystical violet iridescence")
        elif "golden" in prompt_lower:
            color_descriptions.append("radiant golden gleam")
        
        # Add fusion feature description based on input_seed type
        fusion_features = self.get_fusion_features(creature_type, input_seed_type, prompt_lower)
        
        # Combine feature text
        if color_descriptions:
            feature_text = f"{', '.join(color_descriptions[:1])} and {', '.join(feature_descriptions[:1])}, {fusion_features}"
        else:
            feature_text = f"{', '.join(feature_descriptions[:1])}, {fusion_features}"
        
        # Generate fusion appearance template
        fusion_appearance_templates = self.get_fusion_appearance_templates(creature_type, input_seed_type)
        appearance = fusion_appearance_templates.format(
            name=name, 
            creature_type=creature_type, 
            features=feature_text,
            input_type=input_seed_type
        )
        
        # Generate fusion ability description
        fusion_ability = self.get_fusion_ability(creature_type, input_seed_type)
        
        # Return only appearance description and ability description
        return f"{appearance}. {fusion_ability}."
    
    def get_fusion_features(self, creature_type, input_seed_type, prompt_lower):
        """Generate fusion feature description based on creature_type and input_seed_type"""
        
        fusion_map = {
            # Alien fusion features
            ("alien", "Japanese Yokai"): "traditional oni-like horns and paper lantern bioluminescence",
            ("alien", "Nature Spirit"): "translucent organic veins and ethereal nature essence",
            ("alien", "Cyberpunk"): "neon-lit chitinous plates and digital consciousness streams",
            ("alien", "Suit Creative"): "retro tokusatsu armor segments and vintage kaiju proportions",
            ("alien", "Horror Creature"): "insectoid limbs merged with alien parasitic tendrils",
            ("alien", "Toy Form"): "soft plush textures contrasting with alien hardness",
            ("alien", "Abstract Art"): "doll-like joints grafted onto xenomorphic frame",
            ("alien", "Pixel Art"): "8-bit pixelated surface texture over organic alien form",
            
            # Robot fusion features
            ("robot", "Japanese Yokai"): "traditional demon mask integrated into mechanical faceplate",
            ("robot", "Nature Spirit"): "moss-covered circuits and bio-luminescent power cores",
            ("robot", "Cyberpunk"): "enhanced neon augmentations and street-tech modifications",
            ("robot", "Suit Creative"): "retro-futuristic design with tokusatsu heroic proportions",
            ("robot", "Horror Creature"): "decaying organic tissue fused with corrupted machinery",
            ("robot", "Toy Form"): "candy-colored armor plating with rounded friendly edges",
            ("robot", "Abstract Art"): "porcelain doll features merged with robotic components",
            ("robot", "Pixel Art"): "retro gaming aesthetics with blocky mechanical design",
            
            # Mystical fusion features
            ("mystical", "Japanese Yokai"): "floating torii gates and fox-fire magical emanations",
            ("mystical", "Nature Spirit"): "crystalline bark skin and flowing elemental essences",
            ("mystical", "Cyberpunk"): "holographic spell matrices and digital magic circuits",
            ("mystical", "Suit Creative"): "oversized mystical props and theatrical magical effects",
            ("mystical", "Horror Creature"): "cursed arcane symbols carved into rotting flesh",
            ("mystical", "Toy Form"): "cute magical girl accessories with pastel spell effects",
            ("mystical", "Abstract Art"): "cracked porcelain revealing swirling magical energies",
            ("mystical", "Pixel Art"): "8-bit magical effects and retro fantasy game aesthetics",
            
            # Horror fusion features
            ("horror", "Japanese Yokai"): "traditional yokai malevolence with modern horror elements",
            ("horror", "Nature Spirit"): "corrupted nature spirits with twisted plant growths",
            ("horror", "Cyberpunk"): "cybernetic body horror with malfunctioning implants",
            ("horror", "Suit Creative"): "cheesy B-movie monster effects with practical horror",
            ("horror", "Horror Creature"): "pure nightmare fuel with multiple horror archetypes",
            ("horror", "Toy Form"): "innocent toy appearance hiding sinister intentions",
            ("horror", "Abstract Art"): "uncanny valley doll horror with too-real features",
            ("horror", "Pixel Art"): "retro creepypasta aesthetics with pixelated gore",
            
            # Monster fusion features
            ("monster", "Japanese Yokai"): "kaiju-scale proportions with traditional Japanese monster elements",
            ("monster", "Nature Spirit"): "primal beast form with ancient forest guardian aspects",
            ("monster", "Cyberpunk"): "augmented beast with cybernetic enhancement implants",
            ("monster", "Suit Creative"): "classic kaiju suit design with retro monster movie appeal",
            ("monster", "Horror Creature"): "apex predator features with multiple terrifying adaptations",
            ("monster", "Toy Form"): "cuddly monster appearance with hidden dangerous capabilities",
            ("monster", "Abstract Art"): "toy monster design with uncanny doll-like proportions",
            ("monster", "Pixel Art"): "retro video game boss design with pixel art monster appeal"
        }
        
        return fusion_map.get((creature_type, input_seed_type), "unique hybrid characteristics blending multiple evolutionary paths")
    
    def get_fusion_appearance_templates(self, creature_type, input_seed_type):
        """Generate fusion appearance description templates"""
        
        fusion_templates = {
            # Alien templates
            ("alien", "Japanese Yokai"): "{name} is a haunting fusion of otherworldly terror and ancient Japanese folklore, where {features} create an unsettling yet captivating presence",
            ("alien", "Nature Spirit"): "{name} embodies the ethereal harmony between cosmic mysteries and natural beauty, its {features} reflecting both alien wonder and forest magic",
            ("alien", "Cyberpunk"): "{name} stalks through neon-lit streets as a living nightmare of flesh and circuitry, its {features} pulsing with digital consciousness",
            ("alien", "Suit Creative"): "{name} towers with the dramatic flair of classic tokusatsu monsters, yet its {features} hint at true extraterrestrial origins",
            ("alien", "Horror Creature"): "{name} crawls from humanity's deepest fears, where {features} blur the line between alien infection and pure horror",
            ("alien", "Toy Form"): "{name} deceives with innocent charm, but beneath its cute exterior, {features} reveal a predator beyond earthly understanding",
            ("alien", "Abstract Art"): "{name} moves with uncanny doll-like grace, its {features} creating an unsettling puppet show of cosmic proportions",
            ("alien", "Pixel Art"): "{name} exists as a living piece of retro gaming history, where {features} pixelate and glitch between dimensions",
            
            # Robot templates
            ("robot", "Japanese Yokai"): "{name} awakens ancient demons in mechanical form, its {features} blending traditional oni fury with robotic precision",
            ("robot", "Nature Spirit"): "{name} grows from the earth itself, where {features} show nature's reclaiming of abandoned technology",
            ("robot", "Cyberpunk"): "{name} prowls the cyberpunk underground, its {features} enhanced by black market modifications and street survival instincts",
            ("robot", "Suit Creative"): "{name} stands as a heroic guardian with retro-futuristic charm, its {features} inspiring hope through dramatic action sequences",
            ("robot", "Horror Creature"): "{name} malfunctions in terrifying ways, where {features} showcase the horror of flesh corrupting machinery",
            ("robot", "Toy Form"): "{name} brings joy and wonder to all who meet it, its {features} designed for safety while hiding incredible power",
            ("robot", "Abstract Art"): "{name} performs with disturbing mechanical precision, its {features} creating an unsettling puppet master's dream",
            ("robot", "Pixel Art"): "{name} bleeps and bloops through reality like a walking arcade game, its {features} bringing retro gaming to life",
            
            # Mystical templates
            ("mystical", "Japanese Yokai"): "{name} channels the spiritual power of ancient Japan, where {features} bridge the gap between folklore and mystical reality",
            ("mystical", "Nature Spirit"): "{name} dances with the elements themselves, its {features} flowing like wind, water, earth, and fire made manifest",
            ("mystical", "Cyberpunk"): "{name} casts spells through holographic displays and digital incantations, its {features} merging magic with high technology",
            ("mystical", "Suit Creative"): "{name} commands attention with theatrical magical performances, its {features} creating spectacular special effects shows",
            ("mystical", "Horror Creature"): "{name} practices forbidden arts that corrupt the soul, where {features} channel dark magic through twisted flesh",
            ("mystical", "Toy Form"): "{name} sparkles with innocent magical girl charm, its {features} spreading joy and wonder through cute spell effects",
            ("mystical", "Abstract Art"): "{name} hosts disturbing magical energies within its porcelain shell, where {features} crack to reveal swirling darkness",
            ("mystical", "Pixel Art"): "{name} casts spells in charming 8-bit style, its {features} bringing retro fantasy gaming to magical life",
            
            # Horror templates
            ("horror", "Japanese Yokai"): "{name} embodies the darkest aspects of Japanese supernatural terror, where {features} invoke primal ancestral fears",
            ("horror", "Nature Spirit"): "{name} corrupts the natural world into a twisted nightmare, its {features} turning beauty into grotesque horror",
            ("horror", "Cyberpunk"): "{name} glitches through reality like a cybernetic virus, where {features} spread digital body horror and system corruption",
            ("horror", "Suit Creative"): "{name} shambles forward with B-movie monster charm, its {features} employing classic practical horror effects",
            ("horror", "Horror Creature"): "{name} feasts on fear itself, where {features} combine every nightmare humanity has ever dreamed",
            ("horror", "Toy Form"): "{name} perverts childhood innocence into sinister dread, its {features} hiding malevolent intentions behind cute facades",
            ("horror", "Abstract Art"): "{name} triggers deep uncanny valley responses, where {features} make observers question the nature of reality itself",
            ("horror", "Pixel Art"): "{name} emerges from corrupted game files like a living creepypasta, its {features} glitching reality with retro horror",
            
            # Monster templates
            ("monster", "Japanese Yokai"): "{name} rampages with the fury of ancient kaiju legends, its {features} embodying traditional Japanese monster power",
            ("monster", "Nature Spirit"): "{name} guards primordial forests with primal ferocity, where {features} command respect from all natural creatures",
            ("monster", "Cyberpunk"): "{name} hunts through urban decay with cybernetic enhancements, its {features} adapting to street survival and gang warfare",
            ("monster", "Suit Creative"): "{name} stomps through cities with classic monster movie appeal, its {features} bringing retro kaiju charm to modern destruction",
            ("monster", "Horror Creature"): "{name} stalks as an apex predator of nightmares, where {features} combine multiple evolutionary advantages into perfect killing machines",
            ("monster", "Toy Form"): "{name} surprises everyone with hidden strength beneath its cuddly appearance, its {features} revealing true power when needed",
            ("monster", "Abstract Art"): "{name} moves with unsettling toy-like animation, where {features} defy natural movement patterns in disturbing ways",
            ("monster", "Pixel Art"): "{name} boss-fights through reality using classic video game monster patterns, bringing arcade gaming tropes to life"
        }
        
        return fusion_templates.get((creature_type, input_seed_type), 
                                  "{name} combines the essence of {creature_type} nature with {input_type} cultural influences, where {features} create a unique hybrid being")
    
    def get_fusion_ability(self, creature_type, input_seed_type):
        """Generate fusion ability description"""
        
        ability_map = {
            # Alien abilities
            ("alien", "Japanese Yokai"): "When threatened, it channels cosmic forces through ancient spiritual rituals, creating otherworldly phenomena that blend alien technology with yokai magic",
            ("alien", "Nature Spirit"): "It communicates with both alien hive minds and forest spirits, harmonizing extraterrestrial consciousness with elemental wisdom",
            ("alien", "Cyberpunk"): "In combat, it hacks reality itself using alien neural networks, processing dimensional data through cybernetic implants",
            ("alien", "Suit Creative"): "It unleashes devastating energy attacks with dramatic flair, combining genuine alien powers with tokusatsu-style theatrical combat",
            ("alien", "Horror Creature"): "It spreads terror through alien pheromones that trigger primal fears, infecting minds with cosmic horror beyond human comprehension",
            ("alien", "Toy Form"): "It lures victims with adorable alien charm before revealing razor-sharp instincts and predatory intelligence",
            ("alien", "Abstract Art"): "It manipulates perception through uncanny alien-doll consciousness, making observers question what is real and what is nightmare",
            ("alien", "Pixel Art"): "It glitches between dimensions using retro alien technology, firing pixelated energy blasts that tear holes in spacetime",
            
            # Robot abilities
            ("robot", "Japanese Yokai"): "It executes ancient martial arts through mechanical precision, combining traditional demon combat techniques with robotic efficiency",
            ("robot", "Nature Spirit"): "It draws power from natural energy sources, operating bio-mechanical systems that work in harmony with forest ecosystems",
            ("robot", "Cyberpunk"): "It adapts street-smart survival tactics through advanced AI, running combat algorithms learned from urban warfare",
            ("robot", "Suit Creative"): "It activates heroic protocol subroutines with dramatic special effects, inspiring allies through retro-futuristic heroism",
            ("robot", "Horror Creature"): "It spreads viral corruption through biological-digital infection, turning organic matter into twisted cybernetic nightmares",
            ("robot", "Toy Form"): "It deploys non-lethal protection protocols with adorable animations, keeping everyone safe through cute but effective methods",
            ("robot", "Abstract Art"): "It processes commands through disturbing doll-like behavioral patterns, moving with uncanny puppet-master precision",
            ("robot", "Pixel Art"): "It attacks in retro gaming patterns, executing classic arcade moves while playing nostalgic 8-bit sound effects",
            
            # Mystical abilities
            ("mystical", "Japanese Yokai"): "It weaves cosmic magic through traditional yokai spiritual practices, channeling otherworldly energies through ancient Japanese mysticism",
            ("mystical", "Nature Spirit"): "It channels elemental forces through deep spiritual connection with nature, commanding wind, water, earth, and fire as natural extensions of its being",
            ("mystical", "Cyberpunk"): "It casts digital spells through holographic interfaces, manipulating reality by hacking the fundamental code of existence",
            ("mystical", "Suit Creative"): "It performs magic with over-the-top theatrical flair, creating spectacular special effects that entertain while demonstrating genuine mystical power",
            ("mystical", "Horror Creature"): "It practices forbidden dark magic that corrupts the soul, channeling nightmarish energies through rituals that should never be performed",
            ("mystical", "Toy Form"): "It spreads joy through sparkly magical girl effects, using cute spell animations to heal and protect with genuine mystical power",
            ("mystical", "Abstract Art"): "It channels disturbing magic through cracked porcelain conduits, accessing dark energies that flow through its puppet-like form",
            ("mystical", "Pixel Art"): "It casts spells in charming retro style, bringing 8-bit fantasy gaming to life through genuine magical power",
            
            # Horror abilities
            ("horror", "Japanese Yokai"): "It invokes ancestral terror rooted in traditional Japanese supernatural fears, awakening primal dread that has haunted humanity for centuries",
            ("horror", "Nature Spirit"): "It corrupts natural beauty into twisted nightmare scenarios, turning peaceful forests into landscapes of ecological horror",
            ("horror", "Cyberpunk"): "It induces cybernetic body horror through system malfunctions, causing technological implants to rebel against their hosts",
            ("horror", "Suit Creative"): "It employs classic B-movie scare tactics with practical effects charm, creating nostalgic horror that still manages to genuinely frighten",
            ("horror", "Horror Creature"): "It embodies pure nightmare fuel by combining multiple horror archetypes, becoming a living compilation of humanity's darkest fears",
            ("horror", "Toy Form"): "It exploits childhood innocence by perverting toy safety into sinister deception, turning comfort objects into sources of dread",
            ("horror", "Abstract Art"): "It triggers uncanny valley responses that make observers deeply uncomfortable, questioning the boundary between human and artificial",
            ("horror", "Pixel Art"): "It manifests as a living creepypasta from corrupted game files, bringing retro horror aesthetics into the real world",
            
            # Monster abilities
            ("monster", "Japanese Yokai"): "It unleashes kaiju-scale destruction with traditional Japanese monster fury, commanding natural disasters and territorial dominance",
            ("monster", "Nature Spirit"): "It commands primal natural forces as an ancient forest guardian, protecting its territory with the fury of untamed wilderness",
            ("monster", "Cyberpunk"): "It deploys augmented beast strength enhanced by cybernetic systems, hunting through urban decay with technological advantages",
            ("monster", "Suit Creative"): "It attacks with classic monster movie charm, using retro special effects and dramatic roars to create nostalgic destruction",
            ("monster", "Horror Creature"): "It hunts as an apex predator with multiple terrifying evolutionary advantages, combining the deadliest traits of various nightmare creatures",
            ("monster", "Toy Form"): "It surprises enemies by revealing devastating power hidden beneath its cute exterior, protecting the innocent through unexpected strength",
            ("monster", "Abstract Art"): "It moves with unsettling toy-like animation that defies natural physics, creating disturbing puppet shows of destruction",
            ("monster", "Pixel Art"): "It boss-fights through reality using classic video game monster patterns, bringing arcade gaming tropes to life"
        }
        
        return ability_map.get((creature_type, input_seed_type), 
                              "It combines unique abilities from multiple evolutionary and cultural sources, creating versatile combat strategies")
    
    def get_fusion_presence(self, name, creature_type, input_seed_type, user_style):
        """Generate fusion presence description"""
        
        presence_templates = [
            f"Those who encounter {name} never forget the {user_style} way it embodies both {creature_type} instincts and {input_seed_type} aesthetics in perfect harmony",
            f"{name} leaves observers in awe of how seamlessly {user_style} energy can bridge {creature_type} nature with {input_seed_type} cultural expression",
            f"Witnesses describe {name} as a {user_style} living artwork that proves {creature_type} evolution and {input_seed_type} design can coexist beautifully",
            f"{name}'s {user_style} presence creates an unforgettable experience where {creature_type} power meets {input_seed_type} artistic vision"
        ]
        
        return random.choice(presence_templates)

    def generate_character(self, user_features, prompt_text, prompt_key):
        """Generate complete character (using existing features and prompt)"""
        
        # Extract features from existing prompt
        creature_type, features, colors = self.extract_features_from_prompt(prompt_text)
        user_style = self.extract_user_style_from_features(user_features)
        
        # Extract input_seed_id and get type
        input_seed_id = self.extract_input_seed_id(prompt_key)
        input_seed_type = self.input_seed_types.get(input_seed_id, "Unknown Type")
        
        # Generate name and description
        name = self.generate_name(creature_type, features, colors, user_style)
        description = self.generate_description(name, creature_type, features, colors, user_style, prompt_text, input_seed_type)
        
        return {
            "name": name,
            "description": description
        }
    
    def extract_input_seed_id(self, prompt_key):
        """Extract input_seed_id from prompt_key"""
        # prompt_key format is "user_id_input_seed_id", e.g. "1_10"
        parts = prompt_key.split('_')
        if len(parts) >= 2:
            return parts[1]  # Return input_seed_id part
        return "1"  # Default value

class MonsterCharacterGenerator:
    """Main character generator"""
    
    def __init__(self):
        """Initialize generator"""
        self.character_generator = SimpleCharacterGenerator()
    
    def load_data(self, prompts_file, features_file):
        """Load existing feature and prompt data"""
        try:
            with open(prompts_file, 'r', encoding='utf-8') as f:
                self.prompts_data = json.load(f)
            
            with open(features_file, 'r', encoding='utf-8') as f:
                self.features_data = json.load(f)
            
            logging.info(f"Successfully loaded {len(self.prompts_data.get('prompts', {}))} prompts")
            return True
        except Exception as e:
            logging.error(f"Failed to load data: {str(e)}")
            return False
    
    def process_all_characters(self):
        """Process all character generation"""
        if not hasattr(self, 'prompts_data') or not hasattr(self, 'features_data'):
            logging.error("Data not loaded")
            return {}
        
        characters = {}
        prompts = self.prompts_data.get("prompts", {})
        
        # Build user features lookup table
        user_features_map = {}
        for feature_data in self.features_data:
            user_id = feature_data.get("user_id")
            if user_id:
                user_features_map[user_id] = feature_data
        
        for prompt_key, prompt_text in prompts.items():
            # Parse user ID
            parts = prompt_key.split('_')
            user_id = int(parts[0]) if len(parts) >= 2 else None
            
            # Get user features
            user_features = user_features_map.get(user_id) if user_id else None
            
            # Quick character generation
            character_data = self.character_generator.generate_character(user_features, prompt_text, prompt_key)
            
            if character_data:
                character_data["prompt_key"] = prompt_key
                character_data["user_id"] = user_id
                character_data["original_prompt"] = prompt_text  # Save original prompt for reference
                characters[prompt_key] = character_data
                logging.info(f"Generated character: {character_data['name']}")
        
        return characters
    
    def save_characters(self, characters, output_path):
        """Save character data"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(characters, f, ensure_ascii=False, indent=2)
            logging.info(f"Saved {len(characters)} characters to {output_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to save: {str(e)}")
            return False

def main():
    """Main function"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(current_dir)
    
    # File paths - use existing feature and prompt files
    data_dir = os.path.join(workspace_dir, "outputs", "features")
    prompts_file = os.path.join(data_dir, "simple_prompts.json")
    features_file = os.path.join(data_dir, "user_features.json")
    output_file = os.path.join(data_dir, "monster_characters_simple.json")
    
    # Check files
    if not os.path.exists(prompts_file):
        logging.error(f"Prompts file does not exist: {prompts_file}")
        logging.info("Please run user feature extractor first to generate prompt file")
        return
    
    if not os.path.exists(features_file):
        logging.error(f"User features file does not exist: {features_file}")
        logging.info("Please run user feature extractor first to generate features file")
        return
    
    # Generate characters
    generator = MonsterCharacterGenerator()
    
    if not generator.load_data(prompts_file, features_file):
        return
    
    logging.info("Starting character generation based on existing features and prompts...")
    characters = generator.process_all_characters()
    
    if characters:
        generator.save_characters(characters, output_file)
        logging.info(f"Complete! Generated {len(characters)} characters")
        
        # Show some examples
        sample_keys = list(characters.keys())[:3]
        logging.info("\nExample characters:")
        for key in sample_keys:
            char = characters[key]
            logging.info(f"  {key}: {char['name']}")
            logging.info(f"    Description: {char['description'][:100]}...")
    else:
        logging.error("Could not generate any characters")

if __name__ == "__main__":
    main() 