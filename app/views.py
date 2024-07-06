from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .forms import SignUpForm, AddRecord
from .models import Record
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
# import for api
from rest_framework import generics
from .serializers import RecordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

# class customization

class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name ='password_reset_form.html'
    success_url = reverse_lazy('home')
    success_message = "We've sent you the reset password email. You should recieve it shortly."

class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('home')
    success_message = "the password has been reset successfully."

# setting up the API
class RecordList(generics.ListAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [AllowAny]

class  RecordListCreate(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]

class RecordRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]

# authentication and authorization
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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, 'Please confirm your email address to complete the Registration')
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid =(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid')
        return redirect('home')

# app urls
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

def youtube(request):
    return render(request, 'youtube.html')
