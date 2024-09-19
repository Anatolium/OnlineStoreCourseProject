from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Пользователь аутентифицируется по базе данных методом authenticate()
            user = authenticate(request, username=cd['username'], password=cd['password'])
            # Пользователь аутентифицирован
            if user is not None:
                # Пользователь активен
                if user.is_active:
                    # Пользователь входит в систему (login() задает пользователя в текущем сеансе)
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})
