from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler,CallbackQueryHandler)
import logging
import telegramcalendar
import telegram
import os
import time
import datetime

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SET_STAT, BOOK, MENU, VIEW, CAT, DATE, DONE = range(7)
LST_CHAT_ID = []
TOKEN = "1047958577:AAFpUNLTsBvr9fi3-DQmZIElPVZcC895Ia0"
PORT = int(os.environ.get('PORT', 5000))

def start(bot, update):
    try:
        print(datetime.date.today().day)
        day = datetime.date.today().day
        if os.path.exists('posters/'+str(day)+'.pdf'):
            bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
            bot.send_document(chat_id=update.message.chat.id, document=open('posters/'+str(day)+'.pdf',"rb"))
        else:
            if int(day) < 22 and int(datetime.date.today().month)==6:
                dl = 22 - int(day)
                bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
                update.message.reply_text(str(dl)+" days left for the webinar series to start!")
            else:
                bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
                update.message.reply_text("The Webinar series are over.")
                return ConversationHandler.END
        reply_keyboard = [['View webinar posters date wise'],['View webinar posters category wise'],['View webinar posters by viewing permissions']]
        update.message.reply_text("Select an option",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return SET_STAT
        
    except Exception as e:
        print(e)

def menu(bot,update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        reply_keyboard = [['View webinar posters date wise'],['View webinar posters category wise'],['View webinar posters by viewing permissions']]
        update.message.reply_text("Select an option",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return SET_STAT
    except Exception as e:
        print(e)

def select_service(bot,update):
    try:
        serviceType = update.message.text
        print(serviceType)
        if serviceType == 'View webinar posters date wise':
            print(serviceType)
            date_wise(bot, update)
            return SET_STAT
        elif serviceType == 'View webinar posters category wise':
            print(serviceType)
            menu_cat(bot,update)
            return CAT
        elif serviceType == 'View webinar posters by viewing permissions':
            print(serviceType)
            menu_view(bot,update)
            return VIEW
        elif serviceType == 'Thanks':
            print("Finally")
            thanks(bot,update)
            return SET_STAT
        elif serviceType == 'Menu':
            print("m")
            STATE = MENU
            menu(bot,update)
            return SET_STAT
        else:
            STATE = MENU
            return MENU
    except Exception as e:
        print(e)

def date_wise(bot, update):
    try:
        print("Hi")
        user = update.message.from_user
        update.message.reply_text('I see! Please select a date to proceed',reply_markup=telegramcalendar.create_calendar())
    except Exception as e:
        print(e)

def select_slot(bot, update):
    try:
        print("Hi")
        selected,date = telegramcalendar.process_calendar_selection(bot, update)
        if selected:
            print(date.day)
            day = date.day
            if (21< int(day) < 31 and int(date.month) == 6) or (int(day)<=12 and int(date.month) == 7):
                bot.send_document(chat_id=update.callback_query.from_user.id, document=open('posters/'+str(day)+'.pdf',"rb"))
                bot.send_message(chat_id=update.callback_query.from_user.id, text = "Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],resize_keyboard=True))
                return
            else:
                bot.send_message(chat_id=update.callback_query.from_user.id, text ="No Webinar is scheduled for the selected date.")
                bot.send_message(chat_id=update.callback_query.from_user.id, text = "Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],resize_keyboard=True))
                return
    except Exception as e:
        print(e)

def cat_wise(bot,update):
    try:
        #bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        #update.message.reply_text('I see! Please select a category to proceed',reply_markup=ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],resize_keyboard=True))
        print("Category Wise")
        cat = update.message.text
        files = []
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        for r, d, f in os.walk(cat+'/'):
            for file in f:
                print(file)
                bot.send_document(chat_id=update.message.chat.id, document=open(cat+'/'+file,"rb"))
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],resize_keyboard=True))
        return SET_STAT 
    except Exception as e:
        print(e)
        update.message.reply_text("Service Timed Out. Please press start to continue.")

def view_wise(bot,update):
    try:
        print("View Wise"+update.message.text)
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        cat = update.message.text
        for r, d, f in os.walk(cat+'/'):
            for file in f:
                bot.send_document(chat_id=update.message.chat.id, document=open(cat+'/'+file,"rb"))
        update.message.reply_text("Select an option to continue.",reply_markup = ReplyKeyboardMarkup(keyboard= [['Thanks', 'Menu']],resize_keyboard=True))
        return SET_STAT 
    except Exception as e:
        print(e)
        update.message.reply_text("Service Timed Out. Please press start to continue.")
    
def menu_cat(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        keyboard = [['Guidance for better placements'], ['Higher studies and Career Guidance'],['Research and Innovations'],['Entrepreneurship Development'],['Trends in Technology']]
        reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
        update.message.reply_text("Select an option to continue.", reply_markup=reply_markup)
    except Exception as e:
        print(e)

def menu_view(bot, update):
    try:
        bot.send_chat_action(chat_id=update["message"]["chat"]["id"], action=telegram.ChatAction.TYPING)
        time.sleep(2)
        keyboard = [['Private Viewing'], ['Public Viewing']]
        reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
        update.message.reply_text("Select an option to continue.", reply_markup=reply_markup)
    except Exception as e:
        print(e)

def thanks(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.',reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("1047958577:AAFpUNLTsBvr9fi3-DQmZIElPVZcC895Ia0")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SET_STAT: [RegexHandler('^(View webinar posters date wise|View webinar posters category wise|View webinar posters by viewing permissions|Thanks|Menu)$',select_service)],
            DATE: [MessageHandler(Filters.text,date_wise),CommandHandler('cancel', cancel)],
            VIEW: [MessageHandler(Filters.text, view_wise),CommandHandler('cancel', cancel)],
            CAT: [MessageHandler(Filters.text, cat_wise),CommandHandler('cancel', cancel)],
            MENU: [MessageHandler(Filters.text, menu)]
             },
        fallbacks=[CommandHandler('start', start),CommandHandler('cancel', cancel)],
        allow_reentry = True
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(select_slot))
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    
    # log all errors)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
    updater.bot.setWebhook('https://sheltered-shore-73299.herokuapp.com/ ' + TOKEN)

#    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

