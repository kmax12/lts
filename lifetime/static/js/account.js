$(function(){
	$('.open-add-address').click(openAddAddress);
	$('.add-address').click(addAddress);
	$('.btn-order').click(handleOrder);
})


function openAddAddress(){
	var $modal = $('#add-address-modal');
	$modal.modal();
}

function addAddress(){
	console.log($('#address-form').serialize())
	$.post('/account/address/add', $('#address-form').serialize(), function(a){
		if (a.success){
			window.location = "/account/";
		} else {
			alert('error with address');
		}
	})
}

function handleOrder(e){
	if (noAddress){
		openAddAddress();
		return;
	}

	var $modal = $('#order-modal');
	var $target = $(e.target);

	$modal.find('#order-item').text($target.data('name'));
	$modal.find('#item-id').val($target.data('id'));
	console.log($('#order-form').serialize())

	$modal.modal();
}

