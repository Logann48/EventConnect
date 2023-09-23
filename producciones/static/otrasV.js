const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');

const expresiones = {
	cedula: /^[0-9]{6,10}$/, // numeros
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,100}$/, // Letras y espacios, pueden llevar acentos.
	password: /^.{4,12}$/, // 4 a 12 digitos.
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefono: /^\d{7,14}$/,// 7 a 14 numeros.
	direccion: /^.{1,100}$/,
	nombreEv: /^.{1,100}$/,
	nroTrans: /^\d{4,14}$/,
	monto: /^\d{1,15}$/
}

const campos = {
	cedula: false,
	nombre: false,
	apellido: false,
	password: false,
	correo: false,
	telefono: false,
	direccion: false,
	nombreEv:false,
	nroTrans:false,
	monto:false
}


const validarFormulario = (e) => {
	switch (e.target.name) {
		case "cedula":
			validarCampo(expresiones.cedula, e.target, 'cedula');
			console.log(typeof expresiones.password)
		break;
		case "apellido":
			validarCampo(expresiones.nombre, e.target, 'apellido');
		break;
		case "nombre":
			validarCampo(expresiones.nombre, e.target, 'nombre');
		break;
		case "password":
			validarCampo(expresiones.password, e.target, 'password');
		break;
		case "nombreEv":
			validarCampo(expresiones.nombreEv, e.target, 'nombreEv');
		break;
		case "monto":
			validarCampo(expresiones.monto, e.target,'monto');
		break;
		case "password2":
			validarPassword2();
		break;
		case "correo":
			validarCampo(expresiones.correo, e.target, 'correo');
		break;
		case "telefono":
			validarCampo(expresiones.telefono, e.target, 'telefono');
		break;
		case "nroTrans":
			validarCampo(expresiones.nroTrans, e.target, 'nroTrans');
		break;
		case "direccion":
			validarCampo(expresiones.direccion, e.target, 'direccion');
		break;
	}
}

const validarCampo = (expresion, input, campo) => {
    if(input.value.trim() === '') {
        document.getElementById(`${campo}`).classList.add('nombre_incorrecto');
        document.getElementById(`${campo}`).classList.remove('nombre_correcto');
        campos[campo] = false;
    } else if(expresion.test(input.value)){
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


formulario.addEventListener('submit',(e) => {
    // Verificar que todos los campos requeridos estén llenos
    let valid = true;
    for (let key in campos) {
        if (campos[key] === false) {
            valid = false;
            break;
        }
    }

    // Si todos los campos requeridos están llenos, procesar el formulario
    if (valid) {

    } else {
        e.preventDefault();
        alert('Por favor, llena todos los campos requeridos antes de enviar el formulario.');
        return;
    }
});