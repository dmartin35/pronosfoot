(function($) {
jQuery.fn.createDropdown = function(ajaxgetrequest,container,ajaxrespvalid) {
	//request is the ajax request to be called on item click
	//container if the section that will be replaced with 
	//html code in response of request
	//ajaxrespvalid if defined must be a function returning true|false 
	var $ajaxgetrequest = ajaxgetrequest;
	var $container = container;

   	return this.each(function() {
		var $this = $(this);
		var $this_id = "#"+$(this).attr("id");

      	$($this_id+" dt a").toggle(function(){
    		//open dropdown
    		$(this).addClass("opened");
    		$($this_id+" dd ul").show();
    	},function(){
			//close dropdown
    		$(this).removeClass("opened");
    		$($this_id+" dd ul").hide();
    	});
                        
        $($this_id+" dd ul li a").click(function() {
            var text = $(this).html();
            var val = $(this).find("span.value").html();
			//change selected value of the dropdown
			$($this_id+" dt a span.selected").html(text);
            //click to apply toggle
        	$($this_id+" dt a").click();
			$.get($ajaxgetrequest(val),function(data){
				valid = true;
				if (typeof ajaxrespvalid != "undefined")
				{
					valid = ajaxrespvalid(data);
				}

				//replace container html content - if data valid
				if (valid) $($container).replaceWith(data);
			}); 
			
        });
          
        $(document).bind('click', function() {

            if ($($this_id+" dd ul").is(':visible'))
            {
            	//click to apply toggle
            	$($this_id+" dt a").click();
            }
        });
        
    });
};
})(jQuery);
