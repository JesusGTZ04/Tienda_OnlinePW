
document.addEventListener('DOMContentLoaded', function () {

    console.log("JS cargado correctamente");

    const validator = new JustValidate('#form-articulos', {
        errorFieldCssClass: 'is-invalid',
        successFieldCssClass: 'is-valid',
        focusInvalidField: true,
        lockForm: true,
    });

    validator
        .addField('#nombre', [
            {
                rule: 'required',
                errorMessage: 'El nombre es obligatorio',
            },
        ])
        .addField('#descripcion', [
            {
                rule: 'required',
                errorMessage: 'La descripción es obligatoria',
            },
            {
                rule: 'minLength',
                value: 10,
                errorMessage: 'Debe tener al menos 10 caracteres',
            },
        ])
        .addField('#precio', [
            {
                rule: 'required',
                errorMessage: 'El precio es obligatorio',
            },
            {
                rule: 'number',
                errorMessage: 'Debe ser un número válido',
            },
            {
                validator: (value) => parseFloat(value) > 0,
                errorMessage: 'El precio debe ser mayor que 0',
            },
        ])
        .addField('#categoria', [
            {
                rule: 'required',
                errorMessage: 'Selecciona una categoría',
            },
        ])
        .addField('#subcategoria', [
            {
                rule: 'required',
                errorMessage: 'Selecciona una subcategoría',
            },
        ])
        .addField('#stock', [
            {
                rule: 'required',
                errorMessage: 'El stock es obligatorio',
            },
            {
                rule: 'number',
                errorMessage: 'Debe ser un número válido',
            },
            {
                validator: (value) => parseInt(value) >= 1,
                errorMessage: 'Debe ser al menos 1',
            },
        ])
        .addField('#genero', [
            {
                rule: 'required',
                errorMessage: 'Ingresa el género del artículo',
            },
        ])
        .addField('#imagen', [
            {
                rule: 'required',
                errorMessage: 'Selecciona una imagen',
            },
            {
                rule: 'minFilesCount',
                value: 1,
                errorMessage: 'Selecciona al menos un archivo',
            },
            {
                rule: 'files',
                value: {
                    files: {
                        extensions: ['jpg', 'jpeg', 'png', 'webp'],
                        maxSize: 2 * 1024 * 1024, // 2 MB
                    },
                },
                errorMessage: 'Solo se permiten imágenes (JPG, PNG, WEBP) de máximo 2 MB',
            },
        ])
        .onSuccess((event) => {
            // Si todo está correcto, enviamos el formulario
            event.target.submit();
        });
});
