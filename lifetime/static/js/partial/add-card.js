$(function(){
	$(document).on('click', '.add-card', handleAddCard);
	$(".add-card-submit").click(handleAddCardSubmit)
});

function handleAddCard(e){
	$('#add-card-modal').modal();
}

function handleAddCardSubmit(e) {
	$('#add-card-error').addClass('hidden');
    // disable the submit button to prevent repeated clicks
    $('.add-card-submit').attr("disabled", "disabled").button('loading');
    $('#add-card-modal').modal('loading');
  

    Stripe.createToken({
        number: $('.card-number').val(),
        cvc: $('.card-cvc').val(),
        exp_month: $('.card-expiry-month').val(),
        exp_year: $('.card-expiry-year').val()
    }, stripeResponseHandler);

    // prevent the form from submitting with the default action
    return false;
}

function stripeResponseHandler(status, res){
	if (res.error){
		$('#add-card-modal').modal('loading');
		$('#add-card-error .message').text(res.error.message);
		$('#add-card-error').removeClass('hidden');
		$('.add-card-submit').removeAttr("disabled").button('reset');
		return;
	}

	$.get('/cart/add-card/', {token:res.id}, function(a){
		$('#add-card-modal').modal('loading');
		$('.add-card-submit').removeAttr("disabled").button('reset');
		$('#add-card-modal').modal('hide');
		$(document).trigger('add-card-success');
	});
}