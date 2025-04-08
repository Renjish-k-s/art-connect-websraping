from django.shortcuts import render, redirect
from art_app.models import Usertable
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage

def homepage(request):
    return render(request,'home.html')

def register(request):
    if request.POST:
        if "register_submit" in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('opassword')
            cpassword = request.POST.get('cpassword')
            role = request.POST.get('role')

            # Input validation
            try:
                # Validate email format
                validate_email(email)
                
                # Validate password length and complexity
                if len(password) < 8:
                    messages.error(request, "Password must be at least 8 characters long", extra_tags='danger')
                    return redirect('register_page')

                # Check password confirmation
                if cpassword != password:
                    messages.error(request, "Passwords do not match!", extra_tags='danger')
                    return redirect('register_page')

                # Check if user already exists
                if Usertable.objects.filter(email=email).exists():
                    messages.error(request, "An account with this email already exists", extra_tags='warning')
                    return redirect('register_page')

                # Create new user with encrypted password
                hashed_password = make_password(password)
                Usertable_obj = Usertable(
                    name=name,
                    email=email,
                    password=hashed_password,
                    role=role,
                    status=0
                )
                Usertable_obj.save()
                
                messages.success(request, "Registration successful! Please login to continue", extra_tags='success')
                return redirect('register_page')

            except ValidationError:
                messages.error(request, "Please enter a valid email address", extra_tags='danger')
                return redirect('register_page')

        elif "login_submit" in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")

            try:
                user = Usertable.objects.get(email=email)
                
                # Verify password using check_password
                if check_password(password, user.password):
                    # Set user session
                    request.session['user_id'] = user.id
                    request.session['user_role'] = user.role
                    request.session['user_name'] = user.name

                    role_names = {
                        '0': 'User',
                        '1': 'Artist'
                    }
                    
                    # messages.success(
                    #     request, 
                    #     f"Welcome back, {user.name}! You're logged in as {role_names.get(user.role, 'Unknown')}", 
                    #     extra_tags='success'
                    # )

                    if user.role == '0':
                        if user.status=='0':
                            return redirect("user_dashboard")
                    elif user.role == '1':
                        if user.status=='0':
                            return redirect("artist_dashboard")
                        else:
                            return redirect("art_upload")

                else:
                    messages.error(request, "Invalid password. Please try again.", extra_tags='danger')
            except Usertable.DoesNotExist:
                messages.error(request, "No account found with this email.", extra_tags='danger')
            
            return redirect('register_page')

    return render(request, 'register.html')

def user_dash(request):
    return render(request, 'user_dash.html')