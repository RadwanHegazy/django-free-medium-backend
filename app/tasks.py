from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER
from celery import shared_task
from globals.scrapper import ArabicFredium

@shared_task
def StartTask (**kwargs) :

    email = kwargs['email']
    link = kwargs['link']
    lang = kwargs['lang']
    
    af = ArabicFredium(
        url = link,
        lang=lang
    )

    template = af.build_page()


    send_mail(
        subject='Your post is now for free',
        html_message=template,
        message="post is done",
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
    )

