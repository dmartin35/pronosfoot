$(document).ready(function() {

  $('.mdl-menu .mdl-menu__item').on("click", function(){
        window.location = $(this).data('href');
    });

});
