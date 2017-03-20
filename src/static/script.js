"use strict";
$(window).on('load', function(){

	$('body').addClass('loading');

});

$(document).ready(function() {

	$('body').removeClass('loading').addClass('ready');

	// Get <footer> height
	var footerHeight = $('footer').outerHeight(true);

	// Fix Body position issue caused by Fixed Footer
	$('body').css({paddingBottom : footerHeight + 16});

	// Messages
	$('.message').delay(3000).fadeOut(300);

});
