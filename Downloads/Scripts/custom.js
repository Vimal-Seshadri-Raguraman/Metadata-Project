jQuery(document).ready(function() {

   // Sticky Nav
   jQuery(window).scroll(function(){
      if ($(this).scrollTop() > 36) {
         $('.navbar').addClass('sticky');
      } else {
         $('.navbar').removeClass('sticky');
      }
   });

   jQuery('.w3--plans--mobile').slick({
        arrows: false,
        slidesToShow: 1,
        slidesToScroll: 1,
        infinite: false
   });

});


