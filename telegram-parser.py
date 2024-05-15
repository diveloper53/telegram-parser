import re
import json
import xml.etree.ElementTree as ET
from telethon.sync import TelegramClient
from telethon.tl.types import User, MessageEntityMention

def save_messages_to_json(messages):
    with open('messages.json', 'w') as json_file:
        json.dump(messages, json_file, default=str, indent=4)

def save_messages_to_xml(messages):
    root = ET.Element("messages")
    for message in messages:
        message_element = ET.SubElement(root, "message")
        for key, value in message.items():
            sub_element = ET.SubElement(message_element, key)
            sub_element.text = str(value)
    tree = ET.ElementTree(root)
    tree.write("messages.xml")

def save_messages_to_txt(messages):
    text = ''
    for message in messages:
        # if re.search('^[0-9]+\. .*$', str(message.text)):
        text += str(message['text']) + '\n'

    with open('messages.txt', 'w') as file:
        file.write(text)

async def get_messages(client, entity, limit):
    result = await client.get_messages(entity, limit=limit)

    messages = []
    for message in result:
        message_data = {
            'id': message.id,
            'text': message.text,
            'from_id': message.from_id,
            'date': message.date
        }
        if message.from_id is not None:
            sender = await client.get_entity(message.from_id)
            if isinstance(sender, User):
                message_data['sender'] = {
                    'id': sender.id,
                    'first_name': sender.first_name,
                    'last_name': sender.last_name,
                    'username': sender.username
                }
                # Получение номера телефона отправителя (если доступно)
                phone_number = None
                if sender.phone:
                    phone_number = sender.phone
                message_data['sender_phone_number'] = phone_number
                
        # Извлечение упомянутых пользователей
        if message.entities:
            mentioned_users = []
            for entity in message.entities:
                try:
                    if isinstance(entity, MessageEntityMention):
                        mentioned_users.append(entity.user_id)
                except:
                    pass

            message_data['mentioned_users'] = mentioned_users

        messages.append(message_data)

    return messages

async def main(client):
    entity_type = input("Выберите тип (1 - Чат, 2 - Канал): ")
    entity_id = input("Введите ID чата или канала: ")
    limit = int(input("Введите лимит сообщений: "))

    entity = None
    if entity_type == '1':
        entity = await client.get_entity(int(entity_id))
    elif entity_type == '2':
        entity = await client.get_entity(int(entity_id))

    messages = await get_messages(client, entity, limit)
    
    save_format = input("Выберите формат сохранения (1 - JSON, 2 - XML, 3 - TXT): ")
    if save_format == '1':
        save_messages_to_json(messages)
    elif save_format == '2':
        save_messages_to_xml(messages)
    elif save_format == '3':
        save_messages_to_txt(messages)

    print("Сообщения сохранены в файл.")

api_id = input("Введите ID вашего приложения: ")
api_hash = input("Введите хеш вашего приложения: ")
phone_number = input("Введите ваш номер телефона в формате +XXXXXXXXXXX: ")

client = TelegramClient('session_name', api_id, api_hash)
client.start(phone_number)

with client:
    client.loop.run_until_complete(main(client)) 
