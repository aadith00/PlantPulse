from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def account(request):
    return render(request, 'my-account.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def auth(request):
    return render(request, 'autho.html' )

def user_register(request):

    errors = {}
    if request.method == 'POST':

        # first_name = request.POST['first_name'].strip()
        # last_name = request.POST['last_name'].strip()
        email = request.POST['email'].strip()
        username = request.POST['email'].strip()
        password = request.POST['password'].strip()
        cnfpass = request.POST['confirm_password'].strip()

    # ## Validation for first name
    #     if not first_name:
    #         errors['first_name'] = 'First name is required.'

    # ## Validation for last name
    #     if not last_name:
    #         errors['last_name'] = 'Last name is required.'

    ## Validation for email
        if not email:
            errors['email'] = 'Email field is required.'
        else:
            is_used = User.objects.filter(email='email').exists()
            if is_used:
                errors['email'] = 'This email is already taken.'

    ## Validation for username
        if not username:
            errors['username'] = 'Username field is required.'
        else:
            is_used = User.objects.filter(username='username').exists()
            if is_used:
                errors['username'] = 'This username is already taken.'

    ## Validation for password
        if not password:
            errors['password'] = 'Password is required.'
        if not cnfpass:
            errors['confirm_password'] = 'Password is required.'
        if password != cnfpass:
            errors['password'] = 'The passwords do not match.'

        is_valid = len(errors.keys()) == 0

        if is_valid:

            ## Creating an user

            user = User.objects.create_user(
                # first_name = first_name,
                # last_name = last_name,
                username = username,
                password = password,
            )
            
            user.save()
            login(request,user)
            return redirect('index')
    
    context = {
        'errors' : errors
    }

    return render (request, "index.html", context)

def user_login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        
        else:
            error_message = "Invalid username or password."
            return render(request, 'autho.html', {'error_message': error_message})
        
    return render (request, 'index.html')

def user_logout(request):
    logout(request)
    return redirect('auth')