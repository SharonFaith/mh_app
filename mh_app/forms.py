from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, MhProProfile
from django.db import transaction

User = get_user_model()

class ClientSignUp(UserCreationForm):

    class Meta(UserCreationForm.Meta):


        model = User

        fields = ['username', 'first_name', 'last_name', 'email']
        
    
    @transaction.atomic
    def save(self):
        user = super().save()
        
        user.save()
        profile = UserProfile.objects.create(user = user)
        
        return user
   
CHOICES = [(1, 'Prof.'), (2, 'Dr.'), (3, 'Ms.'), (4, 'Mrs.'), (5, 'Mr.')]


class WorkerSignUp(UserCreationForm):
        title = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
        #education_level = forms.CharField(max_length=255)
        work_place =  forms.CharField(max_length=255)
        work_place_contact = forms.CharField(max_length=10)
       
        id_or_passport_number = forms.IntegerField()

        class Meta(UserCreationForm.Meta):

            model = User

            fields = ['username', 'first_name', 'last_name', 'email', 'age']

        @transaction.atomic
        def save(self):
            user = super().save()
            # user.is_staff = True
            # user.save()
            mhworker = MhProProfile.objects.create(user=user)
            return user