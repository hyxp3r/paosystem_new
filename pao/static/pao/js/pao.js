
window.onload = init;

$('[data-toggle="tooltip"]').tooltip();


function init() {

    var check = document.getElementsByClassName('h5 mb-0 mr-3 font-weight-bold text-gray-800');
    var values = document.getElementsByClassName('progress-bar');

    values[0].style.width = check[0].textContent


    for (var i = 1; i<30; i++){
        
        values[i].style.width = values[i].textContent

    }
    
}

$(function () {

$('.notCheckFilter').on('click', function() {
    
    $('.razd').parent().parent().parent().hide();
    $('.notCheck').parent().parent().parent().show();

})

$('.checkInProgressFilter').on('click', function() {
    
    $('.razd').parent().parent().parent().hide();
    $('.checkInProgress').parent().parent().parent().show();

})

$('.checkCompleteFilter').on('click', function() {
    
    $('.razd').parent().parent().parent().hide();
    $('.checkComplete').parent().parent().parent().show();

})

});