from django.core.mail import send_mail

def send(subject, message, from="info", to):
	messages = ()

	for r in to:
		add = (subject, message, from+'@lifetimesupply.com', [r])
		messages = messages + (add)
		

	send_mass_mail(messages)

