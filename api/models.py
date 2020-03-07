from django.db import models


class BookTable(models.Model):
	name = models.CharField(max_length=30)
	author = models.CharField(max_length=30)
	price = models.IntegerField()

	def __str__(self):
		return self.name

