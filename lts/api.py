from django.contrib.auth.models import User
from tastypie import fields
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from lifetime.models import Supply, Category, Product, ProductImage
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization, ReadOnlyAuthorization
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash

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


    def apply_authorization_limits(self, request, object_list):
        print "works!"
        if request.user.is_superuser:
            return object_list.filter(user__id=request.GET.get('user__id',''))

    # def apply_authorization_limits(self, request, object_list):
    #     # if request.GET.get("all", "true") != "true":
    #     #     return User.objects.filter(user=request.user).profile.get_supplies()
    #     return []

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

