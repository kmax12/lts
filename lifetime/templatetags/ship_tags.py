from django.template import Library

register = Library()

@register.filter
def can_ship(user, product): 
	if user.is_authenticated():
		return user.profile.has_product_id(product.id)

	return None
    