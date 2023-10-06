
## Getting Started 🚀
1. **Install Python 3.8+**

   Make sure you have Python 3.8 or a higher version installed on your system.

   ```shell
   # Check your Python version
   python --version
2. **Clone the Repository**
    Clone the GitHub repository for the File Stream bot using the following command:
    `git clone https://github.com/mohamadSaleh82/File-Stream-bot`
3. **Set Environment Variables or Edit Config/init.py**
    Open the Config/__init__.py file and configure the following environment variables:
    ```
    api_id = 12345  # Your Telegram API ID
    api_hash = "21ab7cb0a453b5e60016dc7bbeb701cb"  # Your Telegram API hash
    channel_files_chat_id = -10012345466  # Telegram channel chat ID for storing files
    channel_username = "Userlandapp"  # Telegram channel username for support
    token = "0000000:AAFFMMgYoL9Vjb5KUU0bXxVReUI81xuU"  # Your Telegram bot token
    ```
4. **Install Python Dependencies**
    Install the required Python packages using pip:
    `pip install -r requirements.txt`
5. **Run the Web Application**
    run web : 
        `gunicorn main:main --workers 4 --threads 4 --bind 0.0.0.0:$PORT --timeout 86400 --worker-class aiohttp.GunicornWebWorker`
        
    run bot :
        `python -m bot`
        
    run web and bot :
        `./start`


## Environment: 


| Env             | Description                                                      | Example                              |
|-----------------|------------------------------------------------------------------|--------------------------------------|
| api_id          | Telegram API ID for developing a bot (get from my.telegram.org) | 12345                                |
| api_hash        | Telegram API hash for developing a bot                           | 21ab7cb0a453b5e60016dc7bbeb701cb    |
| channel_files_chat_id | Telegram channel chat ID for storing and managing files  | -10012345466                         |
| channel_username | Telegram channel username for support                            | Userlandapp                          |
| token           | Telegram bot token for launching                                  | 0000000:AAFFMMgYoL9Vjb5KUU0bXxVReUI81xuU |

**Management Guide:**

📚 If a file is deleted from the storage channel, the link will expire.

📩 If a file is replayed in the storage channel and a message is sent, that message will be sent to the sender of the file.

🔄 If a file is edited in the storage channel and replaced by another file, the link will download the new file.

🚫 If a user is blocked from the support channel, they can no longer use the bot.

Feel free to ask if you need any further information or assistance! 🤖🔗📦

Don't forget to star this repository 🌟 if you find it useful!


## Management guide:

    If a file is deleted from the storage channel, the link will expire
    If a file is replayed in the storage channel and a message is sent, that message will be sent to the sender of the file
    If a file is edited in the storage channel and replaced by another file, the link will download the new file
    If a user is blocked from the support channel, he can no longer use the robot

Don't forget to star this repository 🌟 if you find it useful!