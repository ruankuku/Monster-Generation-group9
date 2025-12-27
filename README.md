# 🎭 Monster Generation Project

## Project Introduction

This is an AI-based personalized monster character generation project that combines user feature analysis, ComfyUI image generation, and character card creation to generate unique monster characters for each user.

## 📁 Project Structure

```
Monster Generation Project/
├── 📄 run_monster_generation.py   # 🚀 Main Program
├── 📄 requirements.txt            # Python dependencies
├── 📁 src/                        # Core functionality modules
│   ├── 📄 user_feature_extractor.py  # User feature extraction
│   ├── 📄 comfyui_integration.py  # ComfyUI integration
│   ├── 📄 automated_monster_generator.py  # Automated image generation
│   ├── 📄 simple_character_generator.py   # Character generation
│   └── 📄 user_card.py            # User card generation
├── 📁 config/                     # Configuration files
│   ├── 📄 settings.py             # Path configuration
│   └── 📄 mappings.py             # Keyword mappings
├── 📁 data/                       # Data directory
│   ├── 📄 comfyui_template.json   # ComfyUI workflow template
│   ├── 📁 personalization_seeds/  # Personalization seed data
│   └── 📁 input_seeds/            # Input seed data
└── 📁 outputs/                    # Unified output directory
    ├── 📁 features/               # Feature extraction results
    ├── 📁 workflows/              # ComfyUI workflows
    ├── 📁 generated_outputs/      # Generated output results
```

## 🚀 Setup instructions:

### Step 1: Setting up the virtual environment

```
conda create --name pml python=3.12
```
```
conda activate pml
```

### Step 2: Install dependencies

Install all required Python packages：

```
pip install -r requirements.txt
```

### Step 3: Start ComfyUI server (in ComfyUI directory)

Download the models to the ComfyUI folder (please deploy ComfyUI locally)

```
├── models/checkpoints
│ ├── realisticVisionV51_v51VAE.safetensors
├── models/clip_vision
│ ├── IPAdapter_image_encoder_sd15.safetensors
├── models/controlnet
│ ├── control_v11p_sd15_canny_fp16.safetensors
├── models/ipadapter
│ ├── ip-adapter-plus_sd15.safetensors
├── models/vae
│ ├── vae-ft-mse-840000-ema-pruned.safetensors
```

Download address:

```
https://huggingface.co/lllyasviel/fav_models/tree/main/fav
```
```
https://huggingface.co/h94/IP-Adapter/tree/main/models/image_encoder
```
```
https://huggingface.co/lllyasviel/control_v11p_sd15_canny
```
```
https://huggingface.co/h94/IP-Adapter/tree/main/sdxl_models
```
```
https://huggingface.co/stabilityai/sd-vae-ft-mse-original/tree/main
```

### Step 4: Run the application

```
python run_monster_generation.py
```

The program will automatically execute the complete 6-step workflow:

## ⚙️ Configuration Guide

### Required Data Files

1. **User data**: `data/personalization_seeds/user_preferences.csv`
2. **User images**: `data/personalization_seeds/images/P*.png`
3. **Input seed texts**: `data/input_seeds/texts/*.txt`
4. **Input seed images**: `data/input_seeds/images/*.jpg`
5. **ComfyUI template**: `data/comfyui_template.json`

### ComfyUI Requirements

- ComfyUI server running on `http://127.0.0.1:8188`
- Required models and plugins installed (ControlNet, IP-Adapter, etc.)

---

**🎭 Enjoy your personalized monster character creation journey!** 
