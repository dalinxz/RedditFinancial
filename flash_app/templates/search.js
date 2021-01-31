// <![CDATA[	
    $(document).ready(function(){	

        // delete event
        $('#attach').livequery("click", function(){
        
            if(!isValidURL($('#url').val()))
            {
                alert('Please enter a valid url.');
                return false;
            }
            else
            {
                $('#load').show();
                $.post("fetch.php?url="+$('#url').val(), {
                }, function(response){
                    $('#loader').html($(response).fadeIn('slow'));
                    $('.images img').hide();
                    $('#load').hide();
                    $('img#1').fadeIn();
                    $('#cur_image').val(1);
                });
            }
        });	
        // next image
        $('#next').livequery("click", function(){
        
            var firstimage = $('#cur_image').val();
            $('#cur_image').val(1);
            $('img#'+firstimage).hide();
            if(firstimage <= $('#total_images').val())
            {
                firstimage = parseInt(firstimage)+parseInt(1);
                $('#cur_image').val(firstimage);
                $('img#'+firstimage).show();
            }
        });	
        // prev image
        $('#prev').livequery("click", function(){
        
            var firstimage = $('#cur_image').val();
            
            $('img#'+firstimage).hide();
            if(firstimage]]>0)
            {
                firstimage = parseInt(firstimage)-parseInt(1);
                $('#cur_image').val(firstimage);
                $('img#'+firstimage).show();
            }
            
        });	
        // watermark input fields
        jQuery(function($){
           
           $("#url").Watermark("http://");
        });
        jQuery(function($){
        
            $("#url").Watermark("watermark","#369");
            
        });	
        function UseData(){
           $.Watermark.HideAll();
           $.Watermark.ShowAll();
        }
        });	
        function isValidURL(url){
        var RegExp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&amp;%@!\-\/]))?/;
        
        if(RegExp.test(url)){
            return true;
        }else{
            return false;
        }
        }
        // ]]&gt;