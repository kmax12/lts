$(function(){
	$('#marketing').carousel({interval: 4000}).carousel('cycle');

	footer();
	// $('.add-to-cart').click(handleBuy);
});

function footer() {
    if ($(window).height() > $('body').height()){
        var extra = $(window).height() - $('body').height();
        $('footer-container').css('margin-top', extra);
    }
}

function handleBuy(e){
	//todo update number of items in cart

	var $modal = $('#ajax-modal');
	 $('body').modalmanager('loading');


	$modal.load('/cart/add #page-content', 'id='+$(e.target).data('id'), function(){
      $modal.modal();
    });

	return false;
}

