from django.db import models

class IngredientCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    category = models.ForeignKey(IngredientCategory, on_delete=models.CASCADE, null=False)

class Recipe(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientRecipe')
    recipe_link = models.CharField(max_length=200)
    thumbnail_link = models.CharField(max_length=200)

class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    optional = models.BooleanField(default=False)

    class Meta:
        unique_together = (("ingredient", "recipe"),)
