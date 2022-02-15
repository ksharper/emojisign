import os
import emoji_data_python
import glob

from slack_sdk.rtm_v2 import RTMClient
from os.path import exists

rtm = RTMClient(token='xoxb-4064436828-3084036248151-bLNNPlQRcw4bZVCGvyG57tEF')

@rtm.on("message")
def handle(client: RTMClient, event: dict):
    channel_id = event['channel']
    thread_ts = event['ts']
    user = event['user']

    if event['text'][0] == ':' and event['text'][len(event['text']) - 1] == ':':
        short_name = event['text'].strip(':')
        print(f'Name: {short_name}')

    file_name = glob.glob(f'/home/pi/custom/{short_name}.*')
    print(f'Custom: {file_name}')
    
    if not file_name:
        try:
            file_name = [f'/home/pi/emoji-data/img-apple-64/{emoji_data_python.emoji_short_names[short_name].image}']
            print(f'Apple: {file_name}')
        except:
            client.web_client.chat_postMessage(
                channel=channel_id,
                text=f"EmojiSign does not know {short_name}!",
                thread_ts=thread_ts
            )

    if file_name:
        os.system('pkill led-image-view')
        os.system(f'/home/pi/rpi-rgb-led-matrix/utils/led-image-viewer --led-rows=32 --led-cols=64 --led-daemon -C {file_name[0]}')

rtm.start()
