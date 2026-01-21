from django.db import models
from  django.contrib.auth.models import  AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    RoleChoices = (
    ('guest', 'guest'),
    ('host', 'host')
    )
    user_role = models.CharField(max_length=30, choices=RoleChoices,default='guest')
    phone_number = PhoneNumberField(null=True, blank=True)
    avatar = models.ImageField(upload_to='user_photo', null=True, blank=True)

    def str(self):
        return f'{self.username}, {self.password}, {self.email}'

class City(models.Model):
    city_name = models.CharField(max_length=100)
    city_img = models.ImageField(upload_to='city_img')

    def str(self):
        return self.city_name

class Rules(models.Model):
    rules_img = models.ImageField(upload_to='rules_images')
    rules_name = models.CharField(max_length=50)

    def __str__(self):
        return self.rules_name

class Property(models.Model):
    title = models.CharField(max_length=50)
    descriptions = models.TextField()
    price_per_night = models.PositiveSmallIntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    PropertyChoices = (
    ('apartment', 'apartment'),
    ('house', 'house'),
    ('studio', 'studio ')
    )
    property_type = models.CharField(max_length=30, choices=PropertyChoices)
    rules = models.ManyToManyField(Rules)
    max_guests = models.PositiveSmallIntegerField()
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField()
    def str(self):
        return f'{self.title},{self.city}'

    def get_avg_rating(self):
        reviews = self.review_property.all()
        if reviews.exists():
            return round(sum([i.rating for i in reviews]) / reviews.count(), 1)
        return 0

    def get_count_person(self):
         return self.review_property.count()

    def get_price_property(self):
        return self.property_price_per_night.count()*2


class PropertyImg(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    property_img = models.ImageField(upload_to='property_photo')

    def str(self):
        return f'{self.property}, {self.property_img}'

class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    StatusChoices = (
    ('pending', 'pending'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
    ('cancelled', 'cancelled')
    )
    status = models.CharField(max_length=30, choices=StatusChoices)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.guest}, {self.property}'

class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1,6)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.property},{self.guest}'
