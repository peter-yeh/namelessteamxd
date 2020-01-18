
from django.core.management.base import BaseCommand, CommandError
import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Age', 'Favourite colour'],
                  ['Number of siblings', 'Something else...'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

# added in by meeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

INGREDIENTS, PHOTO, LOCATION, BIO = range(4)


def start(update, context):
    reply_keyboard = [['Meat', 'Dairy', 'Robin']]
    # button_list = [
    #         InlineKeyboardButton("Meat", callback_data=...),
    #         InlineKeyboardButton("Dairy", callback_data=...),
    #         InlineKeyboardButton("Robin", callback_data=...)
    #     ]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Which ingredients do you have?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        # reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2)))
    #bot.send_message(..., "A two-column menu", reply_markup=reply_markup)

    return INGREDIENTS


def ingredients(update, context):
    user = update.message.from_user
    logger.info("Ingredients of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me an yes of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def photo(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(update, context):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# End of the my codeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee





class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # TODO: change
        self.main()

    def main(self):
        # # Create the Updater and pass it your bot's token.
        # # Make sure to set use_context=True to use the new context based callbacks
        # # Post version 12 this will no longer be necessary
        # updater = Updater("TOKEN", use_context=True)

        # pass
            # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(
            "1002329449:AAFAK5ltD_lg-g8MAc9iC-0KaK12qZDfEqk", use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher


# commented by meeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        # Add conversation handler with the states INGREDIENTS, PHOTO, LOCATION and BIO
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],

            states={
                INGREDIENTS: [MessageHandler(Filters.regex('^(Meat|Dairy|Robin)$'), ingredients)],

                PHOTO: [MessageHandler(Filters.photo, photo),
                        CommandHandler('skip', skip_photo)],

                LOCATION: [MessageHandler(Filters.location, location),
                           CommandHandler('skip', skip_location)],

                BIO: [MessageHandler(Filters.text, bio)]
            },

            fallbacks=[CommandHandler('cancel', cancel)]
        )

        dp.add_handler(conv_handler)

        # log all errors
        dp.add_error_handler(error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()