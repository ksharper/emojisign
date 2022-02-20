import os
import glob
import socket
import re
import emoji_data_python
from slack_sdk.rtm_v2 import RTMClient
from typing import cast
from dotenv import load_dotenv

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

load_dotenv()
rtm = RTMClient(token=os.environ["SLACK_BOT_TOKEN"])

ip_address = get_ip_address()
os.system('pkill led-image-view')
os.system(f'/home/pi/rpi-rgb-led-matrix/utils/text-scroller -f /home/pi/rpi-rgb-led-matrix/fonts/9x18.bdf -s 5 -l 1 --led-rows=32 --led-cols=64 --led-chain=2 --led-pixel-mapper=V-mapper {ip_address}')

@rtm.on("message")
def handle(client: RTMClient, event: dict):
    channel_id = event['channel']
    thread_ts = event['ts']
    user = event['user']

    emoji_search = re.search('\:([0-9a-z-_+]*)\:(?:\:([0-9a-z-]*)\:)?', event['text'], re.IGNORECASE)
    if emoji_search:
        short_name = emoji_search.group(1)
        skin_tone = emoji_search.group(2)
            
    print(f'Name: {short_name}')
    print(f'Skin tone: {skin_tone}')

    file_name = glob.glob(f'/home/pi/custom/{short_name}.*')
    print(f'Custom: {file_name}')
    
    if not file_name:
        try:
            if emoji_search.lastindex == 1:
                file_name = [f'/home/pi/emoji-data/img-apple-64/{emoji_data_python.emoji_short_names[short_name].image}']
            else:
                file_name = [f'/home/pi/emoji-data/img-apple-64/{emoji_data_python.emoji_short_names[short_name].skin_variations[emoji_data_python.emoji_short_names[skin_tone].unified].image}']

            print(f'Apple: {file_name}')
        except:
            client.web_client.chat_postMessage(
                channel=channel_id,
                text=f"emojisign does not know {event['text']}",
                thread_ts=thread_ts
            )

    if file_name:
        os.system('pkill led-image-view')
        os.system(f'/home/pi/rpi-rgb-led-matrix/utils/led-image-viewer --led-rows=32 --led-cols=64 --led-chain=2 --led-pixel-mapper=V-mapper --led-daemon -C {file_name[0]}')

rtm.start()
