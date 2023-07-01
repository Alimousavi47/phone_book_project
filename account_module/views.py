
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import CustomUserFormSerializer, LoginFormSerializer








from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from account_module.models import User
from django.contrib.auth import login, logout
from account_module.forms import ForgotPasswordForm, RegisterForm, LoginForm, ResetPasswordForm



# Create your views here.
class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'you didn\'t activate your email')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('user_panel_dashboard'))
                    else:
                        login_form.add_error('email', 'wrong password')
            else:
                login_form.add_error('email', 'did not find user')
                
                
        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)
  
class RegisterView(View):
    def get(self, request: HttpRequest):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request: HttpRequest):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get('name')
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'Email has been used before')
            else:
                new_user = User(
                    name=user_name,
                    email=user_email,
                    is_active=True,
                    username=user_email)
                new_user.set_password(user_password)
                new_user.save()
                return redirect(reverse('login_page')) 

        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)


#--------------------------------------------------------------------------------------------

# class ResetPasswordAPIView(APIView):
#     def get(self, request):
#         username = request.user.username
#         user = User.objects.filter(username=username).first()
#         if user is None:
#             return Response({"error": "User not found"}, status=404)
        
#         serializer = ResetPasswordSerializer(user)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ResetPasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             password = serializer.validated_data['password']
#             confirm_password = serializer.validated_data['confirm_password']
            
#             if password != confirm_password:
#                 return Response({'error': 'The password and confirm password do not match.'}, status=status.HTTP_400_BAD_REQUEST)
            
#             username = request.user.username
#             user = User.objects.filter(username=username).first()
#             if user is None:
#                 return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
#             user.set_password(password)
#             user.is_active = True
#             user.save()
            
#             return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(View):
    def get(self, request: HttpRequest):
        username = request.user.username # Get the username of the current user
        user: User = User.objects.filter(username=username).first() # Filter the User objects based on the username
        if user is None:
            return redirect(reverse('login_page'))
        reset_pass_form = ResetPasswordForm()

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest):
        reset_pass_form = ResetPasswordForm(request.POST)
        username = request.user.username
        user: User = User.objects.filter(username=username).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page')) ##
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm()
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)
    def post(self, request: HttpRequest):
        pass
# 
# class LogoutView(View):
#     def get(self, request):
#         username = LoginView(request)
#         if username != None:
#             logout(request)
#         return redirect(reverse('login_page'))
    

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            request.session.flush()
            response.delete_cookie('sessionid', domain='127.0.0.1', path='/')
            # response = redirect(reverse('login_page'))
            response = HttpResponseRedirect(reverse('login_page'))
            return response
        else:
            return redirect('login_page')





# Login User
class UserLoginAPI(APIView):
    def get(self, request):
        serializer = LoginFormSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = LoginFormSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful.'})
            else:
                return Response({'message': 'User not found.'}, status=400)
        return Response(serializer.errors, status=400)

# Register User
class UserRegisterAPI(APIView):
    def get(self, request):
        serializer = CustomUserFormSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserFormSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Registration successful.'})
        return Response(serializer.errors, status=400)


# Logout User
class UserLogoutAPI(APIView):
    def get(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully.'})

    def post(self, request):
        response = Response({'message': 'Logged out successfully.'})
        response.delete_cookie('jwt')
        return response
