function wcag_handler(){
    if(!localStorage.getItem("wcag")){
        localStorage.setItem("wcag", "default"); 
        localStorage.setItem("wcag_size", 1);  
    } else {
        if(localStorage.getItem("wcag") == "yellow"){
            wcag_yellow();
        }
        if(localStorage.getItem("wcag") == "black"){
            wcag_black();
        }
        change_size(parseInt(localStorage.getItem("wcag_size")))
    }
}

function change_size(size){
    $('html *:not(script, style, noscript, input)').each(function() {
        test = parseInt($(this).css('font-size'))+size
        $(this).css("font-size", test)
    });
}

function reset_size(){
    localStorage.setItem("wcag_size", 1); 
    window.location.reload(true);
}

function change_size_minus(){
    localStorage.setItem("wcag_size", parseInt(localStorage.getItem("wcag_size"))-1); 
    $('html *:not(script, style, noscript, input)').each(function() {
        size = parseInt($(this).css('font-size'))-1
        $(this).css("font-size", size)
    });
}

function change_size_plus(){
    localStorage.setItem("wcag_size", parseInt(localStorage.getItem("wcag_size"))+1); 
    $('html *:not(script, style, noscript, input)').each(function() {
        size = parseInt($(this).css('font-size'))+1
        $(this).css("font-size", size)
    });
}


function wcag_default(){
    localStorage.setItem("wcag", "default"); 
    window.location.reload(true);
}

function wcag_black(){
    localStorage.setItem("wcag", "black");
    $('html *:not(script, style, noscript, input)').each(function() {
        $(this).css("background", "none");
        $(this).css("background-color", "black");
        $(this).css("color", "white");
        $(this).css("box-shadow", "none");
        $(this).css("text-shadow", "none");
    });
    $('.nav-item').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });
    $('.navbar').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });
    $('.nav-link').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });
    $('.nav').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });
    $('.black_container2').each(function() {
        $(this).css("background-color", "black");
        $(this).css("color", "white");
    });
    $('.sidebar').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });
    $('.navbar-brand').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });
    $('.navbar-brand-wrapper').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });
    $('.menu-title').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });  
    $('.sidebar-user-menu').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });  
    $('.nav .mdi').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });  
    $('.nav .icon-bg').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });  
    $('.nav .menu-arrow').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });  
    $('.nav .user-details').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });  
    $('.nav .email').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    }); 
    $('.nav .mb-1').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });  
    $('.image_wcag').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    }); 
    $('.navbar-menu-wrapper').each(function() {
        $(this).css("background-color", "white");
    });  
    $('.navbar-toggler').each(function() {
        $(this).css("background-color", "white");
    }); 
    $('.mdi-menu').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });  
    $('.navbar-nav').each(function() {
        $(this).css("background-color", "white");
    }); 
    $('.black_container').each(function() {
        $(this).css("background-color", "white");
    }); 
    $('.turn_black').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });
    $('.yellow_container').each(function() {
        $(this).css("background-color", "white");
    }); 
    $('.turn_yellow').each(function() {
        $(this).css("background-color", "yellow");
        $(this).css("color", "black");
    }); 
    $('.default_container').each(function() {
        $(this).css("background-color", "white");
    }); 
    $('.turn_default').each(function() {
        $(this).css("background-color", "#33c92d");
        $(this).css("color", "black");
    }); 
    $('a').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });
    $('.form-control').each(function() {
        $(this).css("background-color", "white");
        $(this).css("color", "black");
    });  
}

function wcag_yellow(){
    localStorage.setItem("wcag", "yellow");
    $('html *:not(script, style, noscript, input)').each(function() {
        $(this).css("background", "none");
        $(this).css("background-color", "yellow");
        $(this).css("color", "black");
        $(this).css("box-shadow", "none");
        $(this).css("text-shadow", "none");
    });
    $('.nav-item').each(function() {
        $(this).css("background-color", "white");
    });
    $('.nav-link').each(function() {
        $(this).css("background-color", "white");
    });
    $('.nav').each(function() {
        $(this).css("background-color", "white");
    });
    $('input').each(function() {
        $(this).css("background-color", "white");
    });
    $('.nav').each(function() {
        $(this).css("background-color", "white");
    });
    $('.sidebar').each(function() {
        $(this).css("background-color", "white");
    });
    $('.navbar-brand').each(function() {
        $(this).css("background-color", "white");
    });
    $('.navbar-brand-wrapper').each(function() {
        $(this).css("background-color", "white");
    });
    $('.menu-title').each(function() {
        $(this).css("background-color", "white");
    });  
    $('.sidebar-user-menu').each(function() {
        $(this).css("background-color", "white");
    });  
    $('.nav .mdi').each(function() {
        $(this).css("background-color", "white");
    });  
    $('.nav .icon-bg').each(function() {
        $(this).css("background-color", "white");
    });  
    $('.nav .menu-arrow').each(function() {
        $(this).css("background-color", "white");
    });  
    $('.nav .user-details').each(function() {
        $(this).css("background-color", "white");
    });  
    $('.nav .email').each(function() {
        $(this).css("background-color", "white");
    }); 
    $('.turn_black').each(function() {
        $(this).css("background-color", "white");
    }); 
    $('.turn_default').each(function() {
        $(this).css("background-color", "#33c92d");
    }); 
    $('.nav .mb-1').each(function() {
        $(this).css("background-color", "white");
    });  
}

wcag_handler()