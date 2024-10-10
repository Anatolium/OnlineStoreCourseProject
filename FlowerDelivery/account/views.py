from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.views.decorators.http import require_POST


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
@require_POST
def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    print('Вы успешно вышли из системы')
    return redirect('/')


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаём новый объект пользователя, но пока не сохраняем его
            new_user = user_form.save(commit=False)
            # Устанавливаем выбранный пароль; для безопасности
            # метод хеширует пароль перед его сохранением в базе данных
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем объект User
            new_user.save()
            # Создаём профиль пользователя
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
