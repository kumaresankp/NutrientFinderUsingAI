from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from NutrientFinderUsingAI.evaluate import generate_nutrient
from .models import UploadedFood
import json

def home(request):
    if request.user.is_authenticated:  # Correct way to check if the user is logged in
        return redirect('dashboard')  # Redirect to the dashboard if the user is authenticated
    return render(request, "home.html")

# Sign up view
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        list(messages.get_messages(request))
        messages.success(request, "Account created successfully! You can log in now.")
        return redirect('login')  # After signing up, redirect to login

    return render(request, 'Registration/signup.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            list(messages.get_messages(request))
            messages.success(request, "Login successful!")
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            list(messages.get_messages(request))
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Stay on login page if there's an error

    return render(request, 'Registration/login.html')

# Dashboard view (for uploading and displaying the latest image)
@login_required
def dashboard(request):
    if request.method == 'POST' and request.FILES.get('food_image'):
        uploaded = UploadedFood.objects.create(
            user=request.user,
            image=request.FILES['food_image']
        )

        result = generate_nutrient(uploaded.image.path)
        uploaded.content = result
        uploaded.save()

        list(messages.get_messages(request))
        messages.success(request, "Image uploaded and analyzed successfully!")
        return redirect('dashboard')

    uploaded_image = UploadedFood.objects.filter(user=request.user).order_by('-uploaded_at').first()

    if uploaded_image and uploaded_image.content:
        try:
            parsed = json.loads(uploaded_image.content)
            # If it's a list, get the first element
            if isinstance(parsed, list) and parsed:
                uploaded_image.parsed_content = parsed[0]
            else:
                uploaded_image.parsed_content = parsed
        except json.JSONDecodeError:
            uploaded_image.parsed_content = {}
    else:
        uploaded_image = None

    return render(request, 'Dashboard/dashboard.html', {'upload': uploaded_image})



# Logout view
def user_logout(request):
    logout(request)

    messages.success(request, "You have been logged out successfully!")
    return redirect('login')  # Make sure 'login' is your URL name for the login page

@login_required
def uploaded_images(request):
    # Filter uploaded images by the logged-in user
    uploaded_images = UploadedFood.objects.filter(user=request.user).order_by('-uploaded_at')

    # Parse the content if it exists and pass it to the template
    for uploaded in uploaded_images:
        if uploaded.content:
            try:
                parsed = json.loads(uploaded.content)

                # If it's a list with at least one item, get the first item
                if isinstance(parsed, list) and parsed:
                    uploaded.parsed_content = parsed[0]
                else:
                    uploaded.parsed_content = parsed
            except json.JSONDecodeError:
                uploaded.parsed_content = {}
        else:
            uploaded.parsed_content = {}

    return render(request, 'Dashboard/uploaded_images.html', {'uploads': uploaded_images})
