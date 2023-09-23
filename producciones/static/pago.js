document.getElementById('check1').addEventListener('change', function() {
    if(this.checked) {
        document.getElementById('telefono').placeholder = "1234";
        document.getElementById('cuenta').innerText = "últimos 7 digitos de la cuenta";
        document.getElementById('check2').checked = false;
    } else {
        // reset the placeholder and text when checkbox is unchecked
        document.getElementById('telefono').placeholder = "Ej: 04145555555";
        document.getElementById('cuenta').innerText = "Número de teléfono";
    }
});

document.getElementById('check2').addEventListener('change', function() {
    if(this.checked) {
        document.getElementById('check1').checked = false;
        // reset the placeholder and text when checkbox is checked
        document.getElementById('telefono').placeholder = "Ej: 04145555555";
        document.getElementById('cuenta').innerText = "Número de teléfono";
    }
});