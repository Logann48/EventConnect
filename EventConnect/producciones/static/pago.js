const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');

const expresiones = {
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	cedula: /^\d{7,8}$/, // 7 a 8 digitos.
    nroTrans: /^\d{8,11}$/, // 1 a 20 digitos.
    telefono: /^(0412|0424|0414|0416)\d{7}$/, // 11 digitos, empezando con 0412, 0424, 0414 o 0416.
    monto: /^\d+(\.\d{1,2})?$/, // Numeros con hasta dos decimales.
    transferencia: /^\d{4}$/, // Solo 4 digitos.
    pagoMovil: /^(0412|0424|0414|0416)\d{7}$/, // Solo 11 digitos
}

const campos = {
	nombre: false,
	cedula: false,
    nroTrans: false,
    telefono: false,
    monto: false
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "nombre":
			validarCampo(expresiones.nombre, e.target, 'nombre');
		break;
		case "cedula":
			validarCampo(expresiones.cedula, e.target, 'cedula');
		break;
        case "nroTrans":
			validarCampo(expresiones.nroTrans, e.target, 'nroTrans');
		break;
        case "telefono":
			validarCampo(expresiones.telefono, e.target, 'telefono');
		break;
        case "monto":
			validarCampo(expresiones.monto, e.target, 'monto');
		break;
	}
}

const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		document.getElementById(`${campo}`).classList.remove('nombre_incorrecto');
		document.getElementById(`${campo}`).classList.add('nombre_correcto');
		campos[campo] = true;
	} else {
		document.getElementById(`${campo}`).classList.add('nombre_incorrecto');
		document.getElementById(`${campo}`).classList.remove('nombre_correcto');
		campos[campo] = false;
	}
}

inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});

formulario.addEventListener('submit', (e) => {
	if(!(campos.nombre && campos.cedula && campos.nroTrans && campos.telefono && campos.monto)){
		e.preventDefault();
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
	}
	else{
		document.getElementById('formulario__mensaje-exito').classList.add('formulario__mensaje-exito-activo');
		setTimeout(() => {
			document.getElementById('formulario__mensaje-exito').classList.remove('formulario__mensaje-exito-activo');
		}, 5000);

		document.querySelectorAll('.nombre_correcto').forEach((icono) => {
			icono.classList.remove('nombre_correcto');
		});
	}
});

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
