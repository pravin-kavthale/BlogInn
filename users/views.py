from django.shortcuts import render,redirect
from django.contrib import messages
from .form import UserRegistrationForm
from django.contrib.auth.forms import UserCreationForm
from .form import UserUpdateForm, UpdateProfileForm

from django.contrib.auth.decorators import login_required

def register(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your account has been created successfully! You can now log in.")
            return redirect('login')
    else:
        form =UserRegistrationForm()

    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    return render(request,'users/profile.html')

@login_required
def profileUpdate(request):
    if request.method=="POST":
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=UpdateProfileForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=UpdateProfileForm(instance=request.user.profile) 

    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/profileUpdate.html',context)
