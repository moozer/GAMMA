"use strict";

// Load
$(window).on('load', function(){

	// Body Classes
	$('body').addClass('loading');

});

// Ready
$(document).ready(function() {

	// Body Classes
	$('body').removeClass('loading').addClass('ready');

	// Fix Body position issue caused by Fixed Footer
	// @footerHeight : footer total height
	var footerHeight = $('footer').outerHeight(true);
	$('body').css({paddingBottom : footerHeight + 32});

	// Hide Messages
	$('.message-close').on( 'click', function() {
		$(this).parent().fadeOut(300); // message box
		$(this).parent().parent().fadeOut(300); // message container (background)
	});

	// Scroll To Top Button
	$(window).scroll(function() {
		if ($(window).scrollTop() >= $(window).height() / 4) {
			$('body').addClass('scroll');
			$('.scroll-top').on( 'click', function() {
				$('html, body').stop().animate({ scrollTop: 0 }, 200);
				// .stop() fixes scrolling issue after click
			});
		} else {
			$('body').removeClass('scroll');
		}
	});

});

// Key Press Events
$(document).keyup(function(e) {
	// Esc Key
	if (e.keyCode === 27) $('.message-close').click();
});
