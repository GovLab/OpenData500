$(document).ready(function() {

$.stellar();

$('.m-list-company-summary').click(function() {
	$(this).parent().toggleClass('s-active');
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
