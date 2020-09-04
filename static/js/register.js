//$(document).ready(function(){
//
//	$("#register").click(function(){
//		var form = $("#registration-form");
//		form.validate({
//			rules: {
//				email: {required: true,},
//				username:{required:true, minlength:6,},
//				password:{required: true,minlength:8,},
//				confirmPassword:{required:true,equalTo:'#password',},
//				policy:{required:true,},
//
//			},
//			messages: {
//				email: {required: "email is required",},
//				username:{required:"this field is required",},
//				password:{required: "password is required",},
//				confirmPassword:{required:"this field is required",equalTo:"password does not match",},
//				policy:{required:"You must accept in order to register",},
//			}
//		});
//
//		if(form.valid()==true){
////			form.submit();
//			console.log('form submittd');
//		}
//	});
//});