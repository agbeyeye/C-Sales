$(document).ready(function() {
    // document.getElementById('pro-image').addEventListener('change', readImage, false);

    // $( ".preview-images-zone" ).sortable();

    // $(document).on('click', '.image-cancel', function() {
    //     let no = $(this).data('no');
    //     $(".preview-image.preview-show-"+no).remove();
    // });

    //  $('#upload').click(function() {
    //     console.log('ajax run');
    //     var car_id = $("#car_id").val();
    //     formData.append('car_id',car_id);
    //     $.ajax({
    //       url: 'upload/',
    //       type: 'POST',
    //       processData: false, // important
    //       contentType: false, // important
    //       data: formData
    //     });
    // });
});


var num = 1;
var formData= new FormData();

function readImage() {
    var images={};
    if (window.File && window.FileList && window.FileReader) {
        var files = event.target.files; //FileList object
        for (var i =0; i< files.length; i++) {
            //append image file to data form
            formData.append("file", files[i]);
        }
        
        
        for(var item of imgFiles.entries()){
             console.log(item[0],item[1]);

        }
       
        var output = $(".preview-images-zone");

        for (let i = 0; i < files.length; i++) {
            var file = files[i];
            if (!file.type.match('image')) continue;

            var picReader = new FileReader();

            picReader.addEventListener('load', function (event) {
                var picFile = event.target;
                var html =  '<div class="preview-image preview-show-' + num + '">' +
                            '<div class="image-cancel" data-no="' + num + '">x</div>' +
                            '<div class="image-zone"><img id="pro-img-' + num + '" src="' + picFile.result + '"></div>';

                output.append(html);
                num = num + 1;
            });

            picReader.readAsDataURL(file);
        }
        // $("#pro-image").val('');
    } else {

        console.log('Browser not support');
    }
}

