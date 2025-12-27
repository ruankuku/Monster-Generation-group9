"""
Keyword Mapping Library - Used to map user preference keywords to visual features
"""

# Movie/game type keyword mapping to visual and conceptual features
MOVIE_GAME_KEYWORD_MAPPING = {
    'Science Fiction': ['futuristic', 'technological', 'alien', 'space', 'advanced'],
    'Thriller': ['suspenseful', 'mysterious', 'tense', 'dark', 'psychological'],
    'Cyberpunk': ['neon', 'dystopian', 'technological', 'urban', 'digital', 'hacker'],
    'Future City': ['urban', 'technological', 'futuristic', 'metallic', 'neon'],
    'Artificial Intelligence': ['digital', 'technological', 'robotic', 'synthetic', 'intelligent'],
    'Nordic Mythology': ['ancient', 'mystical', 'mythological', 'runic', 'viking'],
    'Polar Adventure': ['icy', 'cold', 'stark', 'desolate', 'survival'],
    'Unknown Ecology': ['alien', 'mysterious', 'organic', 'evolving', 'environmental'],
    'Backroom': ['liminal', 'uncanny', 'isolated', 'surreal', 'empty'],
    'Creepy': ['disturbing', 'unsettling', 'eerie', 'dark', 'shadowy'],
    'Psychedelic': ['vibrant', 'colorful', 'surreal', 'distorted', 'hallucinatory'],
    'Dystopia': ['grim', 'bleak', 'decaying', 'oppressive', 'apocalyptic'],
    'Experimental': ['abstract', 'unconventional', 'artistic', 'avant-garde', 'innovative'],
    'Gothic': ['dark', 'gloomy', 'macabre', 'ancient', 'mysterious'],
    'Horror': ['frightening', 'disturbing', 'macabre', 'violent', 'terrifying'],
    'Anti-Utopia': ['dystopian', 'oppressive', 'controlled', 'rebellious', 'systematic'],
    'Philosophy': ['conceptual', 'thought-provoking', 'abstract', 'intellectual', 'existential'],
    'Monster vs. Monster': ['battling', 'fierce', 'powerful', 'monstrous', 'violent'],
    'Pixel Indie': ['retro', 'pixelated', '8-bit', 'nostalgic', 'simplistic'],
    'JRPG': ['fantasy', 'anime-styled', 'heroic', 'quest-based', 'colorful'],
    'Teen Battle': ['energetic', 'youthful', 'action-packed', 'dramatic', 'vibrant'],
    'Marvel': ['superheroic', 'colorful', 'action-packed', 'larger-than-life', 'powerful'],
    'Superheroism': ['heroic', 'powerful', 'iconic', 'moral', 'extraordinary'],
    'A24': ['artistic', 'indie', 'atmospheric', 'unconventional', 'thoughtful'],
    'David Lynch': ['surreal', 'dreamlike', 'disturbing', 'mysterious', 'uncanny']
}

# Character type keyword mapping
CHARACTER_KEYWORD_MAPPING = {
    'Alien': ['extraterrestrial', 'otherworldly', 'mysterious', 'biological'],
    'Extraterrestrial': ['alien', 'cosmic', 'strange', 'unearthly'],
    'Mecha': ['mechanical', 'robotic', 'technological', 'armored', 'weaponized'],
    'Hacker': ['digital', 'cybernetic', 'connected', 'technological'],
    'Heptapod': ['tentacled', 'complex', 'mysterious', 'communicative'],
    'Dystopian Combo': ['hybrid', 'mutated', 'combined', 'chimeric'],
    'Bluntman': ['blunt', 'direct', 'simple', 'powerful'],
    'Lynchian monster': ['surreal', 'disturbing', 'nightmarish', 'symbolic'],
    'Clowns': ['grotesque', 'painted', 'performative', 'exaggerated'],
    'Geometric constructs': ['geometric', 'constructed', 'abstract', 'mathematical'],
    'Giant Creatures': ['massive', 'imposing', 'powerful', 'destructive'],
    'Violent Monsters': ['aggressive', 'dangerous', 'threatening', 'predatory'],
    'Mimetic Mutants': ['mimicking', 'evolving', 'transforming', 'adaptable'],
    'Summoned Beasts': ['magical', 'controlled', 'mystical', 'obedient'],
    'Mecha Dragons': ['mechanical', 'draconic', 'powerful', 'technological'],
    'Anthropomorphic Gods': ['human-like', 'divine', 'powerful', 'mythological'],
    'Iron Man': ['armored', 'technological', 'sleek', 'weaponized'],
    'Spider Man': ['agile', 'web-like', 'masked', 'flexible']
}

# Color keyword mapping
COLOR_KEYWORD_MAPPING = {
    'Dark': ['shadowy', 'dim', 'murky', 'obscure'],
    'Black & White': ['monochrome', 'stark', 'contrasting', 'binary'],
    'Fluorescent': ['glowing', 'vibrant', 'bright', 'neon'],
    'Silver': ['metallic', 'reflective', 'shiny', 'sleek'],
    'Metallic': ['metal-like', 'shiny', 'hard', 'reflective'],
    'Grey blue': ['cool', 'muted', 'calm', 'subdued'],
    'Snow white': ['pure', 'pristine', 'bright', 'clean'],
    'Colourful': ['vibrant', 'varied', 'saturated', 'lively'],
    'Vintage': ['aged', 'retro', 'nostalgic', 'classic'],
    'Blood red': ['intense', 'crimson', 'violent', 'rich'],
    'Low saturation': ['muted', 'subtle', 'understated', 'desaturated']
}

# Visual style keyword mapping
STYLE_KEYWORD_MAPPING = {
    'Dystopian': ['post-apocalyptic', 'bleak', 'decaying', 'oppressive'],
    'Dark': ['shadowy', 'gloomy', 'obscured', 'moody'],
    'Satirical': ['ironic', 'mocking', 'exaggerated', 'critical'],
    'Horror': ['frightening', 'disturbing', 'unsettling', 'macabre'],
    'Mechanical': ['technological', 'engineered', 'constructed', 'industrial'],
    'Futuristic': ['advanced', 'sci-fi', 'technological', 'forward-looking'],
    'Sense of light and shadow': ['contrasted', 'dramatic', 'chiaroscuro', 'moody'],
    'Texture': ['tactile', 'detailed', 'surface-oriented', 'material'],
    'Detachment': ['isolated', 'distant', 'removed', 'disconnected'],
    'Absurd': ['illogical', 'nonsensical', 'bizarre', 'irrational'],
    'Abstract': ['non-representational', 'conceptual', 'non-literal', 'symbolic'],
    'Strange': ['unusual', 'odd', 'peculiar', 'unfamiliar'],
    'Surrealmemes': ['dreamlike', 'bizarre', 'subconscious', 'illogical'],
    'Visual art': ['artistic', 'aesthetic', 'composed', 'designed'],
    'Cult classic': ['iconic', 'niche', 'underground', 'distinctive'],
    'Fantasy': ['magical', 'otherworldly', 'imaginative', 'mythical'],
    'Gothic': ['gloomy', 'ornate', 'medieval', 'mysterious'],
    'Decadent': ['luxurious', 'excessive', 'indulgent', 'deteriorating'],
    'Minimalist': ['simple', 'clean', 'essential', 'uncluttered'],
    'Industrial': ['mechanical', 'factory-like', 'utilitarian', 'manufactured'],
    'Visual Deconstruction': ['fragmented', 'deconstructed', 'disassembled', 'analytical'],
    'Counter Narrative': ['subversive', 'challenging', 'alternative', 'unconventional'],
    'Retro Pixel': ['8-bit', 'pixelated', 'nostalgic', 'low-resolution'],
    'Vibrant': ['colorful', 'energetic', 'intense', 'lively'],
    'Visual Impact': ['striking', 'bold', 'attention-grabbing', 'memorable'],
    'Arcade Style': ['game-like', 'digital', 'colorful', 'animated'],
    'Gorgeous': ['beautiful', 'elaborate', 'stunning', 'visually-rich'],
    'Technological': ['high-tech', 'digital', 'futuristic', 'modern'],
    'Metallic armour': ['protective', 'shiny', 'hard', 'defensive'],
    'Symmetrical beauty': ['balanced', 'proportioned', 'harmonious', 'ordered'],
    'Realistic style': ['lifelike', 'detailed', 'natural', 'accurate'],
    'Metallic machinery': ['mechanical', 'engineered', 'industrial', 'complex']
}

# Image element keyword mapping - Used for image feature analysis
IMAGE_ELEMENT_MAPPING = {
    # Morphological elements
    'alien': ['extraterrestrial', 'otherworldly', 'unusual anatomy', 'non-human'],
    'tentacles': ['tentacled', 'cephalopod-like', 'writhing', 'grasping'],
    'mechanical': ['robotic', 'artificial', 'constructed', 'engineered'],
    'organic': ['biological', 'living', 'flesh-like', 'natural'],
    'humanoid': ['human-like', 'anthropomorphic', 'bipedal', 'human features'],
    'insectoid': ['insect-like', 'chitinous', 'multi-limbed', 'compound eyes'],
    'reptilian': ['scaly', 'serpentine', 'cold-blooded', 'reptile-like'],
    'amorphous': ['shapeless', 'fluid', 'changing', 'undefined'],
    'crystalline': ['crystal-like', 'faceted', 'geometric', 'translucent'],
    'aquatic': ['water-dwelling', 'fish-like', 'marine', 'amphibious'],
    
    # Material elements
    'metallic': ['metal', 'reflective', 'hard', 'manufactured'],
    'slimy': ['mucous', 'wet', 'glistening', 'viscous'],
    'rocky': ['stone-like', 'hard', 'mineral', 'rough'],
    'gaseous': ['vapor', 'ethereal', 'misty', 'smoke-like'],
    'liquid': ['fluid', 'flowing', 'watery', 'non-solid'],
    'skeletal': ['bone-like', 'exposed bones', 'ribcage', 'skull features'],
    'chitinous': ['exoskeleton', 'hard shell', 'armored', 'carapace'],
    'bioluminescent': ['glowing', 'self-illuminating', 'light-emitting', 'phosphorescent'],
    
    # Special features
    'multi-eyed': ['many eyes', 'compound eyes', 'eye clusters', 'omnidirectional vision'],
    'multi-limbed': ['many arms', 'many legs', 'appendages', 'tentacular'],
    'winged': ['flying', 'feathered', 'aerial', 'bat-like wings'],
    'horned': ['antlered', 'spiked', 'protruding horns', 'horn-crowned'],
    'fanged': ['sharp teeth', 'predatory', 'vampire-like', 'carnivorous'],
    'clawed': ['taloned', 'sharp claws', 'predatory', 'rending'],
    'segmented': ['sectioned', 'multi-part', 'modular', 'divided body'],
    'asymmetrical': ['uneven', 'unbalanced', 'irregular', 'lopsided'],
    
    # Hybrid/composite features
    'cyborg': ['part-machine', 'part-organic', 'technological implants', 'enhanced'],
    'chimera': ['hybrid', 'combined creatures', 'multiple species', 'composite'],
    'elemental': ['embodying elements', 'primal force', 'natural power', 'elemental energy'],
    'dimensional': ['reality-warping', 'space-bending', 'interdimensional', 'non-euclidean'],
    'parasitic': ['host-dependent', 'invasive', 'symbiotic', 'consuming'],
    'spectral': ['ghost-like', 'ethereal', 'translucent', 'spiritual'],
    'demonic': ['hellish', 'infernal', 'devilish', 'malevolent'],
    'angelic': ['divine', 'heavenly', 'radiant', 'winged humanoid'],
    
    # Visual effects
    'glowing': ['luminous', 'radiant', 'neon', 'light-emitting'],
    'shadowy': ['dark', 'umbral', 'obscured', 'shrouded'],
    'iridescent': ['rainbow-colored', 'pearlescent', 'color-shifting', 'opalescent'],
    'translucent': ['see-through', 'transparent', 'clear', 'ghostly'],
    'patterned': ['decorated', 'marked', 'designed', 'textured'],
    'spiky': ['sharp', 'thorny', 'barbed', 'pointed'],
    'geometric': ['mathematical', 'regular shapes', 'symmetrical', 'angular']
}

# Additional vocabulary mappings for enhanced features
MONSTER_TYPES = ['creature', 'beast', 'entity', 'being', 'monster', 'demon', 'spirit', 'guardian', 'construct']
PERSONALITY_TRAITS = ['fierce', 'mysterious', 'ancient', 'wise', 'aggressive', 'protective', 'cunning', 'noble']
ABILITY_CATEGORIES = ['elemental', 'psychic', 'physical', 'magical', 'technological', 'spiritual', 'temporal']
FANTASY_ELEMENTS = ['enchanted', 'cursed', 'blessed', 'mythical', 'legendary', 'forbidden', 'sacred', 'primal'] 