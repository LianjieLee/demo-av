import os
import sys

from glob import glob
from telethon import TelegramClient, sync

# https://docs.telethon.dev/en/latest/concepts/sessions.html
# sync can not omit
def send_video(api_id, api_hash, peer_name, video_list, caption):
    client = TelegramClient("tg_client", api_id, api_hash)
    client.start()
    client.connect()
    client.send_file(peer_name, video_list, caption=caption, supports_streaming=True)

if __name__ == '__main__':
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    peer_name = sys.argv[1]
    caption = sys.argv[2]
    video_list = glob("*.mp4")
    video_list.sort()
    video_list.insert(0, "info/poster.jpg")
    print(f"sending {video_list}", flush=True)
    send_video(api_id, api_hash, peer_name, video_list, caption)