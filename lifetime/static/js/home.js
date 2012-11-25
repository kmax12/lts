$(function(){
	// $('.add-to-cart').click(handleBuy);
})

function handleBuy(e){
	//todo update number of items in cart

	var $modal = $('#ajax-modal');
	 $('body').modalmanager('loading');


	$modal.load('/cart/add #page-content', 'id='+$(e.target).data('id'), function(){
      $modal.modal();
    });

	return false;
}

