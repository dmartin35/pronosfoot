bindtableline = function(tableid,action){
	$('table#'+tableid+' tr.tableline').hover(function() {
        var position_color = $(this).children('td.pos:first').css('background-color');
        $(this).css('background-color', position_color);
        $(this).css('cursor', 'pointer');
        $(this).children('td:not(td.pos)').each(function(){$(this).css('border-bottom', '1px solid '+position_color)});;        
    },
    function() {
        $(this).css('background-color', '#FFFFFF');
        $(this).css('cursor', 'default');
        $(this).children('td:not(td.pos)').each(function(){$(this).css('border-bottom', '1px solid #D4CCC6')});;
    }).bind('click',action); 
};
