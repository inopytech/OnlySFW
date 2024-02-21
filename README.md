# OnlySFW
Open-source anti-NSFW (Not Safe For Work) Telegram bot based in PyTelegramBotAPI and PyTorch

Bot remove's NSFW photos, GIF's, and videos.

## Installing
Install Python 3.11.*

APT package manager based Linux:
```
sudo apt install python3 python3-pip -y
```
RPM package manager based Linux:
```
sudo rpm install python3 python3-pip -y
```
Windows - download installer from official website, open installer, and press checkbox in "Add to path...", press next button, and continue installation.

## Configurate
1. Open `main.py` in any text/code editor, and find `# CONFIG` line (13).
2. Edit parameters:
- `OS` - Operating system.
- `TOKEN` - Telegram bot token.
- `DEVICE` - Device for run AI, `cuda` - NVIDIA graphic card with CUDA, `cpu` - any CPU.

## Install requirements
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install transformers opencv-python pytelegrambotapi
```

# Run
`python3 main.py`

Thanks for using, please give star on this repository in Github.

It works on the basis of the [AI model](https://huggingface.co/Falconsai/nsfw_image_detection).
