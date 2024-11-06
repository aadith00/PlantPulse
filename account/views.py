from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Customer, Farmer
from shop.models import Order, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from custom_admin.models import Admin

# Create your views here.
def account(request):
    # Get the customer associated with the logged-in user, create if not exists
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)

    # Get all orders associated with the customer
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'customer': customer,
        'orders': orders  # Pass orders to the template
    }

    return render(request, 'my-account.html', context)



# Add Review view
def add_review(request,id):
    if request.method == 'POST':
        # form = ReviewForm(request.POST)
        order=Order.objects.get(order_id=id)
        rating = request.POST.get('rating', '').strip()
        review = request.POST.get('review_text', '').strip()

        review=Review.objects.create(
            order=order,
            rating=rating,
            review=review,
        )
        review.save()
        return redirect('my-account')
    else:

        return render(request, 'add_review.html',)


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
        print(role)

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

            # Redirect based on user type
            if Admin.objects.filter(user=user).exists():
                return redirect('dashboard')
            elif Farmer.objects.filter(user=user).exists():
                return redirect('index')
            elif Customer.objects.filter(user=user).exists():
                return redirect('index')
            else:
                messages.error(request, "Account type not recognized.")
                return redirect('autho.html')
        else:
            error_message = "Invalid username or password."
            return render(request, 'autho.html', {'error_message': error_message})
        
    return render(request, 'autho.html')

def user_logout(request):
    logout(request)
    return redirect('auth')

@login_required
def update_general_info(request):
    customer = get_object_or_404(Customer, user=request.user)
    
    if request.method == 'POST':
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.phone_number = request.POST.get('phone_number')
        customer.save()
        
        messages.success(request, "Your general information has been updated successfully.")
        return redirect('my-account')
    
    return render(request, 'my-account.html', {'customer': customer})

@login_required
def update_address(request):
    customer = get_object_or_404(Customer, user=request.user)
    
    if request.method == 'POST':
        # Get the form data from the request
        address = request.POST.get('address')
        address2 = request.POST.get('address2', '')  # Optional field
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        
        # Ensure required fields are present
        if address and city and state and country and zip_code:
            # Update customer address information
            customer.address = address
            customer.address2 = address2
            customer.city = city
            customer.state = state
            customer.country = country
            customer.zip_code = zip_code
            customer.save()
            
            messages.success(request, "Your address has been updated successfully.")
            return redirect('my-account')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'my-account.html', {'customer': customer})

@login_required
def update_profile_picture(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect('my-account')  # Adjust redirect as needed

    if request.method == 'POST':
        if request.FILES.get('profile_picture'):
            customer.profile_picture = request.FILES['profile_picture']
            customer.save()
            messages.success(request, "Profile picture updated successfully.")
        else:
            messages.error(request, "No file uploaded. Please select a picture to upload.")
    else:
        messages.error(request, "Invalid request method. Please try again.")

    return redirect('my-account')