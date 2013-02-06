$(function(){
	$(document).on('click', '.add-card', handleAddCard);
});

function handleAddCard(e){
	StripeCheckout.open({
		key:         'pk_test_K9TEaiWEhLWxOhkmsRC1WgCD',
		name:        'Lifetime Supply',
		panelLabel:  'Add card',
		token:       stripeResponseHandler
	});

    // prevent the form from submitting with the default action
    return false;
}

function stripeResponseHandler(token){
	$('#stripe-token').val(token.id)
}