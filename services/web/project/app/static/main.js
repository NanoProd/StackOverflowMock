alert('THE HOME HAS BEEN LOADED')


$(document).ready(function(){

	$('#upVote').on( 'click', function(event){
	var answer_id = $(this).data('id');
	var url = '/upVote/' + answer_id;
    console.log('up')
	request = $.ajax({
		url: url,
		type: 'POST',
		//data: {answer_id: answer_id}
	});

	request.done(function(data){
		location.reload();
	});
});

$('#downVote').on( 'click', function(event){
	var answer_id = $(this).data('id');
	var url = '/downVote/' + answer_id;
    console.log('down')
	request = $.ajax({
		url: url,
		type: 'POST',
		//data: {answer_id: answer_id}
	});

	request.done(function(data){
		location.reload();
	});
});
});


