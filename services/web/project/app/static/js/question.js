$(document).ready(function () {

	$('.upVote').on('click', function (event) {
		question_id = $(this).attr('q-id');
		answer_id = $(this).attr('ans-id');
		url = '/vote/' + question_id + '/' + answer_id + '/1';
		request = $.ajax({
			url: url,
			type: 'GET',
		});

		request.done(function (data) {
			location.reload();
		});
	});

	$('.downVote').on('click', function (event) {
		question_id = $(this).attr('q-id');
		answer_id = $(this).attr('ans-id');
		url = '/vote/' + question_id 
            + '/' + answer_id + '/0';
		request = $.ajax({
			url: url,
			type: 'GET',
		});

		request.done(function (data) {
			location.reload();
		});
    });

	$('.questionUpVote').on('click', function(event) {
		question_id = $(this).data("id");

		url = '/questionVote/' + question_id + '/1';
		request = $.ajax({
			url: url,
			type: 'GET',
		});
		request.done(function (data){
			location.reload();
		})
	});

	$('.questionDownVote').on('click', function(event) {
		question_id = $(this).data("id");

		url = '/questionVote/' + question_id + '/0';
		request = $.ajax({
			url: url,
			type: 'GET',
		});
		request.done(function (data){
			location.reload();
		})
	});

   	// Attatch event listener to best answer selection buttons.
	$('.best-answer-selection-btn').on('click', function(event) {
		question_id = $(this).attr('q-id');
		answer_id = $(this).attr('ans-id');
		url = "/questions/accept_answer/" + answer_id + "/" + question_id;
		window.location.replace(url);
	});
});