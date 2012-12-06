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

