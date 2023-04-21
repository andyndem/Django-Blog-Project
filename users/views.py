from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
# from .models import Post

# Create your views here.


def register(request):
        if request.method == 'POST':  # if the request is a 'post' then it will create a form
            form = UserRegisterForm(request.POST)
            if form.is_valid():
              form.save()
              username = form.cleaned_data.get('username')
              messages.success(request, f'Account created for {username}! You can now login')
              return redirect('login')
            else:
              messages.warning(request, f'Invalid entry. Account not created!')
        else:
            form = UserRegisterForm()  # anything not a post request it will create a blank form
        return render(request, 'users/register.html', {'form': form})   


@login_required
def profile(request):
  if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, f'Account updated successfully!')
        return redirect('profile')
    else:
        messages.warning(request, f'Account update failed!')
      
  else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
  
    context = {
        'u_form': u_form,
        'p_form': p_form
      }
    return render(request, 'users/profile.html', context)
  

