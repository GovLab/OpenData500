$(document).ready(function() {

// if (!($('html').hasClass('no-js'))) {
// 	$.stellar();
// };


$('.m-list-company-summary').click(function() {
	$(this).parent().toggleClass('s-active');
});

// $('.m-candidates-item').click(function() {
// 	$(this).toggleClass('s-active');
// });

// Smooth Scrolling Function
	$(function() {
		$('a[href*=#]:not([href=#])').click(function() {
			if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') 
				|| location.hostname == this.hostname) {

			var target = $(this.hash);
			target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
			if (target.length) {
				$('html,body').animate({
				  scrollTop: target.offset().top
				}, 1000);
				return false;
				}
			}
		});
	});


});

// //Istopes
// // init Isotope
// var $container = $('.isotopes-container');
// // init
// $container.isotope({
//   // options
//   itemSelector: '.m-candidates-item',
//   layoutMode: 'fitColumns'
// });



// // filter items on button click
// $('#filters').on( 'click', 'button', function( event ) {
//   var filtr = $(this).attr('data-filter');
//   $container.isotope({ filter: filtr });
// });
