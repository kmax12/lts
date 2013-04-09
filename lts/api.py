from django.contrib.auth.models import User
from tastypie import fields
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from lifetime.models import Supply, Category, Product, ProductImage, Order
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization, ReadOnlyAuthorization
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from account.views import handleOrder
from django.utils import formats

class SupplyAuthorization(ReadOnlyAuthorization):
    def is_authorized(self, request, object=None):
       return false

    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        return []

class SupplyAuthentication( ApiKeyAuthentication ):
    '''
    Authenticates everyone if the request is GET otherwise performs
    ApiKeyAuthentication.
    '''

    def is_authenticated(self, request, **kwargs):
        if request.GET.get("all", "true") == 'true':
            return True
        return super( SupplyAuthentication, self ).is_authenticated( request, **kwargs )


class ProductResource(ModelResource):
    product_images = fields.ToManyField('lts.api.ProductImageResource',
            lambda bundle: ProductImage.objects.filter(
                product=bundle.obj
            ), full=True, null=True)

    class Meta:
        queryset = Product.objects.select_related().all()
        resource_name = 'product'

class SupplyResource(ModelResource):
    Product = fields.ManyToManyField(
            ProductResource,
            lambda bundle: Product.objects.filter(
                categories__in=bundle.obj.categories.all()
            ),
            full=True
    )


    def get_object_list(self, request):
        if request.GET.get("all", "true") == "true":
            return Supply.objects.all()
        elif request.user:
            return request.user.profile.get_supplies()

    def dehydrate(self, bundle):
        bundle.data["all"] = bundle.request.GET.get("all", "true")
        return bundle

    class Meta:
        queryset = Supply.objects.select_related().all()
        authorization = ReadOnlyAuthorization()
        authentication = SupplyAuthentication()
        resource_name = 'supply'


class ProductImageResource(ModelResource):
    product = fields.ForeignKey(ProductResource, 'product')

    class Meta:
        queryset = ProductImage.objects.all()
        resource_name = 'product_image'


class OrderResource(ModelResource):
    product = fields.ForeignKey(ProductResource, 'product', full=True)

    def get_object_list(self, request):
        return request.user.profile.get_orders()

    def obj_create(self, bundle, request=None, **kwargs):
        user = request.user
        product_id = bundle.request.POST.get("product_id")
        success = handleOrder(user, product_id)
        bundle.data["success"] = success
        print success
        return bundle

    def dehydrate(self, bundle):
        date = bundle.data["date_placed"]
        formatted_datetime = formats.date_format(date, "SHORT_DATETIME_FORMAT")
        print formatted_datetime
        bundle.data["date_placed"] = formatted_datetime
        return bundle


    class Meta:
        queryset = Order.objects.all()
        resource_name = 'order'
        authentication = ApiKeyAuthentication()



class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name', 'email']
        allowed_methods = ['post', 'get']
        resource_name = 'user'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

    def get_object_list(self, request):
        return super(UserResource, self).get_object_list(request).filter(username=request.user)


    def dehydrate(self, bundle):
        api_key = ApiKey.objects.get_or_create(user=bundle.request.user)
        key = api_key[0].generate_key()
        api_key[0].key = key
        api_key[0].save()
        return {"api_key":key}

# class EntryResource(ModelResource):
#     user = fields.ForeignKey(UserResource, 'user')

#     class Meta:
#         queryset = Entry.objects.all()
#         resource_name = 'entry'

