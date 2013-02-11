$(function(){
	$(document).on('click', '.add-card', handleAddCard);
});

function handleAddCard(e){
	StripeCheckout.open({
		key:         STRIPE_KEY,
		name:        'Lifetime Supply',
		panelLabel:  'Add card',
		token:       stripeResponseHandler
	});

    // prevent the form from submitting with the default action
    return false;
}

function stripeResponseHandler(token){
	$('#add-card').addClass('hide');

	$('#card-info').removeClass('hide');

	$('#card-type').text(token.card.type)
	$('#card-last4').text(token.card.last4);

	$('#stripe-token').val(token.id)
}