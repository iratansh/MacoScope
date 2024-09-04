from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .serializers import RegisterSerializer
from django.core.mail import get_connection, EmailMessage
import json, smtplib

def activate_email(request, user, to_email):
    try:
        User = get_user_model()
        user = User.objects.using('authentication').get(email=to_email)
        print(user.is_active)
    except User.DoesNotExist:
        print('User does not exist')

    if user.is_active:
        messages.info(request, 'Your email is already activated.')
        return False

    mail_subject = 'Activate your user account'
    domain = 'http://127.0.0.1:8080'
    message = render_to_string('activation_email.html', {
        'user': user.username,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    
    email = EmailMessage(mail_subject, message, to=[to_email])
    try:
        connection = get_connection()
        email.connection = connection
        
        if email.send():
            messages.success(request, 'Please confirm your email address to complete the registration')
            return True
        else:
            messages.error(request, 'Email not sent')
            return False
    except smtplib.SMTPDataError as e:
        messages.error(request, f"Error sending email: {str(e)}")
        return False


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'success': False, 'message': 'Email and password are required.'}, status=400)

        username = email.split('@')[0]

        try:
            user = User.objects.get(email=email)
            if not user.is_active: # check if user is already activated
                if activate_email(request, user, email): # send activation email
                    return JsonResponse({'success': True, 'message': 'A new activation link has been sent to your email.'})
                else: # failed to send activation email (user already exists & is active)
                    return JsonResponse({'success': False, 'message': 'An account already exists with this email. Please log in.'}, status=500)
            else: # user is already activated
                return JsonResponse({'success': False, 'message': 'This account is already activated. Please log in.'}, status=400)
        except User.DoesNotExist: # user does not exist
            user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
            if activate_email(request, user, email): # send activation email
                return JsonResponse({'success': True, 'message': 'Please check your email to verify your account.'})
            else: # failed to send activation email
                return JsonResponse({'success': False, 'message': 'Failed to send verification email. Please try again later.'}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(using="authentication")
        messages.success(request, 'Your email has been verified.')
        return HttpResponse('Thank you for confirming your email. Your account is now activated.')   
    else:
        messages.warning(request, 'The link is invalid.')
        return HttpResponse('Activation link is invalid!', status=400)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

    # users are not being added to the 'authentication' database, instead being added to the 'default' database;
    # delete the default database and change the saving of the users to 'authentication'
    # implement forgot password functionality
    # return a response for if the password does not match the email

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'success': False, 'message': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    print(f"Email: {email}, Password: {password}")

    User = get_user_model()

    try:
        # Attempt to retrieve the user from the 'authentication' database
        user = User.objects.using('authentication').get(email=email)
    except User.DoesNotExist:
        # Account doesn't exist
        print("User does not exist")
        return JsonResponse({'success': False, 'message': 'Account does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    if user.check_password(password):
        if user.is_active:
            # Successful login
            return JsonResponse({'success': True, 'is_active': True, 'message': 'Login successful.'}, status=status.HTTP_200_OK)
        else:
            # Account exists but is not activated
            return JsonResponse({'success': False, 'is_active': False, 'message': 'Account is not activated. Please check your email to activate your account.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        # Password is incorrect
        return JsonResponse({'success': False, 'message': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
