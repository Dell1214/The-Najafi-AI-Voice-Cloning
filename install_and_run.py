# === Najafi AI Voice Cloning Setup ===
# Check NVCC (CUDA)
# !nvcc --version
# Install PyTorch (CUDA 12.4)
# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Install F5-TTS
!pip install git+https://github.com/SWivid/F5-TTS.git

from IPython.display import clear_output
clear_output()

# Launch Gradio Interface
!f5-tts_infer-gradio --share
