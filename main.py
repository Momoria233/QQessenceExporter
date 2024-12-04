from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime

group_id = input("please enter your qq group id:")
url = f'https://qun.qq.com/essence/indexPc?gc={group_id}&seq=11451419&random=1919810114' #能跑就行

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'Host': 'qun.qq.com',
    'Cookie': ''
}

try:
    response = requests.get(url,headers=header)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

body = soup.find('body')
if not body:
    print("No <body> tag found in the HTML content.")
    exit()

container = body.find('div', class_='container')
if not container:
    print("No container found in the <body> tag.")
    exit()

base_directory = os.path.dirname(os.path.abspath(__file__))
current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
current_directory = os.path.join(base_directory, current_time_str)

blocks = container.find_all('div', class_='block')
for block in blocks:
    block_id = block.get('id', 'default_id')
    folder_path = os.path.join(current_directory, block_id)
    os.makedirs(folder_path, exist_ok=True)
    
    sender_nick = block.find('div', class_='sender_nick')
    sender_time = block.find('div', class_='sender_time')
    add_digest = block.find('div', class_='add_digest')
    
    if sender_nick:
        with open(f'{folder_path}/sender_nick.txt', 'w', encoding='utf-8') as f:
            f.write(sender_nick.get_text())
        print("Sender Nick saved to", f'{folder_path}/sender_nick.txt')
    
    if sender_time:
        with open(f'{folder_path}/sender_time.txt', 'w', encoding='utf-8') as f:
            f.write(sender_time.get_text())
        print("Sender Time saved to", f'{folder_path}/sender_time.txt')
    
    if add_digest:
        with open(f'{folder_path}/add_digest.txt', 'w', encoding='utf-8') as f:
            f.write(add_digest.get_text())
        print("Add Digest saved to", f'{folder_path}/add_digest.txt')
    
    sender_avatar = block.find('div', class_='sender_avatar')
    if sender_avatar and 'style' in sender_avatar.attrs:
        style = sender_avatar['style']
        start = style.find('background-image:url(') + len('background-image:url(')
        end = style.find(');', start)
        if start != -1 and end != -1:
            img_url = style[start:end]
            try:
                img_data = requests.get(img_url).content
                with open(f'{folder_path}/avatar.jpg', 'wb') as f:
                    f.write(img_data)
                print("Avatar image downloaded from", img_url, "to folder", folder_path)
            except requests.RequestException as e:
                print(f"Error downloading avatar image from {img_url}: {e}")
    
    hidden_img_div = block.find('div', style='font-size:0;')
    if hidden_img_div:
        img_tag = hidden_img_div.find('img')
        if img_tag and 'src' in img_tag.attrs:
            img_url = img_tag['src']
            try:
                img_data = requests.get(img_url).content
                with open(f'{folder_path}/image.jpg', 'wb') as f:
                    f.write(img_data)
                print("Image downloaded from", img_url, "to folder", folder_path)
            except requests.RequestException as e:
                print(f"Error downloading image from {img_url}: {e}")
    else:
        short_content = block.find('div', class_='short')
        if short_content:
            texts = short_content.find_all(class_='text')
            combined_text = ''.join([text.get_text() for text in texts])
            with open(f'{folder_path}/combined_text.txt', 'w', encoding='utf-8') as f:
                f.write(combined_text)
            print("Combined Text saved to", f'{folder_path}/combined_text.txt')
print("All essence chat history saved to", current_directory)