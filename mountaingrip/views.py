from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import translation

from .forms import SignUpForm
from start.models import Profile, Token

import uuid
from func.tokens import account_activation_token


def about(request):
    return render(request, 'about.html')


def index(request):
    if request.user.is_authenticated:
        return redirect('/start/')
    else:
        return render(request, 'start/index.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/start/')
    else:
        return redirect('/')


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                to_email = form.cleaned_data.get('email')
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                user = form.save(commit=False)

                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                token = str(uuid.uuid4())
                Token(user=user.pk, token=token, activated=0).save()
                Profile(user_id=user.pk).save()
                mail_subject = _('Activate your Mountain Grip account.')
                message = render_to_string('registration/account_activate_email.html', {
                    'name': user.get_full_name(),
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                email = EmailMessage(
                    mail_subject, message, from_email='kboberek@gmail.com', to=[to_email]
                )

                if email.send():
                    data = {'activation': 1}
                else:
                    data = {'activation': 0}
                return render(request, 'start/signup.html', {'data': data})
        else:
            form = SignUpForm()
        return render(request, 'start/signup.html', {'form': form})
    else:
        return redirect('/start/')


''' Server errors '''


def error_404(request, exception):
    response = render(request, 'errors/404.html', {})
    response.status_code = 404
    return response


def error_403(request, exception=None):
    response = render(request, 'errors/403.html', {})
    response.status_code = 403
    return response


def error_400(request, exception=None):
    response = render(request, 'errors/403.html', {})
    response.status_code = 400
    return response


def error_500(request, exception=None):
    response = render(request, 'errors/500.html', {})
    response.status_code = 500
    return response
