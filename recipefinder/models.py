from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientRecipe')
    
class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    optional = models.BooleanField()
