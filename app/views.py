from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecord
from .models import Record


def home(request):
    
    # pass the records if the user is logged in
    records = Record.objects.all()
    # check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, 'The password is incorrect!')
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Successfully Logged Out...")
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def record(request, id):
    if request.user.is_authenticated:
        try:
            record = Record.objects.get(pk=id)
            return render(request, 'record.html', {'record': record})
        except Record.DoesNotExist:
            messages.error(request, "The ID does not match any Record...")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to view the record")
        return redirect('home')
    
def delete_record(request, id):
    if request.user.is_authenticated:
        record = Record.objects.get(pk=id)
        record.delete()
        messages.success(request, "Record Deleted")
        return redirect('home')
    else:
        messages.error(request, "You must be logged in to delete a record")
        return redirect('home')

def update_record(request, id):
    if request.user.is_authenticated:
        current_record = Record.objects.get(pk=id)
        form = AddRecord(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "The record has been successfully updated!")
            return redirect('home')
        return render(request, "update_record.html", {'form': form, 'record': current_record})
    else:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect('home')


def add_record(request):
    if request.user.is_authenticated:
        form = AddRecord(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "the Record is successfully added!")
            return redirect('home')
        return render(request, "add_record.html", {'form': form})
    else:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect('home')
