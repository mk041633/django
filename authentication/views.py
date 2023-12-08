from django.shortcuts import render, redirect
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth
from . models import User
import threading
import json
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from . utils import token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect, JsonResponse

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send(fail_silently=False)

def EmailValidationView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data['email']
        for char in email:
            if char.isupper():
                return JsonResponse({'email_error': 'Адрес электронной почты недействителен'})
        if not validate_email(email):
            return JsonResponse({'email_error': 'Адрес электронной почты недействителен'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Это электронное письмо используется, выберите другое.'})
        return JsonResponse({'email_valid': True})

def UsernameValidationView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        for char in username:
            if char.isdigit():
                return JsonResponse({'username_error': 'Цифровые символы не допускаются.'})
        exists = User.objects.filter(username=username).exists()
        if exists:
            return JsonResponse({'username_error': 'Простите! Выберите другое '})
        return JsonResponse({'username_valid': True})

def RegistrationView(request):
    if request.method == "GET":
        return render(request, 'authentication/register.html')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Слишком короткий пароль')
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email, is_staff=True)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user),
                }
                link = reverse('nactivate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})
                email_subject = 'Activate your account'
                activate_url = 'https://'+current_site.domain+link
                email = EmailMessage(
                    email_subject,
                    'Здравствуйте '+user.username + ', мы рады, что вы зарегистрировали у нас свою учетную запись! Пожалуйста, перейдите по ссылке ниже, чтобы активировать свою учетную запись. Надеемся, что у вас будет замечательный опыт работы с нами! \n'+activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                EmailThread(email).start()
                messages.success(request, 'Учетная запись успешно создана!! Пожалуйста, проверьте свою почту, чтобы активировать учетную запись. Не забудьте также проверить папку со спамом.')
                return redirect('nregister')
            return redirect('nregister')
        return redirect('nregister')

def VerificationView(request,uidb64, token):
    try:
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = id)
        if not token_generator.check_token(user, token):
            return redirect('nlogin'+'?message='+'Пользователь уже активирован')
        if user.is_active:
            return redirect('nlogin')
        user.is_active = True
        user.save()
        messages.success(request, 'Учетная запись успешно активирована! Вы можете войти в систему прямо сейчас!')
        return redirect('nlogin')

    except Exception as ex:
        messages.error(request, 'Мы столкнулись с ошибкой при переходе по ссылке! Пожалуйста, зарегистрируйтесь еще раз!')
    return redirect('nlogin')

def LoginView(request):
    if request.method=="GET":
        return render(request, 'authentication/login.html')
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        if email and password:
            try:
                get_user = User.objects.get(email=email)
            except Exception as a:
                messages.error(request, 'Неверные учетные данные, пожалуйста, введите правильные учетные данные')
                return redirect('nlogin')
            if get_user.is_staff == True :
                user = auth.authenticate(username=get_user.username, password=password)
                if user:
                    auth.login(request, user)
                    messages.success(request, 'Добро пожаловать '+ user.username+'! Теперь вы вошли в систему!')
                    return redirect('nDashboard')
                else:
                    messages.error(request, 'Неверные учетные данные, пожалуйста, введите правильные учетные данные')
                    return redirect('nlogin')
            else:
                user = auth.authenticate(username=get_user.username, password=password)
                if user:
                    auth.login(request, user)
                    messages.success(request, 'Добро пожаловать ' + user.username+'! Теперь вы вошли в систему!')
                    return redirect('ndashboard')
                else:
                    messages.error(request, 'Неверные учетные данные, пожалуйста, введите правильные учетные данные')
                    return redirect('nlogin')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля!')
            return render(request, 'authentication/login.html')

def LogoutView(request):
    auth.logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect('nlogin')

def RequestPasswordResetEmail(request):
    if request.method == "GET":
        return render(request, 'authentication/resetpassword.html')
    if request.method == "POST":
        email = request.POST['email']
        context={'values':request.POST}
        if not validate_email(email):
            messages.error(request, 'Пожалуйста, введите действительный идентификатор электронной почты.')
            return render(request, 'authentication/resetpassword.html', context)
        if not User.objects.filter(email=email).exists() or not validate_email(email):
            messages.error(request, 'This email is not registered with us. Please register yourself first.')
            return render(request, 'authentication/resetpassword.html', context)
        current_site = get_current_site(request)
        user = User.objects.filter(email=email)
        if user.exists():
            email_contents = {
                    'user': user[0],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user[0])),
                    'token': PasswordResetTokenGenerator().make_token(user[0]),
                }
            link = reverse('set-new-password', kwargs={'uidb64': email_contents['uid'], 'token': email_contents['token']})
            email_subject = 'Reset your password'
            reset_url = 'https://'+current_site.domain+link
            email = EmailMessage(
                    email_subject,
                    'Пожалуйста, перейдите по ссылке ниже, чтобы установить новый пароль для вашей учетной записи \n'+ reset_url,
                    'noreply@semycolon.com',
                    [email],
                )
            EmailThread(email).start()
            messages.success(request, 'Мы отправили вам электронное письмо со ссылкой для сброса вашего пароля')
        return render(request, 'authentication/resetpassword.html')

def SetNewPasswordView(request,uidb64, token):
    if request.method=="GET":
        context = {'uidb64':uidb64,'token':token}
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(username=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Ссылка с паролем недействительна или использовалась ранее, пожалуйста, запросите новый.')
                return render(request, 'authentication/resetpassword.html')
        except Exception as a:
            pass
        return render( request, 'authentication/setnewpass.html', context)
    if request.method=="POST":
        context = {'uidb64':uidb64,'token':token}
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают. Повторно введите оба пароля.')
            return render( request, 'authentication/setnewpass.html', context)
        if len(password1)<6:
            messages.error(request, 'Введите пароль длиной более 6 символов.')
            return render( request, 'authentication/setnewpass.html', context)
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(username=id)
            user.set_password(password1)
            user.save()
            messages.success(request, 'Сброс пароля прошел успешно. Вы можете войти в систему с новым паролем.')
            return redirect('nlogin')
        except Exception as ex:
            messages.info(request, 'Что-то пошло не так, попробуйте еще раз.')
            return render( request, 'authentication/setnewpass.html', context)