from django.core.management.base import BaseCommand, CommandError
from recipefinder.utils.util_rank import rank_recipes
from recipefinder.models import Ingredient

class Command(BaseCommand):
    help = 'Get the top n recipes with the given ingredients'

    def add_arguments(self, parser):
        parser.add_argument('n', type=int)
        parser.add_argument('-i', '--ingredients', nargs='+', type=str)
    
    def handle(self, *args, **options):
        n = options['n']
        ingredients = options['ingredients']

        ingredients_list = Ingredient.objects.filter(name__in=ingredients)
        print("Searching by the given ingredients:")
        print(", ".join(list(map(lambda x: x.name, ingredients_list))))
        print("")

        recipes = rank_recipes(ingredients_list, n=n)

        for i, (point, recipe) in enumerate(recipes):
            print(i + 1)
            print("Name: " + recipe.name)
            print("Point: " + str(point))
            print("Ingredients: " + str(", ".join(map(lambda x: x.name, recipe.ingredients.get_queryset()))))
            print("")
        
