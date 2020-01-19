from django.core.management.base import BaseCommand, CommandError
import logging
import math

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from recipefinder.models import IngredientCategory, Ingredient
from recipefinder.utils.util_rank import rank_recipes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

MAIN, CATEGORY, INGREDIENT, REMOVE = range(4)

def split_array(array, size_per_list):
    new_array = []
    for i in range(math.ceil(len(array) / size_per_list)):
        new_array.append(array[i * size_per_list: min((i + 1) * size_per_list, len(array))])
    return new_array

def get_categories():
    return list(map(capitalize_sentence, IngredientCategory.objects.all().values_list('name', flat=True)))

def get_ingredients(category_name):
    return list(map(capitalize_sentence, Ingredient.objects.filter(category__name=category_name).values_list('name', flat=True)))

def capitalize_sentence(sentence):
    return " ".join(w.capitalize() for w in sentence.split())

def cancel_button():
    return [["Cancel"]]

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def __init__(self):
        self.data = {}

    def handle(self, *args, **options):
        # TODO: change
        self.main()

    def get_category_keyboard(self):
        return split_array(get_categories(), 3)

    def get_ingredient_keyboard(self, category_names):
        return split_array(get_ingredients(category_names), 3)

    def update_current_status(self, update):
        user = update.message.from_user
        ingredients = self.data[user.id]["ingredients"]

        update.message.reply_text(
            'Current Ingredients:\n' + "\n".join(ingredients) + "\n\n"
            'Send /add to add more ingredients\n\n'
            'Send /remove to remove ingredients\n\n'
            'Send /done to start looking for recipes\n\n'
            'Send /exit to stop talking to me\n')


    def reset_status(self, update):
        user = update.message.from_user

        self.data[user.id] = {
            "ingredients": []
        }


    def start(self, update, context):
        self.reset_status(update)

        update.message.reply_text('Hi! My name is Buttercream Frosting Bot ' 
            + '\U0001F9C1' + '\n' 
            'Select the ingredients you have in your fridge and '
            # + "\U0001F35E" + 
            'I will help you decide on what delicious meals you can prepare with them')
            
        self.update_current_status(update)

        

        return MAIN

    def add(self, update, context):
        user = update.message.from_user

        update.message.reply_text(
            'Select a category of ingredients',
            reply_markup=ReplyKeyboardMarkup(self.get_category_keyboard() + cancel_button(), one_time_keyboard=True))

        return CATEGORY


    def category(self, update, context):
        user = update.message.from_user
        category = update.message.text

        if not category in get_categories():
            return CATEGORY

        self.data[user.id]["category"] = category

        update.message.reply_text('Choose the ingredient you want to add',
                                reply_markup=ReplyKeyboardMarkup(self.get_ingredient_keyboard(category) + cancel_button(), one_time_keyboard=True))

        return INGREDIENT

    def ingredient(self, update, context):
        user = update.message.from_user
        ingredient = update.message.text
        category = self.data[user.id]["category"]

        if not ingredient in get_ingredients(category):
            return INGREDIENT

        ingredients = self.data[user.id]["ingredients"]
        if ingredient in ingredients:
            update.message.reply_text('The ingredient ' + ingredient + ' has previously been added')
        else:
            update.message.reply_text('The ingredient ' + ingredient + ' has been added')
            ingredients.append(ingredient)

        self.update_current_status(update)
        return MAIN

    def status(self, update, context):
        self.update_current_status(update)
        return MAIN

    def done(self, update, context):
        user = update.message.from_user

        ingredients = self.data[user.id]["ingredients"]

        ingredients_list = Ingredient.objects.filter(name__in=ingredients)

        result = ""
        recipes = rank_recipes(ingredients_list, n=5)

        ingredients_name_list = set(map(capitalize_sentence, ingredients_list.values_list("name", flat=True)))

        for i, (point, recipe) in enumerate(recipes):
            all_ingredients = set(map(capitalize_sentence, recipe.ingredients.get_queryset().values_list("name", flat=True)))
            have_ingredients = all_ingredients & ingredients_name_list
            missing_ingredients = all_ingredients - ingredients_name_list
            result += str(i + 1) + "\n"
            result += "Name: " + capitalize_sentence(recipe.name) + "\n"
            result += "Similarity Point: " + "{:.1%}".format(point) + "\n"
            result += "Ingredients: " + "<b>" + ", ".join(have_ingredients) + "</b>" + (", " if len(missing_ingredients) > 0 and len(have_ingredients) > 0 else "") + (("<i>" + ", ".join(missing_ingredients) + "</i>") if len(missing_ingredients) > 0 else "")+ "\n"
            result += "Website: " + recipe.recipe_link + "\n"
            result += "\n"

        update.message.reply_text(result, parse_mode=ParseMode.HTML)

        return MAIN

    def remove(self, update, context):
        user = update.message.from_user

        all_ingredients = self.data[user.id]["ingredients"]

        update.message.reply_text('Choose the ingredient you want to remove',
                                reply_markup=ReplyKeyboardMarkup(split_array(all_ingredients, 3) + cancel_button(), one_time_keyboard=True))

        return REMOVE

    def removeIngredient(self, update, context):
        user = update.message.from_user
        ingredient = update.message.text

        if not ingredient in self.data[user.id]["ingredients"]:
            return REMOVE
        
        self.data[user.id]["ingredients"].remove(ingredient)
        update.message.reply_text('The ingredient ' + ingredient + ' has been removed')

        self.update_current_status(update)

        return MAIN

    def cancel(self, update, context):
        self.update_current_status(update)

        return MAIN

    def exit(self, update, context):
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Bye! I hope we can talk again some day.',
                                reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END


    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)


    def main(self):
        updater = Updater(
            "919724175:AAFCkSlYl04sQUwTdGa6fAxtczWn6LL2xR4", use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],

            states={
                MAIN: [CommandHandler('add', self.add),
                        CommandHandler('done', self.done),
                        CommandHandler('status', self.status),
                        CommandHandler('remove', self.remove)],

                CATEGORY: [MessageHandler(Filters.text('Cancel'), self.cancel), MessageHandler(Filters.text, self.category)],

                INGREDIENT: [MessageHandler(Filters.text('Cancel'), self.cancel), MessageHandler(Filters.text, self.ingredient)],

                REMOVE: [MessageHandler(Filters.text('Cancel'), self.cancel), MessageHandler(Filters.text, self.removeIngredient)]
            },

            fallbacks=[CommandHandler('exit', self.exit)]
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
