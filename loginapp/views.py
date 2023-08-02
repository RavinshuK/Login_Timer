from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.utils import timezone
from .models import UserLoginHistory
from datetime import datetime
from django.contrib import messages


# Create your views here.
def index(request):
    print(request.user)
    if request.user.is_anonymous:
        return redirect("/login") 
    return render(request, 'index.html')

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)            
           
            # Store login time as string in session
            login_time = timezone.now().isoformat()
            request.session['login_time'] = login_time
          
            return redirect("/")

        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')
        

    return render(request, 'login.html')

def logoutUser(request):
    
    # Calculate the duration
    login_time = request.session.get('login_time')
    if login_time:
        logout_time = timezone.now()
        user = request.user
        login_time = datetime.fromisoformat(login_time)
        duration = (logout_time - login_time).total_seconds()
        
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        message = f"Goodbye, {user.username}! You were logged in for {minutes} minutes and {seconds} seconds."

        messages.info(request, message)

        # Update the user's login history
        user_login_history = UserLoginHistory.objects.get_or_create(user=user)[0]
        user_login_history.update_duration(duration)

    logout(request)
    return redirect("/login")