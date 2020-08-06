from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserReigisterForm

def register(request):
    if request.method == "POST":
        form = UserReigisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for {0}. You can now log in'.format(username))
            return redirect('login')
    else:
        form = UserReigisterForm()

    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)

