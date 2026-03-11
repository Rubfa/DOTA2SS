from django.db import models


class Item(models.Model):

    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name


class PriceRecord(models.Model):

    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    date = models.DateField()

    price = models.FloatField()

    quantity = models.IntegerField()


class Hero(models.Model):

    name = models.CharField(max_length=100)

    icon = models.CharField(max_length=200)

    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Cosmetic(models.Model):

    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)

    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)

    price = models.FloatField(default=0)

    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name