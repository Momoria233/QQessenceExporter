from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime
import pandas as pd

group_id = input("please enter your qq group id:")
url = f'https://qun.qq.com/essence/indexPc?gc={group_id}&seq=11451419&random=1919810114'

#获取方法：进入qun.qq.com的网页下打开浏览器console，输入document.cookie
#不过其实在啥要登陆qq的网页下都能获取到
usrCookie = ''

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'Host': 'qun.qq.com',
    'Cookie': usrCookie
}

try:
    response = requests.get(url, headers=header)
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
data_list = []

for block in blocks:
    block_id = block.get('id', 'default_id')

    sender_nick = block.find('div', class_='sender_nick').get_text().replace(' ', '') if block.find('div', class_='sender_nick') else None

    sender_time = block.find('div', class_='sender_time').get_text().replace(' ', '') if block.find('div', class_='sender_time') else None
    if sender_time:
        sender_time = sender_time.replace('发送', '').strip()

    add_digest = block.find('div', class_='add_digest').get_text().replace(' ', '') if block.find('div', class_='add_digest') else None

    if add_digest:
        parts = add_digest.split('由')
        if len(parts) == 2:
            add_time = parts[0].strip()
            temp = parts[1].split('设置')
            if len(temp) == 2:
                add_name = temp[0].strip()
            else:
                add_name = None
                add_time = add_time.strip()
        else:
            add_time = None
            add_name = None
    else:
        add_time = None
        add_name = None

    sender_avatar = block.find('div', class_='sender_avatar')
    avatar_url = None
    if sender_avatar and 'style' in sender_avatar.attrs:
        style = sender_avatar['style']
        start = style.find('background-image:url(') + len('background-image:url(')
        end = style.find(');', start)
        if start != -1 and end != -1:
            avatar_url = style[start:end]

    hidden_img_div = block.find('div', style='font-size:0;')
    img_url = None
    if hidden_img_div:
        img_tag = hidden_img_div.find('img')
        if img_tag and 'src' in img_tag.attrs:
            img_url = img_tag['src']

    short_content = block.find('div', class_='short')
    main_text = None
    if short_content:
        texts = short_content.find_all(class_='text')
        main_text = ''.join([text.get_text() for text in texts])


# 以下是选择在excel中保存的数据
# 可以通过ctrl+“/”添加/减少数据


    data_list.append({
        'Block ID': block_id,  #qq给予精华消息的id，一般不用保留
        'Sender Nick': sender_nick, #发送者昵称
        'Sender Time': sender_time, #发送时间
        'Main Text': main_text, #正文内容
        'Add Digest': add_digest, #精华消息的摘要
        # 'Add Time': add_time, #由精华消息摘要中提取的被设置为精华的时间
        # 'Add Name': add_name, #由精华消息摘要中提取的将这条消息设置成精华的人
        'Avatar URL': avatar_url, #发送者头像的url，但是不推荐使用，分辨率较低
        'Image URL': img_url #消息中的图片的url，但是不推荐使用，分辨率较低
    })


df = pd.DataFrame(data_list)
excel_file_name = f'es_history_{current_time_str}.xlsx'
excel_file_path = os.path.join(base_directory, excel_file_name)
df.to_excel(excel_file_path, index=False, engine='openpyxl')

print("All essence chat history saved to", excel_file_path)