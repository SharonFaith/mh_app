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
    # def create(self, validated_data):
    #     print("VALIDATED DATA: ",validated_data)
    #     password = validated_data.get('password')
    #     user = User(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user