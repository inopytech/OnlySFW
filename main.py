import os

import cv2
import telebot
from datetime import datetime

import torch

from nsfw_detector import NSFWDetector
from random import choice
from string import ascii_letters
from string import digits

# CONFIG

OS = "unix"  # windows / unix

TOKEN = "ewtjhrbjwrkweteqhtq"  # Токен Telegram бота, можно получить в оффициальном боте @BotFather

DEVICE = "cpu"  # Устанавливает устройство, на котором будет запущен ИИ, для поиска NSFW.
# Возможно: cpu - процессор,
# cuda - видекарта/графический ускоритель NVIDIA.

# END_CONFIG

bot = telebot.TeleBot(TOKEN)
nsfw_detector = NSFWDetector()
torch.device = ""


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    media_folder = "media/{}/{}".format(message.from_user.username, datetime.now().strftime("%Y-%m-%d-%H-%M"))
    os.makedirs(media_folder, exist_ok=True)

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(media_folder, file_info.file_path.split('/')[-1])

    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    nsfw_score = nsfw_detector.detect(file_path, OS)
    if nsfw_score == "normal":
        pass
    elif nsfw_score == "nsfw":
        bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=['video'])
def handle_other_media(message):
    media_folder = "media/{}/{}".format(message.from_user.username, datetime.now().strftime("%Y-%m-%d-%H-%M"))
    os.makedirs(media_folder, exist_ok=True)

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_extension = message.document.file_name.split('.')[-1]
    file_path = os.path.join(media_folder, f"media.{file_extension}")

    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    if file_extension.lower() in ['gif', 'mp4']:
        cap = cv2.VideoCapture(file_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        random_frame_index = int(total_frames * 0.5)
        cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_index)
        _, frame = cap.read()
        rc = ''.join(choice(ascii_letters + digits) for _ in range(48))
        random_frame_path = os.path.join(media_folder, f"random_frame-{rc}.jpg")
        cv2.imwrite(random_frame_path, frame)
        cap.release()

    nsfw_score = nsfw_detector.detect(file_path, OS)
    if nsfw_score == "normal":
        pass
    elif nsfw_score == "nsfw":
        bot.delete_message(message.chat.id, message.message_id)


print("Loaded")

bot.polling()
