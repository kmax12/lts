from django.core.mail import send_mail
from lifetime.models import *
from utils.email_templates import gift
from templated_email import send_templated_mail

def send_reciept(total, supplies, to_email, name):
    send_templated_mail(
            template_name='reciept',
            from_email='Lifetime Supply <friends@lifetimesupply.com>',
            recipient_list=[to_email, "sales@lifetimesupply.com"],
            context={
                'total' : total,
                'supplies' : supplies,
                'name' : name
            }
            # Optional:
            # cc=['cc@example.com'],
            # bcc=['bcc@example.com'],
            # headers={'My-Custom-Header':'Custom Value'},
            # template_prefix="my_emails/",
            # template_suffix="email",
    )


def email_student_supplies(supplies, from_name, to_email):
    g = Gift(from_name = from_name, to_email = to_email)
    g.save()
    g.supplies.add(*supplies)
    g.save()

    send_templated_mail(
            template_name='gift',
            from_email='Lifetime Supply <friends@lifetimesupply.com>',
            recipient_list=[to_email],
            context={
                'code' : g.code,
                'supplies' : supplies,
                'from_name' : from_name
            }
            # Optional:
            # cc=['cc@example.com'],
            # bcc=['bcc@example.com'],
            # headers={'My-Custom-Header':'Custom Value'},
            # template_prefix="my_emails/",
            # template_suffix="email",
    )

def create_user_with_subscriptions(name, email, password, supplies):
    u = User(first_name=name, email=email, username=email)
    u.set_password(password)
    u.save()
    subs = []
    for sup in supplies:
        subs.append(Subscription(owner=u, supply=sup))

    Subscription.objects.bulk_create(subs)