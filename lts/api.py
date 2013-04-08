from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from lifetime.models import Supply, Category, Product, ProductImage




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

    class Meta:
        queryset = Supply.objects.select_related().all()
        resource_name = 'supply'

class ProductImageResource(ModelResource):
    product = fields.ForeignKey(ProductResource, 'product')

    class Meta:
        queryset = ProductImage.objects.all()
        resource_name = 'product_image'

# class EntryResource(ModelResource):
#     user = fields.ForeignKey(UserResource, 'user')

#     class Meta:
#         queryset = Entry.objects.all()
#         resource_name = 'entry'
