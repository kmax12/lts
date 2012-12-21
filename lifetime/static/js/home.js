$(function(){

	$('#marketing').carousel({interval: 6000}).carousel('cycle');
	$("#logo-home").fitText(1.2, { minFontSize: '50px', maxFontSize: '80px' });
	// $('.add-to-cart').click(handleBuy);
});




function handleBuy(e){
	//todo update number of items in cart

	var $modal = $('#ajax-modal');
	 $('body').modalmanager('loading');


	$modal.load('/cart/add #page-content', 'id='+$(e.target).data('id'), function(){
      $modal.modal();
    });

	return false;
}


