from rest_framework import serializers
from .models import BookTable

class BookTableSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookTable
		fields = '__all__'
