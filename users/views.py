from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from users.forms import SignUpForm
from users.token import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            token = account_activation_token.make_token(user)

            pk = user.pk
            pk_bytes = force_bytes(pk)
            user_id = urlsafe_base64_encode(pk_bytes)

            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'user_id': user_id,
                'token': token
            })
            user.email_user(subject, message)
            return render(request, 'users/account_activation_sent.html')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def activate(request, user_id, token):
    try:
        decoded_uid = urlsafe_base64_decode(user_id)
        user_id = force_text(decoded_uid)
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, ObjectDoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')

    return render(request, 'users/account_activation_invalid.html')
