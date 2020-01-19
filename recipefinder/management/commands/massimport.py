from django.core.management.base import BaseCommand, CommandError
from recipefinder.models import Recipe, Ingredient, IngredientRecipe, IngredientCategory
import csv

def clean_string(string):
    cleaned_string = string.strip().lower()
    return cleaned_string

class Command(BaseCommand):
    help = 'Mass imports all the data from the file'

    def add_arguments(self, parser):
        parser.add_argument('category_file', nargs='+', type=str)
        parser.add_argument('ingredient_file', nargs='+', type=str)
        parser.add_argument('recipe_file', nargs='+', type=str)

    def handle(self, *args, **options):
        category_file = options['category_file'][0]
        ingredient_file = options['ingredient_file'][0]
        recipe_file = options['recipe_file'][0]

        with open(category_file, 'r') as csvfile:
            categoryreader = csv.reader(csvfile)
            for row in categoryreader:
                name = row[0]
                emoji = row[1]
                category_obj, created = IngredientCategory.objects.update_or_create(name=name, defaults={'emoji': emoji})

        with open(ingredient_file, 'r') as csvfile:
            ingredientreader = csv.reader(csvfile)
            ingredient_by_cat = dict()

            header = next(ingredientreader)
            header = list(map(clean_string, header))

            for head in header:
                ingredient_by_cat[head] = []

            next(ingredientreader)

            for row in ingredientreader:
                for i, val in enumerate(row):
                    if len(val) > 0:
                        ingredient_by_cat[header[i]].append(val)

            for category in ingredient_by_cat.keys():
                category = clean_string(category)
                category_obj, created = IngredientCategory.objects.get_or_create(name=category)
                if not created:
                    print("Ingredient category " + category + " not created")
                for ingredient in ingredient_by_cat[category]:
                    ingredient = clean_string(ingredient)
                    ingredient_obj, created = Ingredient.objects.get_or_create(name=ingredient, category=category_obj)
                    if not created:
                        print("Ingredient " + ingredient + " not created")

        with open(recipe_file, 'r') as csvfile:
            recipereader = csv.reader(csvfile)

            header = next(recipereader)

            other_cat, created = IngredientCategory.objects.get_or_create(name="Other")

            for row in recipereader:
                name = row[0]
                recipe_link = row[1]
                thumbnail_link = row[2]
                ingredients = row[3:]

                name = clean_string(name)
                ingredients = list(map(lambda x: clean_string(x), ingredients))

                defaults = {
                    "recipe_link": recipe_link,
                    "thumbnail_link": thumbnail_link
                }
                recipe_obj, created = Recipe.objects.get_or_create(name=name, defaults=defaults)
                for ingredient in ingredients:
                    if len(ingredient) > 0:
                        ingredient_obj, created = Ingredient.objects.get_or_create(name=ingredient, defaults={"category": other_cat})
                        IngredientRecipe.objects.get_or_create(ingredient=ingredient_obj, recipe=recipe_obj, optional=False)

        print("Done Import")