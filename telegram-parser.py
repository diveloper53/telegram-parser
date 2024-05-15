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
    print('Parsing... Please wait...')
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
                # Get user phone number if allowed
                phone_number = None
                if sender.phone:
                    phone_number = sender.phone
                message_data['sender_phone_number'] = phone_number
                
        # Get mentioned users
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

    print('Parsing finished!')

    return messages

async def main(client):
    entity_type = input("Select type (1 - Chat/Group, 2 - Channel): ")
    entity_id = input("Enter ID of chat or channel (you can get it from https://web.telegram.org/a/ from your browser address bar, remove minus if u getting an error): ")
    limit = int(input("Enter messages limit: "))

    entity = None
    if entity_type == '1':
        entity = await client.get_entity(int(entity_id))
    elif entity_type == '2':
        entity = await client.get_entity(int(entity_id))

    messages = await get_messages(client, entity, limit)
    
    save_format = input("Select saving format (1 - JSON, 2 - XML, 3 - TXT, 0 - ALL OF THEM): ")
    if save_format == '1':
        save_messages_to_json(messages)
    elif save_format == '2':
        save_messages_to_xml(messages)
    elif save_format == '3':
        save_messages_to_txt(messages)
    elif save_format == '0':
        save_messages_to_json(messages)
        save_messages_to_xml(messages)
        save_messages_to_txt(messages)

    print("Saved!")

print("To start your work with telegram parser go to https://my.telegram.org/ and log in and select API Developement Tools, then provide api_id and api_hash from it.")

api_id = input("Enter your api_id: ")
api_hash = input("Enter your api_hash: ")
phone_number = input("Now please enter your phone number in international format (example: +1234567890): ")

client = TelegramClient('session_name', api_id, api_hash)
client.start(phone_number)

with client:
    client.loop.run_until_complete(main(client)) 
