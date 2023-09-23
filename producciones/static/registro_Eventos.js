const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input, #formulario textarea');

const expresiones = {
	nombreEv: /^[a-zA-ZÀ-ÿ\s]{1,100}$/, 
	horaEv: /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/,
	descripEv: /^[a-zA-Z0-9\s\.\,\;\:\-]{1,150}$/,
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
	if(!(campos.nombreEv && campos.horaEv && campos.descripEv)){
		e.preventDefault();
	}
	else{
		document.querySelectorAll('.nombre_correcto').forEach((icono) => {
			icono.classList.remove('nombre_correcto');
		});
	}
});
