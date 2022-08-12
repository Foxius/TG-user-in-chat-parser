from signal import raise_signal
from telethon import TelegramClient, events
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time
import asyncio
import pandas as pd
###############################################
api_id = '********'                           #
api_hash = '********************************' #
phone = '**********'						  #
###############################################
client = TelegramClient('session_name', api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('cls')
    client.sign_in(phone, input('[+] Введите код: '))
os.system('cls')

chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print('[+] Выберите групу для парсинга участников :')
i=0
for g in groups:
    print('['+str(i)+']'+' - '+ g.title)
    i+=1
 
print('')
g_index = input("[+] Введите номер : ")
target_group=groups[int(g_index)]
chat = target_group.id
 # Айди чата вставлять без кавычек 
df = pd.DataFrame(columns=['Users'])
lst = []
async def main():
  async with client:
    async for user in client.iter_participants(chat):
        lst.append(str(user.id) + ' @' + str(user.username))
        print(user.id)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
df['Users'] = lst
df.to_csv('Users.csv')
for i in lst:
    with open('logs.txt','a') as file:
        file.write(i + '\n')