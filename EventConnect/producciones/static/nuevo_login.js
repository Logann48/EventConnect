const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');

const expresiones = {
	cedula: /^\d{7,8}$/, // 7 a 8 digitos.
	password: /^[A-Za-z0-9]{4,12}$/, // 4 a 12 digitos, solo letras y numeros.
}

const campos = {
	cedula: false,
	password: false
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "cedula":
			validarCampo(expresiones.cedula, e.target, 'cedula');
		break;
		case "password":
			validarCampo(expresiones.password, e.target, 'password');
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
	if(!(campos.cedula && campos.password)){
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
