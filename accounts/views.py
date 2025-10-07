from django.shortcuts import render, redirect
from django.contrib.auth import login
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# 📝 Registration View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# 🏠 Homepage View
@login_required
def home_view(request):
    return render(request, 'home.html')
