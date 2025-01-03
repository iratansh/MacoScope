"""
This file contains the views for the authentication API
"""

from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import get_connection, EmailMessage
import json, smtplib
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str 
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate
import logging

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
    domain = 'http://0.0.0.0:8080'
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
    
        if email.send(fail_silently=False):
            messages.success(request, 'Please confirm your email address to complete the registration')
            return True
        else:
            messages.error(request, 'Email not sent')
            return False
    except smtplib.SMTPDataError as e:
        messages.error(request, f"Error sending email: {str(e)}")
        return False

@api_view(['GET'])
def check_authentication_status(request):
    print("Session ID in dashboard:", request.session.session_key)
    return Response({
        "is_authenticated": request.user.is_authenticated,
        "user": request.user.username if request.user.is_authenticated else None
    }, status=200)

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
            user = User.objects.using('authentication').get(email=email)
            if not user.is_active:  # Check if user is already activated
                if activate_email(request, user, email):  # Send activation email
                    return JsonResponse({'success': True, 'message': 'A new activation link has been sent to your email.'})
                else:  # Failed to send activation email
                    return JsonResponse({'success': False, 'message': 'An account already exists with this email. Please log in.'}, status=500)
            else:  # User is already activated
                return JsonResponse({'success': False, 'message': 'This account is already activated. Please log in.'}, status=400)
        except User.DoesNotExist:  # User does not exist
            user = User.objects.db_manager('authentication').create_user(username=username, email=email, password=password, is_active=False)
            
            if activate_email(request, user, email):  # Send activation email
                return JsonResponse({'success': True, 'message': 'Please check your email to verify your account.'})
            else:  # Failed to send activation email
                return JsonResponse({'success': False, 'message': 'Failed to send verification email. Please try again later.'}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        # Fetch the user from the 'authentication' database
        user = User.objects.using('authentication').get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        # Save the user using the 'authentication' database
        user.save(using="authentication")
        messages.success(request, 'Your email has been verified.')
        return HttpResponse('Thank you for confirming your email. Your account is now activated.')   
    else:
        messages.warning(request, 'The link is invalid.')
        return HttpResponse('Activation link is invalid!', status=400)

@csrf_exempt        
@api_view(['POST'])
def login_user(request):
    logging.info("Login API called")
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'success': False, 'message': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    User = get_user_model()
    
    try:
        user = User.objects.using('authentication').get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Account does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    if user.check_password(password):
        if user.is_active:
            authenticated_user = authenticate(request=request, username=user.username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                
                # Save the session
                request.session.save()

                # Retrieve session key
                session_key = request.session.session_key

                # Set the session ID in the response cookie
                response = JsonResponse({
                    'success': True,
                    'is_active': True,
                    'message': 'Login successful.',
                    'username': user.username,
                    'session_key': session_key
                }, status=status.HTTP_200_OK)

                # Set the sessionid cookie
                response.set_cookie('sessionid', session_key, httponly=True, samesite='Lax')
                return response
            else:
                return JsonResponse({'success': False, 'message': 'Authentication failed.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'success': False, 'message': 'Account is not activated.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_protect
@api_view(['POST'])
def logout_user(request):
    logout(request)
    
    # Send back a success message
    return JsonResponse({
        'success': True,
        'is_active': False,
        'message': 'Logout successful.'
    }, status=status.HTTP_200_OK)

@csrf_exempt
def send_password_reset_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email: 
                return JsonResponse({'error': 'Email field is required.'}, status=400)
            
            user = get_object_or_404(User, email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f'https://www.mmacroscope.me/reset-password/{uid}/{token}/'


            email_message = EmailMessage(
                'MacroScope: Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'i.ratanshi12@outlook.com',  
                [email],  
            )
            email_message.send(fail_silently=False)

            return JsonResponse({'success': True})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': 'User not found or other error occurred.'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def reset_password(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return JsonResponse({'success': False, 'message': 'Invalid token or user'})

        if default_token_generator.check_token(user, token):
            # Get new password from the POST request
            data = json.loads(request.body)
            new_password = data.get('password')

            if not new_password:
                return JsonResponse({'success': False, 'message': 'Password field is required'})

            # Set the new password and save the user
            user.set_password(new_password)
            user.save(using='authentication')
            return JsonResponse({'success': True, 'message': 'Password reset successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid token'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def update_security(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = request.user.id  
        new_email = data.get('email')
        new_password = data.get('password')

        if not new_email or not new_password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        try:
            # Check if the new email is already in use by another user
            if User.objects.using('authentication').filter(email=new_email).exclude(id=user_id).exists():
                return JsonResponse({'error': 'email_in_use'}, status=400)

            # Get the current user
            user = User.objects.get(id=user_id, using='authentication')
            # Set the new password
            user.set_password(new_password)

            # If the email has changed, send a verification email but don't update the email in the DB yet
            if user.email != new_email:
                if send_verification_email(request, user, new_email):
                    # Save new email in a separate field, like user.profile or a pending changes table
                    user.profile.pending_email = new_email
                    user.profile.save(using='authentication')
                    return JsonResponse({'success': True, 'message': 'Please verify your new email to complete the update.'}, status=200)
                else:
                    return JsonResponse({'error': 'Failed to send verification email'}, status=500)

            user.save(using='authentication')
            return JsonResponse({'success': True, 'message': 'Security information updated successfully'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# Function to send a verification email
def send_verification_email(request, user, to_email):
    mail_subject = 'Activate your user account'
    domain = 'https://www.mmacroscope.me'
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
            messages.success(request, 'Please confirm your email address to complete the update.')
            return True
        else:
            messages.error(request, 'Email not sent')
            return False
    except smtplib.SMTPDataError as e:
        messages.error(request, f"Error sending email: {str(e)}")
        return False

def verify_email_change(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.using('authentication').get(pk=uid)

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            # Update the user's email with the pending email
            if user.profile.pending_email:
                user.email = user.profile.pending_email
                user.profile.pending_email = None
                user.save(using='authentication')
                user.profile.save(using='authentication')
                messages.success(request, 'Your email has been updated successfully.')
                return JsonResponse({'success': True}, status=200)
            else:
                return JsonResponse({'error': 'No email change pending.'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid token.'}, status=400)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return JsonResponse({'error': 'Invalid request.'}, status=400)

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

def inspect_session(session_key):
    session = SessionStore(session_key=session_key)
    return session.get('_auth_user_id', None), session.get('_auth_user_backend', None)


from django.utils import timezone

@api_view(['POST'])
def get_user_details(request):
    print("User authenticated:", request.user.is_authenticated)

    if request.user.is_authenticated:
        # If authenticated via request.user, return user details
        return Response({
            'full_name': request.user.username,
            'email': request.user.email,
            'member_since': request.user.date_joined.strftime('%Y-%m-%d'),
        }, status=status.HTTP_200_OK)

    # Check for session ID in custom header
    session_id = request.headers.get('X-Session-ID')
    if session_id:
        # Query session data from 'authentication' database
        session = Session.objects.using('authentication').filter(
            session_key=session_id, expire_date__gt=timezone.now()
        ).first()
        if session:
            # Decode session data to get user_id
            session_data = session.get_decoded()
            user_id = session_data.get('_auth_user_id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    return Response({
                        'full_name': user.username,
                        'email': user.email,
                        'member_since': user.date_joined.strftime('%Y-%m-%d'),
                    }, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # If no valid session or authentication found
    return Response({
        'success': False,
        'message': 'User is not authenticated.'
    }, status=status.HTTP_401_UNAUTHORIZED)


