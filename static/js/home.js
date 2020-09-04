$(document).ready(function(){
	 $('.favorite').click(function() {
                
                $.ajax({
                  url: 'vehicle-like/',
                  type: 'POST',
                  processData: false, // important
                  contentType: false, // important
                  data: {'data':},
                  success: function(response){
                    if(response.success){
                        console.log(response);
                        window.location.href = "{%url 'my-listing'%}";
                    }
                    else {
                          $('#submission-error').css('display','block');
                    }
                  
                  },
                  error:function(error){
                    // window.location.href = "{%url 'home'%}";
                  }
                });
});