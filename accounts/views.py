from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib import messages

# from django.core.exceptions import ValidationError

def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password = password)

        if user is not None and user.is_active:
            login(request, user)

            if request.user.is_customer or request.user.is_supplier:
                return redirect('home')
            elif request.user.is_delivery_team:
                return redirect('delivery:home')
            elif request.user.is_manager:
                return redirect('manager:home') 
            elif request.user.is_admin:
                return redirect('kadmin:home')            
        else:
            # raise ValidationError("Credentials doesnot match. Please check your Email and Password")    
            messages.error(request, 'Credentials doesnot match OR User is inactive')
            return redirect('login')
    
    context = {'form': form}
    return render(request, 'utils/login.html', context)



