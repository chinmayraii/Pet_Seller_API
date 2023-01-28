from django.db import models
from django.contrib.auth.models import User
from .choices import GENDER_CHOICES
import uuid
from django.utils.text import slugify

class BaseModel(models.Model):
    uuid=models.UUIDField(default=uuid.uuid4, primary_key=True,editable=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)

    class Meta:
        abstract=True

class Category(BaseModel):
    category_name=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.category_name

class AnimalBreed(BaseModel):
    animal_breed=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.animal_breed

class AnimalColor(BaseModel):
    animal_color=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.animal_color        


class Animal(BaseModel):
    animal_owner=models.ForeignKey(User,models.CASCADE,related_name='animals')
    animal_category=models.ForeignKey(Category,models.CASCADE,related_name='category')
    animal_views=models.IntegerField(default=0)
    animal_likes=models.IntegerField(default=0)
    animal_name=models.CharField(max_length=100)
    animal_description=models.TextField()
    animal_slug=models.SlugField(max_length=1000, unique=True)
    animal_gender=models.CharField(max_length=50, choices=GENDER_CHOICES)
    animal_breed=models.ManyToManyField(AnimalBreed, null=True)
    animal_color=models.ManyToManyField(AnimalColor, null=True)
    
    def save(self, *args, **kwargs):
        uid=str(uuid.uuid4()).split('-')
        self.animal_slug= slugify(self.animal_name)+" - "+uid[0]
        super(Animal,self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.animal_name



    def incrementViews(self):
        self.animal_views += 1 
        self.save()   

    def incrementLikes(self):
        self.animal_likes += 1 
        self.save()

    class Meta:
        ordering=['animal_name']

class AnimalLocation(BaseModel):
    animal=models.ForeignKey(Animal,on_delete=models.CASCADE,related_name='location')
    location=models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'{self.animal.animal_name+" "+self.location} Location'

class AnimalImage(BaseModel):
    animal=models.ForeignKey(Animal,on_delete=models.CASCADE,related_name='images')
    animal_images=models.ImageField(upload_to='animals')
    def __str__(self) -> str:
        return f'{self.animal.animal_name} Images'
 
