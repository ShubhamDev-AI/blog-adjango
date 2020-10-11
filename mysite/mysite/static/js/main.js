// const date = new Date();
// document.querySelector('.year').innerHTML = date.getFullYear();

// //Automatically fade out messages
// setTimeout(function() {
//     $('#message').fadeOut('slow')
// }, 3000);

// 

(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
  });

})(jQuery);
