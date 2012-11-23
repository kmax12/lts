$(function(){
	$(document).on('click', '.btn-remove', handleRemove);
})

function handleRemove(e){
	$target = $(e.target);
	$target.button('loading')
	$.getJSON($target.attr('href'), function(res){
		console.log(res)
		if (res.success){
			$target.closest('tr').remove();	
			$('#total').text(res.total);
		}
		
	});
	return false;
}