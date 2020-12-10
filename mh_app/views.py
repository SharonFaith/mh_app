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
from .models import UserProfile, MhProProfile, User, Post
from .forms import ClientSignUp, WorkerSignUp, UpdateProfileMhp, UpdateProfileUser, AddPost, RatingsForm, ReviewForm
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
            

            MhProProfile.objects.filter(user=new_user).update(work_place = workplace, id_number=id_num, title=title, work_place_contact=workcontact)
            #return redirect('/accounts/login')
            return render(request, 'registration/accesslinklater.html')
        
    else:
        form = WorkerSignUp()

    return render(request, 'registration/mhproform.html', {'form': form})


def prolist(request):
    profiles = MhProProfile.objects.all().order_by('-id')

    return render(request, 'prolist.html', {'pro_profiles':profiles})

def userlist(request):
    profiles = UserProfile.objects.all().order_by('-id')

    return render(request, 'userlist.html', {'user_profiles':profiles})


@login_required(login_url='/accounts/login')
def profile(request, id):

   
    logged_user = request.user
    current_user = User.objects.filter(id = id).first()
    the_title = ''
    user_profile = None
    overall_mean = 0
    person_id = id
    ratings = None
    reviews = None
    posts = None
    reviews_written = None

    if current_user.is_staff:
        print(current_user.is_staff)
        user_profile = current_user.mhproprofile
        if user_profile.title:
            if user_profile.title == '1':
                the_title = 'Prof.'
            if user_profile.title == '2':
                the_title = 'Dr.'
            if user_profile.title == '3':
                the_title = 'Ms.'
            if user_profile.title == '4':
                the_title = 'Mrs.'
            if user_profile.title == '5':
                the_title = 'Mr.'

        ratings = user_profile.ratings.all()
        print('ratings')
        print(ratings)
        the_ratings = []
        for rating in ratings:
            the_ratings.insert(0, rating)

        
        num_ratings = user_profile.ratings.all().count()

        rating_total = []
        for rating in ratings:
            rating_total.append(rating.overall)

        sum_ratings = sum(rating_total)
        
        if sum_ratings != 0:
            overall_mean = sum_ratings/num_ratings
            rounded = round(overall_mean, 2)
            overall_mean = rounded
        else:
            overall_mean = 0

        print(overall_mean)
        reviews = user_profile.reviews.all()

        posts = user_profile.user.posts.all()



    elif current_user.is_superuser:
        user_profile = None


    else:
        user_profile = current_user.clientprofile
        posts = user_profile.user.posts.all()
        reviews_written = user_profile.user.reviews_written.all()


    print(user_profile)
  

  

    #posts = Post.objects.all().order_by('-id')
   
   
    return render(request, 'profile/profile.html', {'user_profile': user_profile, 'current_user':current_user, 'logged_user':logged_user, 'the_title': the_title, 'overall_rating':overall_mean, 'posts':posts, 'reviews':reviews, 'reviews_written':reviews_written, 'ratings':ratings })





@login_required(login_url='/accounts/login')
def update_profile(request):

    current_user = request.user
   
    if current_user.is_staff:
        user_profile = current_user.mhproprofile
        if request.method == 'POST':
            form = UpdateProfileMhp(request.POST, request.FILES)

            if form.is_valid():
            #  new_pic = form.cleaned_data['profile_photo']
                # new_bio = form.cleaned_data['profile_bio']
                # print(current_profile.id)
                
                # Profile.objects.filter(id = current_profile.id).update(profile_pic = new_pic, bio = new_bio)
                
                new_profile = form.save(commit=False)
                # fake_user = User(username = 'fake-user2', first_name='fake', last_name='user')
                # fake_user.save(commit=False)
                # new_profile.user = fake_user
                # new_profile.save(commit=False)
                MhProProfile.objects.filter(id = user_profile.id).update(profile_pic = new_profile.profile_pic, bio = new_profile.bio, work_place = new_profile.work_place, work_place_contact = new_profile.work_place_contact, phone_number= new_profile.phone_number, education_level = new_profile.education_level, id_number = new_profile.id_number, title = new_profile.title )

                # fake_user.delete()
                # image_profile.delete()
                


            return redirect(profile, id = current_user.id)
        else:
            form = UpdateProfileMhp()
   
    else:
        user_profile = current_user.clientprofile


        if request.method == 'POST':
            form = UpdateProfileUser(request.POST, request.FILES)

            if form.is_valid():
                new_profile = form.save(commit=False)
                # fake_user = User.objects.create(username = 'fake-user2', first_name='fake', last_name='user')
                
                # new_profile.user = fake_user
                # new_profile.save()
                
                UserProfile.objects.filter(id = new_profile.id).update(profile_pic = new_profile.profile_pic, bio = new_profile.bio)
                    # fake_user.delete()
                    # new_profile.delete()

            return redirect(profile, id = current_user.id)
        else:
            form = UpdateProfileUser()
   
    return render(request, 'profile/update_profile.html', {'form': form})

@login_required(login_url='/accounts/login')
def add_post(request):
        current_user = request.user
        if request.method == 'POST':
            form = AddPost(request.POST)

            if form.is_valid():

                new_post = form.save(commit=False)
                new_post.user = current_user
                new_post.save()


            return redirect('/')
        form = AddPost()

        return render(request, 'addpost.html', {'form': form})

@login_required(login_url='/accounts/login')
def add_review(request, pro_id):
        current_user = request.user
        the_id = pro_id
    # project_id = proj_id
        current_profile = MhProProfile.objects.filter(id = the_id).first()
        user_reviewed = current_profile.user
        phrase = ''
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            formtrue=False
            if form.is_valid():

                new_review = form.save(commit=False)
                new_review.user = current_user
                new_review.person_reviewing  = current_profile
                new_review.save()


            
        else:
            form = ReviewForm()
            formtrue = True

        return render(request, 'addreview.html', {'form':form, 'the_id': the_id, 'phrase':phrase, 'formtrue': formtrue, 'current_profile': current_profile})

@login_required(login_url='/accounts/login')
def rate_worker(request, profile_id):
    current_user = request.user
    the_id = profile_id
    # project_id = proj_id
    current_profile = MhProProfile.objects.filter(id = the_id).first()
    print("hello")
    print(current_profile.id)
    phrase = ''


    try:
        if request.method == 'POST':
        
            form = RatingsForm(request.POST)
            formtrue=False
            if form.is_valid():
                new_rate = form.save(commit=False)
                new_rate.user_rating = current_user
                new_rate.person_rated = current_profile
                
                
                
                ratings = float(new_rate.ratings_out_of_10)
                # usability = float(new_rate.usability)
                # content = float(new_rate.content)

               
                # print(ratings)
               
                # totalrates =  [design, usability, content]
                # print(totalrates)
                # rates = sum(totalrates)
                # total_average = rates/3

                new_rate.overall = ratings

                new_rate.save()
       
    
            #return redirect(single_project, proj_id = the_id )
        else:
            form = RatingsForm()
            formtrue = True
  
             
    except IntegrityError as e:
        phrase = 'You can only rate a post once' 
        #formtrue = True

    return render(request, 'rateform.html', {'form':form, 'the_id': the_id, 'phrase':phrase, 'formtrue': formtrue, 'current_profile': current_profile})




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

