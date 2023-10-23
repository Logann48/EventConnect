const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input, #formulario textarea');

const expresiones = {
	nombreEv: /^[a-zA-ZÀ-ÿ0-9\s]{1,100}$/, // Permitir números
	horaEv: /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/,
	descripEv: /^[a-zA-Z0-9\s\.\,\;\:\-ñÑ]{1,150}$/, // Permitir la letra "ñ"
	tipo: /^[a-zA-Z0-9]{1,15}$/,
	precio: /^\d+(\.\d{1,2})?$/
}

const campos = {
	nombreEv: false,
	horaEv: false,
	descripEv: false
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "nombreEv":
			validarCampo(expresiones.nombreEv, e.target, 'nombreEv');
		break;
		case "horaEv":
			validarCampo(expresiones.horaEv, e.target, 'horaEv');
		break;
		case "descripEv":
			validarCampo(expresiones.descripEv, e.target, 'descripEv');
		break;
		case "myDate":
			validarFecha(e.target, 'myDate');
		break;
		default:
			// Para los campos "tipo" y "precio", iteramos a través de cada uno
			for (let i = 1; i <= 4; i++) {
				if (e.target.name === "tipo" && e.target.id === `tipo${i}`) {
					validarCampo(expresiones.tipo, e.target, `tipo${i}`);
				}
				if (e.target.name === "precio" && e.target.id === `precio${i}`) {
					validarCampo(expresiones.precio, e.target, `precio${i}`);
				}
			}
		break;
	}
}

const validarCampo = (expresion, input, campo) => {
	if (input.value.trim() === '') {
		input.classList.remove('nombre_correcto');
		input.classList.add('nombre_incorrecto');
		campos[campo] = false;
	} else if (expresion.test(input.value)) {
		input.classList.remove('nombre_incorrecto');
		input.classList.add('nombre_correcto');
		campos[campo] = true;
	} else {
		input.classList.remove('nombre_correcto');
		input.classList.add('nombre_incorrecto');
		campos[campo] = false;
	}
}

const validarFecha = (input, campo) => {
	let fechaSeleccionada = new Date(input.value);
	let fechaMinima = new Date();
	fechaMinima.setDate(fechaMinima.getDate() + 1);
	if(fechaSeleccionada >= fechaMinima){
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

	let allValid = Object.values(campos).every((campo) => campo === true);
	for (let i = 1; i <= 4; i++) {
		allValid = allValid && document.getElementById(`tipo${i}`).classList.contains('nombre_correcto');
		allValid = allValid && document.getElementById(`precio${i}`).classList.contains('nombre_correcto');
		allValid = allValid && document.getElementById(`tipo${i}`).value !== '';
		allValid = allValid && document.getElementById(`precio${i}`).value !== '';
	}
	if (!allValid) {
		e.preventDefault();
		alert('Por favor, corrija los campos marcados en rojo antes de enviar el formulario.');
	} else {
		document.querySelectorAll('.nombre_correcto').forEach((icono) => {
			icono.classList.remove('nombre_correcto');
		});
	}
});

