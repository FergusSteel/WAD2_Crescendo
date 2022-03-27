
    $(document).ready(function() { 
        var width = $(document).width();   
        if (width < 1250) { 
            $("#search-bar").removeClass( "center" ); 
        }
        $(window).resize(function() { 
            var width = $(document).width();    
            console.log(width);
            if (width < 1000) {  
                console.log("Removing")
                $("#search-bar").removeClass( "center" ); 
                change = true;
            }  
            if (width > 1250) {   
                console.log("Adding")
                $("#search-bar").addClass( "center" ); 
            }
        });
    });

