$(document).ready(function(){

	$("#login-form").click(function(){
		var form = $("#login-form");
		form.validate({
			rules: {
				email: {required: true,},
				password:{required: true,},
				
			},
			messages: {
				email: {required: "email is required",},
				password:{required: "password is required",},				
			}
		});

		if(form.valid()==true){
			form.submit();
		}
	});
});