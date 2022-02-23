import os
import json
import glob
import wget

from dotenv import load_dotenv

load_dotenv()

os.system('curl -H "Authorization: Bearer ${SLACK_USER_TOKEN}" --output /home/pi/emoji.json  https://slack.com/api/emoji.list')

output_directory = '/home/pi/custom'
emoji_file = open('/home/pi/emoji.json')
emoji = json.load(emoji_file)

# First pass ignore alias
for short_name, url in emoji['emoji'].items():
    if not url.startswith('alias'):
        alias = url.split(':')[1]
        ext = os.path.splitext(url)[1]
        file = f'{short_name}{ext}'

        if os.path.exists(f'{output_directory}/{file}'):
            print(f'File {file} already exists, skipping')
        else:
            print(f'Downloading {output_directory}/{file}')
            wget.download(url, out=f'{output_directory}/{file}')
            print()

# Second pass only alias
for short_name, url in emoji['emoji'].items():
    if url.startswith('alias'):
        alias = url.split(':')[1]
        source_file = glob.glob(f'{output_directory}/{alias}.*')
        
        if source_file:
            ext = os.path.splitext(glob.glob(f'{output_directory}/{alias}.*')[0])[1]
            output_file = f'{short_name}{ext}'

            if os.path.exists(f'{output_directory}/{output_file}'):
                print(f'File {output_file} already exists, skipping')
            else:
                print(f'Creating alias {output_directory}/{output_file} from {output_directory}/{source_file[0]}')
                os.system(f'cp {source_file[0]} {output_directory}/{output_file}')
            

emoji_file.close()