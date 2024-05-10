# telegram-parser
Quick parsing for telegram chats or channels and saving to json, xml or txt file.

How to use:
1. Install Python3
2. Install Telethon using `pip3 install telethon`
3. Run script using `python3 parser.py`
4. Go to [my.telegram.org/apps](https://my.telegram.org/apps)
5. Create new application
6. Copy and paste to script app_id and app_hash
7. Enter your phone number in international format (example: `+1234567890`)
8. Enter code from Telegram if needed
9. Enter channel id (you can copy it on [web.telegram.org/a](https://web.telegram.org/a/) from browser address bar, if it throws error - try to remove minus symbol)
10. Wait some
11. Select output format: json, xml or txt (Attention! TXT format does not saving any other information about messages excluding text of the message)
12. Congratulations! File saved in the same directory where the script is located (Search for the file named `messages.json`, `messages.xml` or `messages.txt`)

Good luck!
