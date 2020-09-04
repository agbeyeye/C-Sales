$(document).ready(function(){
	var previous_sect, current_sect,next_sect;
	var opacity;

//next button click
$(".next").click(function(){
	var form = $("#carForm");
		form.validate({
			rules: {
				engine: {required: true,},
				year:{required: true,},
				make:{required:true,},
				model:{required:true,},
				transmission:{required:true,},
				drive_train:{required:true,},
				country:{required: true,},
				state:{required:true,},
				city:{required:true,},
				code:{required:true,},
				vin:{required:true,},
				mileage:{required:true,},
				seller:{required:true,},
				title:{required:true,},
				fuel_type:{required:true,},
				other_fuel_type:{required:true,},
				trim:{required:true,},
				exterior_color:{required:true,},
				interior_color:{required:true,},
				asking_price:{required:true,},
				wheel_alignment:{required:true,},
				repair_status:{required:true,},
				repair:{required:true,},
				name:{required:true,},
				financing:{required:true,},
				contact:{required:true,},
				about_rebuilt:{required:true,},
				terms_service:{required:true,},
				pro_image:{required:true,},
			},
			messages: {
				engine: {required: "engine required",},
				year:{required: "Vehicle year is required",},
				make:{required:"Vehicle make is required",},
				model:{required:"Vehicle model is required",},
				transmission:{required:"transmission is required",},
				drive_train:{required:"drive train is required",},
				country:{required: "country is required"},
				state:{required:"Field is required",},
				city:{required:"Field is required",},
				code:{required:"Field is required",},
				seller:{required:"seller is required",},
				vin:{required:"Field is required",},
				mileage:{required:"Field is required",},
				title:{required:"Field is required",},
				fuel_type:{required:"Field is required",},
				other_fuel_type:{required:"Field is required",},
				trim:{required:"Field is required",},
				exterior_color:{required:"Field is required",},
				interior_color:{required:"Field is required",},
				asking_price:{required:"Field is required",},
				wheel_alignment:{required:"Field is required",},
				repair:{required:"Field is required",},
				repair_status:{required:"Field is required",},
				name:{required:"Field is required",},
				financing:{required:"Field is required",},
				contact:{required:"Field is required",},
				about_rebuilt:{required:"Field is required",},
				terms_service:{required:"Field is required",},
				pro_image:{required:"Vehicle photos are required",},
			}
		});
//      validate form
		if(form.valid()==true){
			current_sect = $(this).parent();
			next_sect = $(this).parent().next();
			//Add Class Active
			$("#progressbar li").eq($("section").index(next_sect)).addClass("active");
			$("#progressbar li").eq($("section").index(next_sect)).css({'color':'white'});
			// remove active class
			$("#progressbar li").eq($("section").index(current_sect)).removeClass("active");
			$("#progressbar li").eq($("section").index(current_sect)).css({'color':'#b70b1f'});
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


//next button click
$("#submit").click(function(){
	var form = $("#carForm");
		form.validate({
			rules: {
				
				seller:{required:true,},
				name:{required:true,},
				financing:{required:true,},
				contact:{required:true,},
				about_rebuilt:{required:true,},
				terms_service:{required:true,},
				
			},
			messages: {
				
				seller:{required:"seller is required",},
				
				name:{required:"Field is required",},
				financing:{required:"Field is required",},
				contact:{required:"Field is required",},
				about_rebuilt:{required:"Field is required",},
				terms_service:{required:"Field is required",},
			
			}
		});
//      validate form
		if(form.valid()==true){
			
		}

});
//previous button click
$(".previous").click(function(){

current_sect = $(this).parent();
previous_sect = $(this).parent().prev();
//Remove class active
$("#progressbar li").eq($("section").index(current_sect)).removeClass("active");
$("#progressbar li").eq($("section").index(current_sect)).css({'color':'#b70b1f'});
// set active class
$("#progressbar li").eq($("section").index(previous_sect)).addClass("active");
$("#progressbar li").eq($("section").index(previous_sect)).css({'color':'white'});
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



$('#fuel_type').change(function(){
	var selectedIndex = $('#fuel_type')[0].selectedIndex;
	// var selectedIndex = selection[0].selectedIndex;
	if(selectedIndex==5){
		$('#other-fuel-container').removeClass("hide-element");
		
	}else{
		$('#other-fuel-container').addClass("hide-element");
	}
});

$('#repair_status').change(function(){
	var selectedIndex = $('#repair_status')[0].selectedIndex;
	// var selectedIndex = selection[0].selectedIndex;
	if(selectedIndex==1){
		$('#repair-container').removeClass("hide-element");
		
	}else{
		$('#repair-container').addClass("hide-element");
	}
});

$('#seller').change(function(){
	var selectedIndex = $('#seller')[0].selectedIndex;
	// var selectedIndex = selection[0].selectedIndex;
	if(selectedIndex==1){
		$('#financing-container').removeClass("hide-element");
		
	}else{
		$('#financing-container').addClass("hide-element");
	}
});

});