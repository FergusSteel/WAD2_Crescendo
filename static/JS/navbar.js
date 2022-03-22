
    $(document).ready(function() {
        $(window).resize(function() { 
            var width = $(document).width();    
            console.log(width);
            if (width < 1000) {  
                console.log("Removing")
                $("#search-bar").removeClass( "center" ); 
                change = true;
            }  
            if (width > 1000) {   
                console.log("Adding")
                $("#search-bar").addClass( "center" ); 
            }
        });
    });

