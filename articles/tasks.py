from time import sleep

from celery import shared_task
from django.template.loader import render_to_string
from sendgrid import Mail, SendGridAPIClient

from hillel_post.settings import EMAIL_SENDER, SENDGRID_KEY


@shared_task
def send_email(data):
    print('>> Sending email')
    context = {
        'title': data['article']['title'],
        'name': data['name'],
        'email': data['email'],
        'text': data['text']
    }
    content = render_to_string('emails/added_comment.html', context)
    message = Mail(
        from_email=EMAIL_SENDER,
        to_emails=data['article']['author_email'],
        subject='Added new comment',
        html_content=content
    )
    sleep(30)
    sg = SendGridAPIClient(SENDGRID_KEY)
    sg.send(message)
