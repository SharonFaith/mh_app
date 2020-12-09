from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model, login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .email.token import activation_token
from .email.activation_email import send_activation_email
import requests
from .models import UserProfile, MhProProfile, User
from .forms import ClientSignUp, WorkerSignUp
from django.contrib.sites.shortcuts import get_current_site



def logout_view(request):
    logout(request)

    return redirect(index)




def index(request):

   
   return render(request, 'index.html')


def signupas(request):

    return render(request, 'registration/sign_up.html')

def patsignup(request):
    if request.method == 'POST':
        form = ClientSignUp(request.POST)

        if form.is_valid():
            #new_user = form.save(commit=False)
            #project.profile = current_profile
            #             
            new_user = form.save()

            send_activation_email(request, new_user)

            #return redirect('/accounts/login')
            return render(request, 'registration/accesslink.html')
    else:
        form = ClientSignUp()

    return render(request, 'registration/signup_form.html', {'form': form})

def mhprosignup(request):
    if request.method == 'POST':
        form = WorkerSignUp(request.POST)



        if form.is_valid():    
            new_user = form.save()
            workplace = form.cleaned_data['work_place']
            id_num = form.cleaned_data['id_or_passport_number']
            workcontact = form.cleaned_data['work_place_contact']
            title = form.cleaned_data['title']
            

            MhProProfile.objects.filter(user=new_user).update(work_place = workplace, id_num=id_num, title=title, work_place_contact=workcontact)
            #return redirect('/accounts/login')
            return render(request, 'registration/accesslinklater.html')
        
    else:
        form = WorkerSignUp()

    return render(request, 'registration/mhproform.html', {'form': form})



def activate_account(request, uid, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        return redirect('/accounts/login')

    else:
        return HttpResponse('no user')
