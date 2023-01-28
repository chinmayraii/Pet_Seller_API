from rest_framework import serializers
from . models import *
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = ['category_name']

class AnimalBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model= AnimalBreed
        fields = ['animal_breed']        

class AnimalColorSerializer(serializers.ModelSerializer):
    class Meta:
        model= AnimalColor
        fields = ['animal_color']        

class AnimalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model= AnimalImage
        fields = ['animal_images']                    

class AnimalSerializer(serializers.ModelSerializer):
    animal_category=serializers.SerializerMethodField()
    animal_color=AnimalColorSerializer(many=True)
    animal_breed=AnimalBreedSerializer(many=True)
    # images=AnimalImageSerializer(many=True)

    def get_animal_category(self,obj):
        return obj.animal_category.category_name

    def create(self, data):
        animal_breed=data.pop('animal_breed')
        animal_color=data.pop('animal_color')

        animal=Animal.objects.create(**data , animal_category=Category.objects.get(category_name='Dog'))

        for ab in animal_breed:
            animal_breed_obj=AnimalBreed.objects.get(animal_breed=ab['animal_breed'])
            animal.animal_breed.add(animal_breed_obj)    

        for ac in animal_color:
            animal_color_obj=AnimalColor.objects.get(animal_color=ac['animal_color'])
            animal.animal_color.add(animal_color_obj)

        return animal  

    def update(self, instance , data):

        if 'animal_breed' in data:
            animal_breed=data.pop('animal_breed')
            instance.animal_breed.clear()
            for ab in animal_breed:
                animal_breed_obj=AnimalBreed.objects.get(animal_breed=ab['animal_breed'])
                instance.animal_breed.add(animal_breed_obj)

        if 'animal_color' in data:
            animal_color=data.pop('animal_breed')
            instance.animal_color.clear()
            for ac in animal_color:
                animal_color_obj=AnimalBreed.objects.get(animal_color=ac['animal_color'])
                instance.animal_color.add(animal_color_obj)

        instance.animal_name=data.get('animal_name', instance.animal_name)
        instance.animal_description=data.get('animal_description', instance.animal_description)
        instance.animal_gender=data.get('animal_gender', instance.animal_gender)
        instance.save()
        
        return instance        



    class Meta:
        model= Animal
        fields = '__all__'    

class AnimalLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model= AnimalLocation
        fields = '__all__'

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.CharField()
    password=serializers.CharField()

    def validate(self, data):

        if 'username' in data:
            user=User.objects.filter(username=data['username'])
            if user.exists():
                raise serializers.ValidationError('Username already taken')

        if 'email' in data:
            user=User.objects.filter(email=data['email'])
            if user.exists():
                raise serializers.ValidationError("Email already exists")        

        return data

class  LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self, data):

        if 'username' in data:
            user=User.objects.filter(username=data['username'])
            if not user.exists():
                raise serializers.ValidationError('username already exists')

        return data  


             