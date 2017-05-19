(function($) {
jQuery.fn.pf_dropdown = function(url,container_id) {
    /*
    * url of the ajax request to be called on item select change
	* container_id is the section that will be replaced with
	* html code in response of request
    */

	var $url = url;
	var $container_id = container_id;

   	return this.each(function() {
		var $this = $(this);
		var $this_id = "#"+$(this).attr("id");

        $(this).on("change", function(){
            var team_id = $( this ).val();

            $.get($url(team_id),function(data){
			    //replace container html content
				$($container_id).replaceWith(data);
			});

        });

    });
};
})(jQuery);
