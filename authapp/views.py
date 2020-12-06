from django.contrib import auth
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserAuthenticationForm, ShopUserRegisterForm, ShopUserUpdateForm, \
    ShopUserProfileUpdateForm
from authapp.models import ShopUser, ShopUserProfile


def login(request):
    redirect_url = request.GET.get('next', None)

    if request.method == 'POST':
        form = ShopUserAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                redirect_url = request.POST.get('redirect_url', None)
                auth.login(request, user)
                if redirect_url:
                    return HttpResponseRedirect(redirect_url)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserAuthenticationForm()
        # form = ShopUserAuthenticationForm(data=request.GET)
    context = {
        'page_title': 'аутентификация',
        'form': form,
        'redirect_url': redirect_url,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def user_register(request):
    if request.method == 'POST':
        form = ShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.send_verify_mail()
            # auth.login(request, user)
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        form = ShopUserRegisterForm()
    context = {
        'page_title': 'регистрация',
        'form': form
    }
    return render(request, 'authapp/register.html', context)


def user_profile(request):
    if request.method == 'POST':
        user = ShopUserUpdateForm(request.POST, request.FILES, instance=request.user)
        user_profile = ShopUserProfileUpdateForm(request.POST, request.FILES,
                                                instance=request.user.shopuserprofile)
        if user.is_valid() and user_profile.is_valid():
            user.save()
            # user_profile.save()
            return HttpResponseRedirect(reverse('main:index'))
    else:
        user = ShopUserUpdateForm(instance=request.user)
        user_profile = ShopUserProfileUpdateForm(instance=request.user.shopuserprofile)
    context = {
        'page_title': 'профиль',
        'form': user,
        'user_profile_form': user_profile
    }
    return render(request, 'authapp/profile.html', context)


def user_verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')
        else:
            print(f'error activation user: {user}')
        return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main'))


@receiver(post_save, sender=ShopUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # print('ShopUser created')
        ShopUserProfile.objects.create(user=instance)
    else:
        # print('ShopUser modified')
        instance.shopuserprofile.save()
