document.addEventListener('DOMContentLoaded', function () {

    const validator = new JustValidate('#form-inicio', {
        focusInvalidField: true,
        lockForm: true,
    });

    // Nombre completo
    validator
    .addField('#nombre', [
        { rule: 'required', errorMessage: 'El nombre es obligatorio' },
        { rule: 'minLength', value: 3, errorMessage: 'Debe tener al menos 3 caracteres' }
    ])
    // Correo
    .addField('#correo', [
        { rule: 'required', errorMessage: 'El correo es obligatorio' },
        { rule: 'email', errorMessage: 'Ingresa un correo válido' }
    ])

    // Contraseña
    .addField('#contrasenia', [
        { rule: 'required', errorMessage: 'La contraseña es obligatoria' },
        { rule: 'minLength', value: 8, errorMessage: 'Debe tener al menos 8 caracteres' }
    ])

    // Teléfono
    .addField('#telefono', [
        { rule: 'required', errorMessage: 'El teléfono es obligatorio' },
        { rule: 'number', errorMessage: 'Solo se permiten números' },
        { validator: (value) => /^[0-9]{10}$/.test(value), errorMessage: 'Debe tener 10 dígitos' }
    ])

    // Evento al enviar
    .onSuccess((event) => {
        event.target.submit();
    });
});