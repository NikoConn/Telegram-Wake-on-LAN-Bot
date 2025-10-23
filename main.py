import logging
import os
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from wakeonlan import send_magic_packet
from persistence import load_registry, save_registry

# Load the MAC address registry
mac_registry = load_registry()

def build_keyboard_for_user(user_id):
    """Build a ReplyKeyboardMarkup for a user including quick /wol buttons for their devices."""
    buttons = []
    # Fixed quick actions
    buttons.append([KeyboardButton('/listmacs'), KeyboardButton('/addmac')])

    user_id = str(user_id)
    if user_id in mac_registry and mac_registry[user_id]:
        # Add a button per device as /wol name
        row = []
        for name in mac_registry[user_id].keys():
            # Keep rows of up to 3 buttons
            row.append(KeyboardButton(f"/wol {name}"))
            if len(row) >= 3:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)

    return ReplyKeyboardMarkup(buttons, one_time_keyboard=False, resize_keyboard=True)


def start(update, context):
    update.message.reply_text(
        "Hello! I'm a Wake-on-LAN bot. Register devices with /addmac <name> <mac_address> "
        "and wake registered devices with /wol <name>. Your registry is private.",
        reply_markup=build_keyboard_for_user(update.message.from_user.id),
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
        update.message.reply_text(
            f"MAC address '{mac_address}' registered as '{name}'.",
            reply_markup=build_keyboard_for_user(update.message.from_user.id),
        )
    except IndexError:
        update.message.reply_text("Usage: /addmac <name> <mac_address>")

def list_macs(update, context):
    user_id = str(update.message.from_user.id)
    if user_id in mac_registry and mac_registry[user_id]:
        mac_list = "\n".join([f"{name}: {mac}" for name, mac in mac_registry[user_id].items()])
        update.message.reply_text(
            f"Registered devices:\n{mac_list}",
            reply_markup=build_keyboard_for_user(update.message.from_user.id),
        )
    else:
        update.message.reply_text("You don't have any registered devices.")

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


def handle_text_buttons(update, context):
    """Handle text messages coming from the ReplyKeyboard buttons.

    If the text starts with '/wol ' we'll call the same logic as the /wol command.
    Otherwise, echo or suggest using /menu.
    """
    text = update.message.text.strip()

    # Support buttons like '/wol name'
    if text.startswith('/wol '):
        # Create a fake context.args for wake_device
        class Ctx:
            args = text.split()[1:]

        wake_device(update, Ctx)
        # After action, refresh keyboard
        update.message.reply_text('Done.', reply_markup=build_keyboard_for_user(update.message.from_user.id))
        return

    if text == '/listmacs':
        list_macs(update, context)
        return

    if text == '/addmac':
        update.message.reply_text('Use /addmac <name> <mac_address> to add a device.')
        return

    # Fallback
    update.message.reply_text("Command not recognized. Use /menu to see options.")

def main():
    # Load the API key from environment or API_KEY file
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

    # Handle quick-reply button presses (they arrive as normal text messages)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_buttons))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
