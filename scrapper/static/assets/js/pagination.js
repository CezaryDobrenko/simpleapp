$( document ).ready(function() {
    $( "#page_form" ).submit(function( event ) {
      var value = $('#page').val();
      var url = document.location.protocol +"//"+ document.location.hostname + document.location.pathname;
      if(value>0 && value<={{ paginator.page_range|last }}){
        if(document.location.href.indexOf("?filter") >= 0) {
          url += "?page="+value;
        }else{
          url += "?page="+value;
        }
          document.location = url;
      }
      else{
        alert("Numer strony musi znajdować się w zakresie: <1,"+{{ paginator.page_range|last }}+">");
      }
      event.preventDefault();
    });
  });