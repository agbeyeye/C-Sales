$(document).ready(function(){
	var previous_sect, current_sect,next_sect;
	var opacity;

$(".next").click(function(){
	var form = $("#carForm");
		form.validate({
			rules: {
				engine: {required: true,},
				vehicle_year:{required: true,},
				vehicle_make:{required:true,},
				transmission:{required:true,},
				drive_train:{required:true,},
				country:{required: true,},
				city:{required:true,},
				seller:{required:true,},
				pro_image:{required:true,},
			},
			messages: {
				engine: {required: "engine required",},
				vehicle_year:{required: "Vehicle year is required",},
				vehicle_make:{required:"Vehicle make is required",},
				transmission:{required:"transmission is required",},
				drive_train:{required:"drive train is required",},
				country:{required: "country is required"},
				city:{required:"city is required",},
				seller:{required:"seller is required",},
				pro_image:{required:"Upload car images",},
			}
		});

		if(form.valid()==true){
			current_sect = $(this).parent();
			next_sect = $(this).parent().next();
			//Add Class Active
			$("#progressbar li").eq($("section").index(next_sect)).addClass("active");
			$("#progressbar li").eq($("section").index(current_sect)).removeClass("active");
			//show the next fieldset
			next_sect.show();
			//hide the current fieldset with style
			current_sect.animate({opacity: 0}, {
			step: function(now) {
			// for making fielset appear animation
			opacity = 1 - now;

			current_sect.css({
			'display': 'none',
			'position': 'relative'
			});
			next_sect.css({'opacity': opacity});
			},
			duration: 600
			});
		}
	
});

$(".previous").click(function(){

current_sect = $(this).parent();
previous_sect = $(this).parent().prev();
//Remove class active
$("#progressbar li").eq($("section").index(current_sect)).removeClass("active");
$("#progressbar li").eq($("section").index(previous_sect)).addClass("active");
//show the previous fieldset
previous_sect.show();

//hide the current fieldset with style
current_sect.animate({opacity: 0}, {
step: function(now) {
// for making fielset appear animation
opacity = 1 - now;

current_sect.css({
'display': 'none',
'position': 'relative'
});
previous_sect.css({'opacity': opacity});
},
duration: 600
});
});


});