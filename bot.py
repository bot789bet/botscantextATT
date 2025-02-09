# ©️ @jhny0210 

from telegram import ChatAction,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler,PicklePersistence
import logging
import os
from functools import wraps
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests


API_KEY = os.environ.get("API_KEY","") 

TOKEN = os.environ.get("BOT_TOKEN","")

OWNER = os.environ.get("OWNER", "")

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


@run_async     
@send_typing_action
def start(update,context):
    """Send a message when the command /start is issued."""
    global first
    first=update.message.chat.first_name
    keybord1 = [[InlineKeyboardButton("Owner 👨‍💻", url=f"https://t.me/{OWNER}"),
                 InlineKeyboardButton("Tutorial 📺", url="https://7789bets.com")]]
    reply_markup = InlineKeyboardMarkup(keybord1)
    update.message.reply_text('Hi! '+str(first)+' \n\nBot Quét ảnh ra chữ. Được tạo bởi johnnytr0210. Powered by 789bet.\n\nGo /help de duoc tro giup...', reply_markup=reply_markup)

def help(update,context):
    """Send a message when the command /help is issued."""
    global first
    first=update.message.chat.first_name
    keybord1 = [[InlineKeyboardButton("Owner 👨‍💻", url=f"https://t.me/{OWNER}"),
                 InlineKeyboardButton("Tutorial 📺", url="https://7789bets.com")]]
    reply_markup = InlineKeyboardMarkup(keybord1)
    update.message.reply_text('Chào! '+str(first)+' \n\nVui lòng theo các bước sau...\n➥ Gửi ảnh vào nhóm \n➥ Bấm vào nút Vietnamese \n➥ Đợi chữ được giải nén', reply_markup=reply_markup)


@run_async
@send_typing_action
def convert_image(update, context):
    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    file = newFile.file_path
    context.user_data['filepath'] = file
    
    user_id = update.message.from_user.id  # Lấy user_id của người gửi
    
    keyboard = [[InlineKeyboardButton("Vietnamese", callback_data='vie')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Chỉ cho người gửi được quyền bấm vào nút
    if user_id == update.effective_user.id:
        update.message.reply_text("Ai gửi thì bấm vào đây 👇", reply_markup=reply_markup)
    else:
        update.message.reply_text("Bạn không có quyền bấm vào nút.")

@run_async
def button(update,context):
    filepath=context.user_data['filepath']
    query = update.callback_query
    query.answer()
    query.edit_message_text("Đang giải nén...")
    data=requests.get(f"https://apipro3.ocr.space/parse/imageurl?apikey={API_KEY}&url={filepath}&language={query.data}&detectOrientation=True&filetype=JPG&OCREngine=3&isTable=True&scale=True")
    data=data.json()
    if data['IsErroredOnProcessing']==False:
        message=data['ParsedResults'][0]['ParsedText']
        query.edit_message_text(f"{message}")
    else:
        query.edit_message_text(text="⚠️ Bot lỗi rùi, vui lòng liên hệ telegram @johnnytr0210 để báo lỗi")

persistence=PicklePersistence('userdata')
def main():
    token=TOKEN 
    updater = Updater(token,use_context=True,persistence=persistence)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(MessageHandler(Filters.photo, convert_image))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling(clean=True)
    updater.idle()
 
	
if __name__=="__main__":
	main()
