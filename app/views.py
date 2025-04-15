from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from NutrientFinderUsingAI.evaluate import generate_nutrient
from .models import UploadedFood
def home(request):
    return render(request, "home.html")

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
        messages.success(request, "Account created successfully! You can log in now.")
        return redirect('dashboard')

    return render(request, 'Registration/signup.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')  # Redirect to homepage or dashboard after login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Stay on login page if there's an error

    return render(request, 'Registration/login.html')



@login_required
def dashboard(request):
    # Handling image upload and nutrient analysis
    if request.method == 'POST' and request.FILES.get('food_image'):
        uploaded = UploadedFood.objects.create(image=request.FILES['food_image'])
        result = generate_nutrient(uploaded.image.path)

        uploaded.content = result  # Save AI output to content field
        uploaded.save()

        messages.success(request, "Image uploaded and analyzed successfully!")
        return redirect('dashboard')

    # Fetch the latest uploaded image (most recent one)
    uploaded_image = UploadedFood.objects.all().order_by('-uploaded_at').first()

    # Pass the latest image and content to the template
    return render(request, 'Dashboard/dashboard.html', {'upload': uploaded_image})
