from cart import Cart
from django.contrib.auth.models import User, AnonymousUser


def cart(request):
    # if isinstance(request.user, AnonymousUser):
    #     username = "anonuser"
    #     try:
    #         request.user = User.objects.create_user(username)
    #     except IntegrityError:
    #         request.user = User.objects.get(username=username)


    return {
        'cart': Cart(request)
    }