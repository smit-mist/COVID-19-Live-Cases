from django.db import models
from django.forms import ModelForm


class Review(models.Model):
    name = models.CharField(max_length=50)
    mob = models.BigIntegerField()
    msg = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Search(models.Model):
    country_name = models.CharField(max_length=40)


class Searchform(ModelForm):
    class Meta:
        model = Search
        fields = ['country_name']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'mob', 'msg']
