
from django.core.management.base import BaseCommand, CommandError
import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_ingredient_category = range(3)

# reply_keyboard = [['Age', 'Favourite colour'],
#                   ['Number of siblings', 'Something else...'],
#                   ['Done']]
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

# added in by meeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

INGREDIENTS, MEAT, DAIRY, ROBIN, BIO = range(5)

type_keyboard = [['Spices and Herbs', 'Dairy', 'Seasonings', 'Vegetables'], ['Baking', 'Meats', 'Condiments',
                        'Alcohol'], ['Fruits', 'Oil', 'Grains', 'Soup']]
meats_keyboard = [['bacon', 'beef shanks', 'beef tenderloin', 'chicken breasts'], ['chicken thighs', 'chicken wings', 
                'ground beef', 'ground chicken'], ['ground lamb', 'ground turkey', 'ham', 'pork loin'], ['pork ribs', turkey breasts', 'venison']]

Spices_and_herbs_keyboard = [['basil', 'bay leaf', 'cayenne pepper', 'chili flakes'],
                      ['chilli powder', 'cilantro', 'cinnamon', 'coriander'],
                      ['cumin', 'curry powder', 'dill', 'italian seasoning'],
                      ['lemongrass', 'nutmeg', 'oregano'],
                      ['paprika', 'parsley', 'pecans'],
                      ['rosemary', 'thyme', 'turmeric']]
diary_keyboard = [['butter', 'buttermilk', 'cheddar cheese', 'coconut milk'], 
                      ['cream cheese', 'eggs', 'milk', 'parmesan cheese']]
seasonings_keyboard = [['black pepper', 'fish sauce', 'salt', 'sour cream'], 
                      ['soy sauce', 'sugar', 'vinegar', 'worcestershire sauce']]
condiments_keyboard = [['barbecue sauce', 'chilli sauce', 'mayonaise'], ['mustard', 'Sriracha', 'tomato sauce']]
Baking: [['active dry yeast', 'all purpose flour', 'almond extract', 'baking powder'], ['baking soda', 'bread crumbs', 'caramel', 'chocolate chips'], ['cornstarch', 'cream of tartar', 'flour', 'heavy whipping cream'], 
['honey', 'hot chocolate powder', 'maple syrup', 'marshmallows', 'peanut butter'], ['peppermint extract', 'vanilla extract', 'whipped cream']]

soup_keyboard = ['beef stock', 'chicken stock']

basket = []

# def photo(update, context):
#     user = update.message.from_user
#     photo_file = update.message.photo[-1].get_file()
#     photo_file.download('user_photo.jpg')
#     logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
#     update.message.reply_text('Gorgeous! Now, send me your location please, '
#                               'or send /skip if you don\'t want to.')

#     return LOCATION


# def skip_photo(update, context):
#     user = update.message.from_user
#     logger.info("User %s did not send a photo.", user.first_name)
#     update.message.reply_text('I bet you look great! Now, send me your location please, '
#                               'or send /skip.')

#     return LOCATION


# def location(update, context):
#     user = update.message.from_user
#     user_location = update.message.location
#     logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
#                 user_location.longitude)
#     update.message.reply_text('Maybe I can visit you sometime! '
#                               'At last, tell me something about yourself.')

#     return BIO


# def skip_location(update, context):
#     user = update.message.from_user
#     logger.info("User %s did not send a location.", user.first_name)
#     update.message.reply_text('You seem a bit paranoid! '
#                               'At last, tell me something about yourself.')

#     return BIO




# End of the my codeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee





class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def __init__(self):
        self.meat_counter = 0

    def handle(self, *args, **options):
        # TODO: change
        self.main()

    def start(self, update, context):

        update.message.reply_text(
            'Hi! My name is Professor Bot. I will hold a conversation with you. '
            'Send /cancel to stop talking to me.\n\n'
            'Send /done to find ur receipt\n\n'
            'Which CHANGEMEEEEEE do you have?',
            reply_markup=ReplyKeyboardMarkup(type_keyboard, one_time_keyboard=True))

        return INGREDIENTS


    def ingredients(self, update, context):
        # user = update.message.from_user

        ingredient_category = update.message.text
        import pdb
        pdb.set_trace()
        
        logger.info(update.message.text)


        update.message.reply_text('I see! Please send me an yes of yourself, '
                                'so I know what you look like, or send /skip if you don\'t want to.',
                                reply_markup=ReplyKeyboardMarkup(type_keyboard, one_time_keyboard=True))
        logger.info("Ingredient is choosen")

        if ingredient_category == "Meat" :
            logger.info("if loop entered: meat")
            update.message.reply_text('Meat is choosen', reply_markup=ReplyKeyboardMarkup(meat_keyboard))
            update.message.reply_text(self.meat_counter)
            
            self.meat_counter+=1
            return MEAT

        else :
            logger.info("Exiting ingredients")
            # return BIO


    def meat(self, update, context):

        logger.info("meat is selecteddddddddddddddddddddddd")
        update.message.reply_text("meat is selected", reply_markup=ReplyKeyboardMarkup(type_keyboard))

        return INGREDIENTS


    def bio(self, update, context):
        user = update.message.from_user
        logger.info("Bio of %s: %s", user.first_name, update.message.text)
        update.message.reply_text('Thank you! I hope we can talk again some day.')

        return ConversationHandler.END


    def cancel(self, update, context):
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Bye! I hope we can talk again some day.',
                                reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END


    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)


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
            entry_points=[CommandHandler('start', self.start)],

            states={
                INGREDIENTS: [MessageHandler(Filters.regex('^(Meat|Dairy|Robin)$'), self.ingredients)],

                # PHOTO: [MessageHandler(Filters.photo, photo),
                #         CommandHandler('skip', skip_photo)],

                # LOCATION: [MessageHandler(Filters.location, location),
                #            CommandHandler('skip', skip_location)],

                MEAT: [MessageHandler(Filters.regex('^(Beef|Chicken)$'), self.meat)],

                BIO: [MessageHandler(Filters.text, self.bio)]
            },

            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

        dp.add_handler(conv_handler)

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()