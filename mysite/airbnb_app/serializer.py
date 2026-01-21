from rest_framework import serializers
from .models import (UserProfile,Property,PropertyImg,Rules,Review,Booking,City)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ('username', 'email', 'password', 'first_name', 'last_name')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = UserProfile.objects.create_user(**validated_data)
    return user

  def to_representation(self, instance):
    refresh = RefreshToken.for_user(instance)
    return {
      'user': {
        'username': instance.username,
        'email': instance.email,
      },
      'access': str(refresh.access_token),
      'refresh': str(refresh),
    }


class UserLoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField(write_only=True)

  def validate(self, data):
    user = authenticate(**data)
    if user and user.is_active:
      return user
    raise serializers.ValidationError("Неверные учетные данные")

  def to_representation(self, instance):
    refresh = RefreshToken.for_user(instance)
    return {
      'user': {
        'username': instance.username,
        'email': instance.email,
      },
      'access': str(refresh.access_token),
      'refresh': str(refresh),
    }


class UserProfileListSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['username', 'email', 'password']


class UserProfileDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = '__all__'

class PropertyCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Property
    fields = '__all__'

class UserProfileNameSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ['username']

class PropertyImgSerializer(serializers.ModelSerializer):
  class Meta:
    model = PropertyImg
    fields = '__all__'

class ReviewCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = '__all__'

class PropertyListSerializer(serializers.ModelSerializer):
  photo_property = PropertyImgSerializer(many=True, read_only=True)
  class Meta:
    model = Property
    fields = ['title', 'id','address', 'photo_property', 'max_guests', 'bedrooms', 'bathrooms', 'is_active', 'price_per_night']


class CitySerializer(serializers.ModelSerializer):
  city_property = PropertyListSerializer(many=True, read_only=True)
  class Meta:
    model = City
    fields = ['city_property', 'city_name']


class ReviewSerializer(serializers.ModelSerializer):
  created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%H')
  guest = UserProfileNameSerializer()
  class Meta:
    model = Review
    fields = ['guest', 'comment', 'rating', 'created_date']

class PropertyDetailSerializer(serializers.ModelSerializer):
  photo_property = PropertyImgSerializer(many=True, read_only=True)
  rules = Rules()
  city = CitySerializer()
  review_property = ReviewSerializer(many=True, read_only=True)
  get_avg_rating = serializers.SerializerMethodField()
  count_person = serializers.SerializerMethodField()
  get_price_property = serializers.SerializerMethodField()

  class Meta:
    model = Property
    fields = ['title', 'property_type', 'address', 'max_guests', 'bedrooms','city', 'bathrooms', 'is_active',
              'price_per_night', 'rules', 'photo_property',  'count_person','get_price_property',
              'get_avg_rating','review_property']

  def get_avg_rating(self, obj):
      return obj.get_avg_rating()

  def get_count_person(self, obj):
      return obj.get_count_person()

  def get_price_property(self, obj):
    return obj.get_price_property()


class RulesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Rules
    fields = ['rules_name']



class BookingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Booking
    fields = '__all__'
