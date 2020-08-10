$(document).ready(function(){
	
	var gridSection = $("#gridShow");
	var listSection = $("#listShow");

	// when grid button is clicked
	$(".gridview").click(function(){
		$(".listview").removeClass("active-view");
		$(".gridview").addClass("active-view");
		gridSection.show();
		listSection.css({'display':'none'});
		
	});

	// when list button is clicked
	$(".listview").click(function(){
		$(".gridview").removeClass("active-view");
		$(".listview").addClass("active-view");
		listSection.show();
		gridSection.css({'display':'none'});
	});
});