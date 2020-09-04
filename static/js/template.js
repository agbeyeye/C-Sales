$(document).ready(function(){

	$("#submit").click(function(){
		var form = $("#login-form");
		form.validate({
			rules: {
				username: {required: true,},
				password:{required: true,},

			},
			messages: {
				username: {required: "username is required",},
				password:{required: "password is required",},
			}
		});

		

		// if(form.valid()==true){
		// 	var username = $.trim($('#username').val());
  //   		var pwd = $.trim($('#password').val());
		// 	$.ajax({
		// 	    type: "GET",
		// 	    url: "login/",
		// 	    data: {username:username,password:pwd},
		// 	    success: function(response){
		// 	        //if request if made successfully then the response represent the data
		// 	        if(response=='login'){console.log('successfuly login');
		// 	        	window.location.href = "{%url 'home'%}";
		// 	    	}else{
		// 	    		console.log('login failed');
			    		
		// 	    	}
		// 	    }
		// 	  });
		// }
	});
});