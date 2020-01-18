from ..models import Ingredient, Recipe

def rank_recipes(ingredients_list):
    ingredient_obj_list = Ingredient.filter(name__in=ingredients_list)
