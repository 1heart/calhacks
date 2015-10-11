var sendLike = function(element) {
	// $('.likable').each(function(a) {console.log($(this).data('transaction-id'))})
	var currId = $(element).data('transaction-id');
	var data = {
		'transactionId': currId
	};
	$.post('/vote', data, function(response) {
			if (response === 'lol nice') {
				currLikes = findLikeElement(currId);
				currNumLikes = parseInt($(currLikes).html());
				$(currLikes).html(currNumLikes + 1);
				console.log( currLikes);
			}
		}).error(function(e) {

		});
}

var findLikeElement = function(transactionId) {
	var likes = $('.likes');
	for (var i=0; i<likes.length; i++){
		if ($(likes[i]).data('transaction-id') === transactionId) {
			return likes[i];
		}
	}
}


// $('.likable').each(function(a) {
// 	$(this).onClick(function() {
// 		console.log('LOL')
// 	});
// 	// console.log($(this).data('transaction-id'));
// })
