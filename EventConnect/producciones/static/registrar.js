const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');

const expresiones = {
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	apellido: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	cedula: /^\d{7,8}$/, // 7 a 8 digitos.
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefono: /^(0412|0424|0414|0416)\d{7}$/, // 11 digitos, empezando con 0412, 0424, 0414 o 0416.
	direccion: /^.{1,100}$/, // 1 a 100 caracteres.
	password: /^[A-Za-z0-9]{4,12}$/, // 4 a 12 digitos, solo letras y numeros.
}

const campos = {
	nombre: false,
	apellido: false,
	cedula: false,
	correo: false,
	telefono: false,
	direccion: false,
	password: false
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "nombre":
			validarCampo(expresiones.nombre, e.target, 'nombre');
		break;
		case "apellido":
			validarCampo(expresiones.apellido, e.target, 'apellido');
		break;
		case "cedula":
			validarCampo(expresiones.cedula, e.target, 'cedula');
		break;
		case "correo":
			validarCampo(expresiones.correo, e.target, 'correo');
		break;
		case "telefono":
			validarCampo(expresiones.telefono, e.target, 'telefono');
		break;
		case "direccion":
			validarCampo(expresiones.direccion, e.target, 'direccion');
		break;
		case "password":
			validarCampo(expresiones.password, e.target, 'password');
		break;
	}
}

const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		document.getElementById(`${campo}`).classList.add('nombre_correcto');
		document.getElementById(`${campo}`).classList.remove('nombre_incorrecto');
		campos[campo] = true;
	} else {
		document.getElementById(`${campo}`).classList.remove('nombre_correcto');
		document.getElementById(`${campo}`).classList.add('nombre_incorrecto');
		campos[campo] = false;
	}
}

inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});

formulario.addEventListener('submit', (e) => {
	if(!(campos.nombre && campos.cedula && campos.correo && campos.telefono && campos.direccion && campos.password)){
		e.preventDefault();
		const obj = {
			nombre: campos.nombre,
			apellido: campos.apellido,
			cedula: campos.cedula,
			correo: campos.correo,
			telefono: campos.telefono,
			direccion: campos.direccion,
			password: campos.password
		}

		console.log(obj);
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
		document.getElementById('formulario__mensaje').innerText = 'Please fill all fields correctly';
	}
	else{
		document.getElementById('formulario__mensaje').classList.remove('formulario__mensaje-activo');
		document.querySelectorAll('.nombre_correcto').forEach((icono) => {
			icono.classList.remove('nombre_correcto');
		});
	}
});


