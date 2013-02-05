$(function(){
	// $(document).on('click', '.btn-remove', handleRemove);
	// $(document).on('add-card-success', function(){
	// 	window.location = "/cart/";
	// });
})

function handleRemove(e){
	$target = $(e.target);
	$target.button('loading')
	$.getJSON($target.attr('href'), function(res){
		if (res.success){
			$target.closest('tr').remove();	
			$('#total').text(res.total);
			if (parseInt(res.total) == 0){
				window.location = "/cart/";
			}
		}
		
	});
	return false;
}