from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User


def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponse('Authenticated successfully')
			else:
				return HttpResponse('Disabled account')
		else:
			return HttpResponse('Invalid login')
	else:
		form = LoginForm()
	return render(request, 'registration/login.html', {'form': form})


class MyRegisterFormView(FormView):
	form_class = UserCreationForm
	success_url = reverse_lazy("login")
	template_name = "account/register.html"

	def form_valid(self, form):
		form.save()
		return super(MyRegisterFormView, self).form_valid(form)

	def form_invalid(self, form):
		return super(MyRegisterFormView, self).form_invalid(form)


# def register(request):
# 	if request.method == 'POST':
# 		user_form = UserRegistrationForm(request.POST)
# 		if user_form.is_valid():
# 			# Создаем нового пользователя, но пока не сохраняем в базу данных.
# 			new_user = user_form.save(commit=False)
# 			# Задаем пользователю зашифрованный пароль.
# 			new_user.set_password(user_form.cleaned_data['password'])
#
# 			# Сохраняем пользователя в базе данных.
# 			new_user.save()
# 			return render(request, 'registration/login.html', {'new_user': new_user})
# 	else:
# 		user_form = UserRegistrationForm()
# 	return render(request,'account/register.html',{'user_form': user_form})



@login_required
def edit_profile(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
		return render(request, 'account/edit_profile.html',
					  {'user_form': user_form, 'profile_form': profile_form})


