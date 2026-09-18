"""
Setup script for Mistral Local LLM
Downloads and configures Mistral model for local inference
"""

import os
import sys
import urllib.request
from pathlib import Path


def download_file(url: str, destination: str, description: str):
    """Download file with progress bar"""
    print(f"\n📥 Downloading {description}...")
    print(f"   URL: {url}")
    print(f"   Destination: {destination}")
    
    def progress_hook(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(f"\r   Progress: {percent}% ")
        sys.stdout.flush()
    
    try:
        urllib.request.urlretrieve(url, destination, progress_hook)
        print("\n   ✅ Download complete!")
        return True
    except Exception as e:
        print(f"\n   ❌ Download failed: {str(e)}")
        return False


def setup_mistral_model():
    """Setup Mistral model for local inference"""
    
    print("=" * 60)
    print("Mistral Local LLM Setup")
    print("=" * 60)
    
    # Create models directory
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)
    
    print(f"\n📁 Models directory: {models_dir}")
    
    # Recommended models (GGUF format for llama-cpp-python)
    models = {
        "1": {
            "name": "Mistral-7B-Instruct-v0.2 (Q4_K_M) - Recommended",
            "size": "~4.4 GB",
            "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            "filename": "mistral-7b-instruct-v0.2.Q4_K_M.gguf",
            "description": "Best balance of quality and speed"
        },
        "2": {
            "name": "Mistral-7B-Instruct-v0.2 (Q5_K_M)",
            "size": "~5.3 GB",
            "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q5_K_M.gguf",
            "filename": "mistral-7b-instruct-v0.2.Q5_K_M.gguf",
            "description": "Higher quality, slower inference"
        },
        "3": {
            "name": "Mistral-7B-Instruct-v0.2 (Q3_K_M)",
            "size": "~3.5 GB",
            "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q3_K_M.gguf",
            "filename": "mistral-7b-instruct-v0.2.Q3_K_M.gguf",
            "description": "Smaller size, faster but lower quality"
        }
    }
    
    print("\n📋 Available Models:")
    for key, model in models.items():
        print(f"\n{key}. {model['name']}")
        print(f"   Size: {model['size']}")
        print(f"   {model['description']}")
    
    print("\n" + "=" * 60)
    choice = input("\nSelect model to download (1-3, or 'skip' to skip): ").strip()
    
    if choice.lower() == 'skip':
        print("\n⏭️  Skipping model download.")
        print("   You can download manually later from HuggingFace.")
        return None
    
    if choice not in models:
        print("\n❌ Invalid choice. Exiting.")
        return None
    
    selected_model = models[choice]
    model_path = models_dir / selected_model['filename']
    
    # Check if already exists
    if model_path.exists():
        print(f"\n✅ Model already exists: {model_path}")
        overwrite = input("   Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("   Using existing model.")
            return str(model_path)
    
    # Download model
    success = download_file(
        selected_model['url'],
        str(model_path),
        selected_model['name']
    )
    
    if success:
        print(f"\n✅ Model setup complete!")
        print(f"   Model path: {model_path}")
        return str(model_path)
    else:
        print(f"\n❌ Model setup failed.")
        return None


def create_env_file(model_path: str):
    """Create or update .env file with model path"""
    
    env_file = Path(__file__).parent.parent / ".env"
    
    print(f"\n📝 Updating environment configuration...")
    print(f"   File: {env_file}")
    
    # Read existing .env if it exists
    env_lines = []
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_lines = f.readlines()
    
    # Update or add MISTRAL_MODEL_PATH
    found = False
    for i, line in enumerate(env_lines):
        if line.startswith('MISTRAL_MODEL_PATH='):
            env_lines[i] = f'MISTRAL_MODEL_PATH={model_path}\n'
            found = True
            break
    
    if not found:
        env_lines.append(f'\n# Mistral Local LLM Configuration\n')
        env_lines.append(f'MISTRAL_MODEL_PATH={model_path}\n')
    
    # Write back
    with open(env_file, 'w') as f:
        f.writelines(env_lines)
    
    print("   ✅ Environment file updated!")


def verify_installation():
    """Verify llama-cpp-python installation"""
    
    print("\n🔍 Verifying llama-cpp-python installation...")
    
    try:
        import llama_cpp
        print("   ✅ llama-cpp-python is installed!")
        print(f"   Version: {llama_cpp.__version__}")
        return True
    except ImportError:
        print("   ❌ llama-cpp-python is not installed!")
        print("\n   Install with:")
        print("   pip install llama-cpp-python")
        print("\n   For GPU support (CUDA):")
        print("   CMAKE_ARGS=\"-DLLAMA_CUBLAS=on\" pip install llama-cpp-python")
        return False


def main():
    """Main setup function"""
    
    print("\n🚀 Starting Mistral Local LLM Setup...\n")
    
    # Step 1: Verify installation
    if not verify_installation():
        print("\n⚠️  Please install llama-cpp-python first, then run this script again.")
        return
    
    # Step 2: Setup model
    model_path = setup_mistral_model()
    
    if model_path:
        # Step 3: Update .env
        create_env_file(model_path)
        
        print("\n" + "=" * 60)
        print("✅ Setup Complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Restart your Flask server")
        print("2. The chatbot will automatically use Mistral LLM")
        print("3. If Mistral fails, it will fallback to rule-based responses")
        print("\nTest the integration:")
        print("   python mistral_local_chat.py")
    else:
        print("\n" + "=" * 60)
        print("⚠️  Setup Incomplete")
        print("=" * 60)
        print("\nManual setup instructions:")
        print("1. Download a Mistral GGUF model from HuggingFace")
        print("2. Place it in: backend/models/")
        print("3. Set MISTRAL_MODEL_PATH in .env file")
        print("\nRecommended model:")
        print("https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
