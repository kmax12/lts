from django.template import Library

register = Library()

@register.filter
def can_ship(user, product): 
	return user.profile.has_product_id(product.id)
    