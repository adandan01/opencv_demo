$(function () {

    //$.ajax({
    //    url: 'http://uifaces.com/api/v1/random',
    //    type: 'GET',
    //    dataType: 'json',
    //    cache: false,
    //    success: function (uifaces) {
    //        var name = uifaces.username;
    //        console.log(uifaces);
    //        $('#random1').prop('src', uifaces.image_urls.epic);
    //        $('#image_url').val(uifaces.image_urls.epic).change();
    //
    //    }
    //});
    lightbox.option({
        'resizeDuration': 200,
        'wrapAround': true,
    });
    $.ajax({
        url: 'https://randomuser.me/api/',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            $('#random1').prop('src', data.results[0].user.picture.large);
            $('#image_url').val(data.results[0].user.picture.large).change();
        }
    });
    $('#image_url').change(function () {
        $('#random1').prop('src', $(this).val());
        $('#random1_url').prop('href', $(this).val());
        $('#random_result').prop('src', '');
        $.post("/face_detection/detect/", {url: $(this).val()}).done(function (data) {
            console.log('data', data);
            $('#random_result').prop('src', data.image_data);
            $('#random_result_url').prop('href', data.image_data);
            $('#result_msg').text(data.num_faces);
        });
    });


});

function setInput(url) {

    $('#image_url').val(url).change();
}
