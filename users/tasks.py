# users/tasks.py (or in views.py)
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def send_verification_email(user_id):
    from .models import User
    user = User.objects.get(id=user_id)  # Fixed typo: id-user_id → id=user_id
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    subject = "Verify your email"
    message = render_to_string('verification_email.html', {
        'user': user,
        'token': token,
        'uid': uid,
    })
    send_mail(subject, message, 'noreply@jobportal.com', [user.email])  # Fixed typo: noneply → noreply