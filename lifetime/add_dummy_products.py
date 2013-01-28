from models import Category, Product


cats = Category.objects.all()

for c in cats:
	for n in range(3):
		p = Product(name=c.name + " " + str(n))
		p.save()
		p.categories.add(c)

