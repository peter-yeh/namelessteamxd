from ..models import Ingredient, Recipe, IngredientRecipe

# Returns list of recipe in form of (percentage, recipe)
def rank_recipes(ingredients_list, n=5):
    all_recipes = Recipe.objects.all()

    def get_point(recipe):
        all_ingredients = IngredientRecipe.objects.filter(recipe=recipe)
        #all_ingredients_all = all_ingredients.count()
        all_ingredients_compulsory = all_ingredients.filter(optional=False).count()
        matched_ingredients = IngredientRecipe.objects.filter(recipe=recipe, ingredient__in=ingredients_list)
        #matched_ingredients_all = matched_ingredients.count()
        matched_ingredients_compulsory = matched_ingredients.filter(optional=False).count()

        #all_ingredient_percentage = matched_ingredients_all / all_ingredients_all
        compulsory_ingredient_percentage = matched_ingredients_compulsory / all_ingredients_compulsory if all_ingredients_compulsory != 0 else 0

        #print(all_ingredient_percentage)
        #print(compulsory_ingredient_percentage)

        return (compulsory_ingredient_percentage, recipe)

    return list(sorted(filter(lambda x: x[0] > 0, map(get_point, all_recipes)), key=lambda x: x[0], reverse=True))[:n]
