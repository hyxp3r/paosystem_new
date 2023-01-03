
window.onload = init;

function init() {

    var check = document.getElementsByClassName('h5 mb-0 mr-3 font-weight-bold text-gray-800');
    var values = document.getElementsByClassName('progress-bar bg-info');

    values[0].style.width = check[0].textContent


    for (var i = 1; i<30; i++){
        
        values[i].style.width = values[i].textContent

    }
  
    
}
