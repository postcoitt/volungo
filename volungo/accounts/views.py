from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import EmailOrUsernameAuthForm

def login_view(request):
    form = EmailOrUsernameAuthForm()

    if request.method == 'POST':
        form = EmailOrUsernameAuthForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')

    return render(request, 'accounts/login.html', {'form': form})
