# Telegram Wake-on-LAN Bot
This project creates a Telegram bot that allows you to register MAC addresses and send Wake-on-LAN (WoL) packets to wake devices on your local network. Each Telegram user has their own private registry of devices.

## Table of Contents
1. Requirements
2. Setup
    1. Obtain a Telegram Bot API Key
    2. Clone the Repository
    3. Install Dependencies
    4. Set Up the API Key
    5. Run the Bot
3. Usage
4. Available Commands

## Requirements
- Python 3.7 or higher
- Telegram account
- A device on your local network to send Wake-on-LAN packets to

## Setup

### 1. Obtain a Telegram Bot API Key

To create a new bot, follow these steps:

1. Open Telegram and search for BotFather.
2. Start a chat with BotFather and send the command /newbot.
3. Follow the prompts to set up your new bot:
    - Give it a name.
    - Choose a unique username (must end with "bot", e.g., MyWakeBot).
4. Once created, you will receive an API Key. Save this key as it will be used to run your bot.

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/telegram-wol-bot.git
cd telegram-wol-bot
```

### 3. Install Dependencies
You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```
### 4. Set Up the API Key
1. Create a file named API_KEY in the project directory.
2. Add your Telegram bot API key to the API_KEY file:
```bash
echo "YOUR_API_KEY_HERE" > API_KEY
```

### 5. Run the Bot
Start the bot by running:

```bash
python main.py
```
Your bot is now running! You can interact with it using the Telegram app.

## Usage
Once your bot is running, you can send the following commands to it in a chat:

### Available Commands
- /start - Shows a welcome message and general instructions.
- /addmac <name> <mac_address> - Registers a MAC address with a given name. Example:
    ```mathematica
    /addmac Laptop 00:1A:2B:3C:4D:5E
    ```
- /listmacs - Lists all registered devices for your user account.
- /wol <name> - Sends a Wake-on-LAN packet to the registered device with the specified name. Example:
    ```bash
    /wol Laptop
    ```

## Project Structure
```bash
telegram-wol-bot/
│
├── main.py              # Main bot code
├── persistence.py       # Functions for data persistence
├── mac_registry.json    # Data file (created after running)
├── API_KEY              # File containing the Telegram bot API key
└── README.md            # Project documentation (this file)
```
## Notes
Ensure that the device you want to wake up supports Wake-on-LAN and is properly configured.
The bot maintains a separate MAC address registry for each Telegram user, ensuring privacy and personalized configurations.
