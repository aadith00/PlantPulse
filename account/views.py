from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Customer, Farmer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import default_storage

def update_profile_picture(request):
    try:
        customer = request.user.customer_profile  # Adjusted to use the correct related_name 'customer_profile'
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect('my-account')  # Redirect back to account page or an appropriate page

    if request.method == 'POST':
        # Check if 'profile_picture' is in request.FILES
        if request.FILES.get('profile_picture'):
            customer.profile_picture = request.FILES['profile_picture']
            customer.save()
            messages.success(request, "Profile picture updated successfully.")
        else:
            messages.error(request, "No file uploaded. Please select a picture to upload.")
    else:
        messages.error(request, "Invalid request method. Please try again.")

    return redirect('my-account')  # Adjust redirect as needed

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
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        cnfpass = request.POST.get('confirm_password', '').strip()
        role = request.POST.get('role', '').strip()  # Capture the role from the form

        # Validation for email
        if not email:
            errors['email'] = 'Email field is required.'
        else:
            is_used = User.objects.filter(email=email).exists()
            if is_used:
                errors['email'] = 'This email is already taken.'

        # Validation for username
        if not username:
            errors['username'] = 'Username field is required.'
        else:
            is_used = User.objects.filter(username=username).exists()
            if is_used:
                errors['username'] = 'This username is already taken.'

        # Validation for password
        if not password:
            errors['password'] = 'Password is required.'
        if not cnfpass:
            errors['confirm_password'] = 'Confirm password is required.'
        if password != cnfpass:
            errors['password'] = 'The passwords do not match.'

        # Validation for role selection
        if role.lower() not in ['farmer', 'customer']:
            errors['role'] = 'Please select a valid role.'

        is_valid = len(errors) == 0

        if is_valid:
            # Create the User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()

            # Register user in the appropriate table based on role
            if role.lower() == 'farmer':
                Farmer.objects.create(user=user)
            elif role.lower() == 'customer':
                Customer.objects.create(user=user)

            # Log the user in and redirect
            login(request, user)
            return redirect('index')
    
    context = {
        'errors': errors
    }

    return render(request, "index.html", context)

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


@login_required
def update_customer_info(request):
    customer = get_object_or_404(Customer, user=request.user)

    if request.method == 'POST':
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.address = request.POST.get('address')
        customer.city = request.POST.get('city')
        customer.country = request.POST.get('country')
        customer.zip_code = request.POST.get('zip_code')
        customer.phone_number = request.POST.get('phone_number')
        
        customer.save()
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('profile')

    return render(request, 'profile.html', {'customer': customer})