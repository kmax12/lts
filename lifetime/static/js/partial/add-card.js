$(function(){
	$(document).on('click', '.add-card', handleAddCard);
});

function handleAddCard(e){
	var token = function(res){
	    console.log('Got token ID:', res.id);
	};

	StripeCheckout.open({
		key:         'pk_test_czwzkTp2tactuLOEOqbMTRzG',
		name:        'Lifetime Supply',
		panelLabel:  'Add card',
		token:       stripeResponseHandler
	});

    // prevent the form from submitting with the default action
    return false;
}

function stripeResponseHandler(token){
	$.get('/account/add-card/', {token:token}, function(a){
		$.trigger('add-card-success');
		console.log(a)
	});
}