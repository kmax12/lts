from cart import Cart
from django.contrib.auth.models import User, AnonymousUser
from lts.settings import ORDER_TEXT


def cart(request):
    # if isinstance(request.user, AnonymousUser):
    #     username = "anonuser"
    #     try:
    #         request.user = User.objects.create_user(username)
    #     except IntegrityError:
    #         request.user = User.objects.get(username=username)


    return {
        'cart': Cart(request),
        'ORDER_TEXT': ORDER_TEXT
    }