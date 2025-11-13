document.addEventListener('DOMContentLoaded', () => {
    console.log("JS cargado correctamente");
    const contenedor = document.getElementById('contenido-dinamico');
    const enlacesMenu = document.querySelectorAll('#menu-navegacion a');

    const setActiveLink = (target) => {
        enlacesMenu.forEach(link => {
            link.classList.remove('active');
        });
        const newActiveLink = document.querySelector(`[data-target="${target}"]`);
        if (newActiveLink) {
            newActiveLink.classList.add('active');
        }
    };

    // Función para cargar el contenido
    const cargarContenido = async (url, target) => {
        try {
            
            contenedor.innerHTML = '<div class="loading-spinner">Cargando...</div>'; 

            //Cargar el HTML vía fetch
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' 
                }
            });
            if (!response.ok) {
                throw new Error(`Error al cargar el contenido: ${response.statusText}`);
            }
            const html = await response.text();

            // Inyectar el nuevo HTML
            contenedor.innerHTML = html;
            
            // Actualizar la URL en el navegador y el estado del menú
            window.history.pushState({ path: url, target: target }, '', url);
            setActiveLink(target);
            
            // 
            ejecutarScripts(contenedor);

        } catch (error) {
            console.error('AJAX Falló:', error);
            contenedor.innerHTML = '<h1>Error al cargar la página.</h1>';
        }
    };

    // Función para ejecutar scripts dentro del contenido cargado
    const ejecutarScripts = (container) => {
        container.querySelectorAll('script').forEach(oldScript => {
            const newScript = document.createElement('script');
            Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
            newScript.appendChild(document.createTextNode(oldScript.innerHTML));
            
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });
    };

    // Event Listener para los enlaces del menú
    enlacesMenu.forEach(link => {
        link.addEventListener('click', (e) => {
        
        const url = link.getAttribute('data-url');
        const target = link.getAttribute('data-target');

        if (url) {
            e.preventDefault();
        }
        
        if (url && target) {
            cargarContenido(url, target);
        }
    });
    });
    
    // Manejar el botón de retroceso del navegador
    window.addEventListener('popstate', (e) => {
        if (e.state && e.state.path && e.state.target) {
            cargarContenido(e.state.path, e.state.target);
        } else {
            const initialLink = document.querySelector('.boton-menu.active');
            if(initialLink){
                 cargarContenido(initialLink.getAttribute('data-url'), initialLink.getAttribute('data-target'));
            }
        }
    });

    const currentPath = window.location.pathname.replace(/\/$/, '');
    let linkToLoad = null;

    enlacesMenu.forEach(link => {
        const linkHref = link.getAttribute('href').replace(/\/$/, '');
        
        if (linkHref === currentPath) {
            linkToLoad = link;
        }
    });

    if (linkToLoad) {
        cargarContenido(linkToLoad.getAttribute('data-url'), linkToLoad.getAttribute('data-target'));
    } else {
        const initialLink = document.querySelector('[data-target="articulos"]');
        const initialUrl = initialLink ? initialLink.getAttribute('data-url') : null;
        const initialTarget = initialLink ? initialLink.getAttribute('data-target') : null;

        if (initialUrl && initialTarget && contenedor.innerHTML.trim() === '') {
            cargarContenido(initialUrl, initialTarget);
        }
    }
});