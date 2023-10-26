# accounts/factories.py
from cryptography.fernet import Fernet
import secrets
import random
from django.utils import timezone
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files import File
import factory
from faker import Faker
from .models import *
from rooms.models import Room_Data, Slot_Machine
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()

faker = Faker()

def create_random_image():
    image = Image.new('RGB', (100, 100), color=(73, 109, 137))  # You can adjust dimensions and color
    stream = BytesIO()
    image.save(stream, format='JPEG')
    return File(stream, name='random_image.jpg')
  

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"broadcaster_{n}")
    email = factory.LazyAttribute(lambda _: faker.email())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    password = make_password('password1234')
    Status = "Broadcaster"
    Ip_Address = "110.54.207.192"
    Ip_Address_Expires = timezone.now() + timezone.timedelta(days=30)
    Country = "PH"
    Region = "National Capital Region"
    latitude = "14.524300"
    longitude = "121.079200"
    
    @factory.post_generation
    def create_related_models(self, create, extracted, **kwargs):
        if not create:
            return

        # Create an instance of Profile (User_Data) for this user
        ProfileFactory(User=self)

        # Create an instance of Room_Data for this user
        Room_DataFactory(User=self)

        # Create an instance of Slot_Machine for this user
        Slot_MachineFactory(User=self)
    
    
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User_Data

    User = factory.SubFactory(UserFactory)
    Birth_Date = "1990-01-01"
    Real_Name = factory.LazyAttribute(lambda _: faker.name())
    Age = factory.LazyAttribute(lambda _: faker.random_int(min=18, max=99))
    I_Am = factory.LazyAttribute(lambda _: random.choice(['Men', 'Women']))
    Interested_In = factory.LazyAttribute(lambda _: random.choice(['Men', 'Women']))
    Location = "PH"
    Language = "english"
    Body_Type = "chubby"
    Image = factory.django.ImageField(from_path='static/images/new/women/sensual-brunette-black-lingerie-concept-260nw-1933865081.jpg')
    Id_File = factory.django.ImageField(from_path='static/images/new/women/fashion-woman-sitting-on-floor-260nw-1962255619.jpg')
    Second_Id_File = factory.django.ImageField(from_path='static/images/new/women/fashion-woman-sitting-on-floor-260nw-1962255619.jpg')
    
    
    @factory.lazy_attribute
    def U_token(self):
        fernet = Fernet(settings.FERNET_KEY)
        random_token = secrets.token_urlsafe(32)
        return fernet.encrypt(random_token.encode())
      
      
class Room_DataFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Room_Data
    
  User = factory.SubFactory(UserFactory)
  Tab = factory.LazyAttribute(lambda _: random.choice(['MEN', 'WOMEN', 'COUPLES', 'TRANS']))
  

class Slot_MachineFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Slot_Machine
  User = factory.SubFactory(UserFactory)
