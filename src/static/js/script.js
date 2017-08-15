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

	// Hide Messages
	$('.message-close').on( 'click', function() {
		$(this).parent().fadeOut(300); // message box
		$(this).parent().parent().fadeOut(300); // message container (background)
	});

	// Toggle Graph Visibility
	$('.graph').each(function(){
		$(this).wrap('<div class="graph-container"></div>');
	});
	$('.graph-container').on( 'click', function() {
		$(this).toggleClass('show');
		$(this).find('embed').fadeToggle(300);
	});

	// Show Menu Dropdown
	$('.user-menu').on( 'click', function() {
		// Use Class to pass visual functionality to CSS
		$(this).toggleClass('clicked');
	});

	// Fix visual issue caused by Fixed Footer
	// @footerHeight : footer total height
	var footerHeight = $('footer').outerHeight(true);
	$('main').css({paddingBottom : footerHeight + 16});
	$('.message-container').css({bottom : footerHeight});

	// Scroll To Top Button
	$(window).scroll(function() {
		if ($(window).scrollTop() >= $(window).height() / 4) {
			$('body').addClass('scroll');
			$('.scroll-top').on( 'click', function() {
				$('html, body').stop().animate({ scrollTop: 0 }, 300);
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
