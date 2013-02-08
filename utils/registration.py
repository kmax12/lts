from django.core.mail import send_mail
from lifetime.models import *
from utils.email_templates import gift


def email_student_supplies(supplies, from_name, to_email):
    g = Gift(from_name = from_name, to_email = to_email)
    g.save()
    g.supplies.add(*supplies)
    g.save()

    subject =  gift["subject"]
    body = gift["body"] % ("localhost:8000/gift?code="+g.code)
    send_mail(subject, body, 'team@lifetimesupply.com', [to_email], fail_silently=False)

def create_user_with_subscriptions(name, email, password, supplies):
    u = User(first_name=name, email=email, username=email)
    u.set_password(password)
    u.save()
    subs = []
    for sup in supplies:
        subs.append(Subscription(owner=u, supply=sup))

    Subscription.objects.bulk_create(subs)