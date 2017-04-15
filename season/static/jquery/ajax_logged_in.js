check_ajax_logged_in = function(data)
{
	//check data received by ajax is still valid for
	//section that requires user logged in;
	//handle session time out
	//returns true|false to indicate if user logged in 
	
	/* JSON object is returned when user not authenticated */
	if (typeof data == 'object' && data.not_authenticated == true)
	{
		$('div#lb-mask').show();
		$.get(Urls.ajax_timeout(),function(html){
			//display timeout lb
	       	$('div#lb-to').replaceWith(html);
    		$('div#lb-to').parent('div').show();
		});
		return false;
	}
	return true;
};