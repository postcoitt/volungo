# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    # Якщо користувач вже залогінений, редіректимо його на свій профіль
    if request.user.is_authenticated:
        return redirect('my_profile')

    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # username або email
        password = request.POST.get('password')

        user_obj = None
        # шукаємо користувача по username
        try:
            user_obj = User.objects.get(username=identifier)
        except User.DoesNotExist:
            # якщо не знайшли, шукаємо по email
            try:
                user_obj = User.objects.get(email=identifier)
            except User.DoesNotExist:
                user_obj = None

        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('my_profile')  # редірект після успішного входу

        # Якщо логін не вдалий
        messages.error(request, "Невірний логін або пароль")

    # GET запит або невдалий POST
    return render(request, 'accounts/login.html')
