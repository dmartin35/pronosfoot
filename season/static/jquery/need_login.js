bind_to_need_login = function(elem){
	//bind an html element click to the need login page
    $(elem).bind('click',function(event){
		event.preventDefault();
		$('div#lb-mask').show();
		$.get(Urls.ajax_need_login(),function(html){
       		$('div#lb-info').replaceWith(html);
			$('div#lb-info').parent('div').show();
		});
    });
};