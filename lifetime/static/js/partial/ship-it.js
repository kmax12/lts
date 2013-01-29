/*
	How to use
	1. add class btn-ship-it to any button that should trigger shipping modal
	2. button with btn-ship-it class should have two attributes
		1. "data-name" = name of product
		2. "data-id" = id of procduct 
*/

$(function(){
	$('.btn-ship-it').click(handleOrder);
});

function handleOrder(e){
	// if (noAddress){
	// 	openAddAddress();
	// 	return;
	// }

	var $modal = $('#order-modal');
	var $target = $(e.target);

	$modal.find('#order-item').text($target.data('name'));
	$modal.find('#item-id').val($target.data('id'));

	$modal.modal();
}

