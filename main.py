import logging
from telegram.ext import Updater, CommandHandler
from wakeonlan import send_magic_packet
from persistence import load_registry, save_registry

# Load the MAC address registry
mac_registry = load_registry()

def start(update, context):
    update.message.reply_text(
        "Hello! I'm a Wake-on-LAN bot. You can register devices with /addmac <name> <mac_address> "
        "and wake up registered devices with /wol <name>. Your registry is private to your account."
    )

def add_mac(update, context):
    user_id = str(update.message.from_user.id)
    try:
        name = context.args[0]
        mac_address = context.args[1]

        if user_id not in mac_registry:
            mac_registry[user_id] = {}

        mac_registry[user_id][name] = mac_address
        save_registry(mac_registry)
        update.message.reply_text(f"MAC address '{mac_address}' registered as '{name}'.")
    except IndexError:
        update.message.reply_text("Usage: /addmac <name> <mac_address>")

def list_macs(update, context):
    user_id = str(update.message.from_user.id)
    if user_id in mac_registry and mac_registry[user_id]:
        mac_list = "\n".join([f"{name}: {mac}" for name, mac in mac_registry[user_id].items()])
        update.message.reply_text(f"Registered devices:\n{mac_list}")
    else:
        update.message.reply_text("You have no registered devices.")

def wake_device(update, context):
    user_id = str(update.message.from_user.id)
    try:
        name = context.args[0]
        if user_id in mac_registry and name in mac_registry[user_id]:
            mac_address = mac_registry[user_id][name]
            send_magic_packet(mac_address)
            update.message.reply_text(f"Sending Wake-on-LAN packet to '{name}' ({mac_address}).")
        else:
            update.message.reply_text(f"Device '{name}' not found. Use /listmacs to see registered devices.")
    except IndexError:
        update.message.reply_text("Usage: /wol <name>")

def main():
    # Load the API key from environment or API_KEY file
    import os
    api_key = os.getenv("TELEGRAM_API_KEY")
    
    if not api_key:
        try:
            with open("API_KEY", "r") as file:
                api_key = file.read().strip()
        except FileNotFoundError:
            print("Error: API_KEY file not found and TELEGRAM_API_KEY environment variable not set.")
            return
    
    if not api_key:
        print("Error: API key is empty.")
        return

    # Initialize the bot
    updater = Updater(api_key, use_context=True)
    dp = updater.dispatcher

    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    # Bot commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addmac", add_mac))
    dp.add_handler(CommandHandler("listmacs", list_macs))
    dp.add_handler(CommandHandler("wol", wake_device))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
