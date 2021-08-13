from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler,CallbackQueryHandler
from datetime import datetime
from time import sleep

import shutil

TELEGRAM_TOKEN="1442470337:AAFmNpQdsGTkcOtbaOtJBGroSIeKiF7Ukfk"

# Función para enviar mensaje por Telegram
def send_message(text, chat_id, silent=False):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        msg = bot.send_message(chat_id=chat_id, text=text, disable_notification=silent)
        return msg["message_id"]
    except Exception as e:
        return e

# Función para eliminar mensaje en Telegram
def delete_message(msg_id, chat_id):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.delete_message(chat_id=chat_id, message_id=msg_id)
    except Exception as e:
        print(f"Error al eliminar el mensaje: {e}")

# Función para enviar mensaje del Espacio en Disco
def send_disk_message():
    disco_duro = shutil.disk_usage("/")
    free = (disco_duro.free / (1024.0 ** 3))
    texto = (
        '🚨 🎲 Espacio en disco 🎲 🚨\n'
        f'🗓 {datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
        f'🖥 Espacio en disco libre {round(free, 2)}GB'
    )

    msg_id = send_message(chat_id="1598327449", text=texto)
    print(msg_id)

# Menú principal
def menu_principal():
    options = [
        [InlineKeyboardButton("¿Cuánto es mi espacio libre de Disco Duro?", callback_data="reply_disk_free")]
    ]
    return InlineKeyboardMarkup(options)

def start(update, context):
    username = update.effective_user.name
    update.message.reply_text(text=f"Hola {username}. ¿En qué puedo ayudarte?", reply_markup=menu_principal())

def reply_disk_free(update, context):
    query = update.callback_query
    query.answer()
    disco_duro = shutil.disk_usage("/")
    free = (disco_duro.free / (1024.0 ** 3))
    query.edit_message_text(f'Espacio en disco duro libre es: {round(free, 2)}GB')
    sleep(3)
    mostrar_seguir_consultando(update, context)

def mostrar_seguir_consultando(update, context):
    chat_id = update.effective_user.id
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=chat_id, text="Otra consulta", reply_markup=menu_principal())

def telegram_bot():
    print("Iniciando el Bot de Telegram CoP")
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(reply_disk_free, pattern="reply_disk_free"))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    telegram_bot()