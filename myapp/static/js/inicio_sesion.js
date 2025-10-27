document.addEventListener('DOMContentLoaded', function () {

    const validator = new JustValidate('#form-inicio', {
        focusInvalidField: true,
        lockForm: true,
    });

    validator
        .addField('#usuario', [
            {
                rule: 'required',
                errorMessage: 'El correo es obligatorio',
            },
            {
                rule: 'email',
                errorMessage: 'Ingresa un correo válido',
            }
        ])
        .addField('#password', [
            {
                rule: 'required',
                errorMessage: 'La contraseña es obligatoria',
            },
            {
                rule: 'minLength',
                value: 8,
                errorMessage: 'La contraseña debe tener al menos 8 caracteres',
            }
        ])
        .onSuccess((event) => {
            // Formulario válido: se envía
            event.target.submit();
        });
});
