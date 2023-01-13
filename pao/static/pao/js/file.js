window.onload = init;

function deleteWarning() {
    
    const elem = document.getElementById("formAlert");
    elem.remove();
}

function init() {

    const radiobtn = document.getElementById("id_types_0");
    radiobtn.checked = true;
}