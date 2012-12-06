$(function(){
	// $('.open-add-address').click(openAddAddress);
	$('.add-address').click(addAddress);
})


function openAddAddress(){
	var $modal = $('#add-address-modal');
	$modal.modal();
}

function addAddress(){
	console.log($('#address-form').serialize())
	$.post('/account/address/add/', $('#address-form').serialize(), function(a){
		if (a.success){
			window.location = "/account/";
		} else {
			alert('error with address');
		}
	})
}
