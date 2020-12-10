from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password, **other_fields):
        if not email:
            raise ValueError('You must provide an email address ')
        if not username:
            raise ValueError('Username is required')
        if not first_name:
            raise ValueError('You must provide your first_name')
        if not last_name:
            raise ValueError('You must provide your last_name')
        if not password:
            raise ValueError('Password is required')
        
        email = self.normalize_email(email)
        user = self.model(email = email, username = username, first_name=first_name, last_name=last_name,
                         password=password, **other_fields)
        #user.setpassword(password)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):

        if not username:
            raise ValueError('Username is required')
        if not first_name:
            raise ValueError('You must provide your first_name')
        if not last_name:
            raise ValueError('You must provide your last_name')
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')        

        return self.create_user(email, username, first_name, last_name, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    date_registered = models.DateTimeField(auto_now = True)
    age = models.IntegerField(blank=True, null=True)

    # For the system admin
    is_superuser = models.BooleanField(default=False)

    # For the mh professional
    is_staff = models.BooleanField(default=False)
    #for all users
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clientprofile')
    #profile_pic = CloudinaryField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to = 'uploads/', default = 'pics', blank =True)
    bio = models.TextField(blank =True, null=True)

class MhProProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mhproprofile')
    #profile_pic = CloudinaryField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to = 'uploads/', default = 'pics', blank =True)
    bio = models.TextField(blank =True, null=True)
    work_place = models.CharField(max_length=255)
    work_place_contact = models.CharField(max_length=10, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    education_level = models.CharField(max_length=255, blank=True, null=True)
    id_number = models.IntegerField(default=0)
    title = models.CharField(max_length=255, blank=True, null=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=400, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    user_rating = models.ForeignKey(User, on_delete=models.CASCADE, default = None, related_name='ratings_done')
    person_rated = models.ForeignKey(MhProProfile, on_delete=models.CASCADE,default = None, related_name='ratings')
    
    ratings_out_of_10 = models.DecimalField(max_digits=4, decimal_places=2)
    overall= models.DecimalField(max_digits=4, decimal_places=2)

    # class Meta:
    #     unique_together = ('user_rating', 'person_rated')

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    person_reviewing = models.ForeignKey(MhProProfile, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField(max_length=400, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

