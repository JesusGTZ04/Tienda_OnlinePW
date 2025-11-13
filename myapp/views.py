from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import transaction

# Create your views here.
def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def index(request):
    productos = Producto.objects.all().prefetch_related('imagenproducto_set')

    carrito = request.session.get('carrito', {})
    cart_count = sum(item.get('cantidad', 0) for item in carrito.values())

    context = {
        'titulo_principal': 'Todos los productos',
        'productos': productos,
        'cart_count': cart_count
    }
    return render(request, 'index.html', context)

@user_passes_test(is_admin)
def admin_main(request):
    articulos = Producto.objects.select_related('subcategoria', 'subcategoria__categoria').all()

    context = {
        'articulos': articulos
    }
    if is_ajax(request):
        return render(request, 'admin_main_content.html', context)
    else:
        return render(request, 'base_admin.html', context)

@user_passes_test(is_admin)
def admin_usuarios(request):
    usuarios_resgistrados = User.objects.all().order_by('email')
    context = {
        'usuarios_registrados': usuarios_resgistrados
    }

    if is_ajax(request):
        return render(request, 'usuarios_content.html', context)
    else:
        return render(request, 'base_admin.html', context)
    
@user_passes_test(is_admin)
def add_articulo(request):
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        genero = request.POST.get('genero')
        descripcion = request.POST.get('descripcion')
        categoria_nombre = request.POST.get('categoria')
        subcategoria_nombre = request.POST.get('subcategoria')
        imagen_archivo = request.FILES.get('imagen')

        try:

            with transaction.atomic():
                categoria, created_cat = Categoria.objects.get_or_create( 
                    nombre_categoria = categoria_nombre)
                
                subcategoria, created_sub = Subcategoria.objects.get_or_create(
                    nombre_subcategoria=subcategoria_nombre,
                    categoria=categoria 
                )

                producto = Producto.objects.create(
                    nombre_producto=nombre,
                    precio=precio,
                    stock=stock,
                    genero=genero,
                    subcategoria=subcategoria,
                    descripcion = descripcion,
                )

                if imagen_archivo:
                   
                    ImagenProducto.objects.create(
                        producto=producto,
                        imagen=imagen_archivo, 
                        principal=True
                    )
            messages.success(request, f"Artículo '{nombre}' agregado exitosamente.")
            return redirect('add_articulo')
        except Exception as e:
            messages.error(request, f"Error al guardar el artículo: {e}")
    return render(request, 'add_articulo.html')

def inicio_sesion(request):
    return render(request, 'inicio_sesion.html')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user = request.user

        first_name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        
        user.first_name = first_name

        if user.email != email:
             user.email = email
             user.username = email

        if hasattr(user, 'telefono'):
            user.telefono = telefono
        if hasattr(user, 'direccion'):
            user.direccion = direccion

        try:
            
            user.full_clean() 
            user.save()

            messages.success(request, 'Tus datos se han actualizado con éxito')
            return redirect('index') 
        
        except IntegrityError:
            messages.error(request, 'Ese correo electrónico ya está registrado por otra cuenta.')
        except Exception as e:
             messages.error(request, f'Error de validación: {e}')
    
    return render(request, 'editar_usuario.html')

@user_passes_test(is_admin)
def eliminar_usuario(request, user_id):
    if request.method == 'POST':
        usuario_elminar = get_object_or_404(User, id=user_id)

        if usuario_elminar == request.user:
            messages.error(request, "No puedes eliminar tu propia cuenta de administrador.")
            return redirect('usuarios')
        
        try:
            nombre_eliminado = usuario_elminar.first_name or usuario_elminar.email
            usuario_elminar.delete()

            messages.success(request, f"El usuario '{nombre_eliminado}' ha sido eliminado.")

        except Exception as e:
            messages.error(request, f"Error al eliminar el usuario: {e}")
    
    return redirect('usuarios')

def registro_usuario(request):
    
    if request.method == 'POST':
        full_name = request.POST.get('nombre')      
        email = request.POST.get('correo')
        password = request.POST.get('contrasenia')  
        telefono = request.POST.get('telefono')
    

        try:
            # Creación y cifrado del usuario
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                telefono=telefono,
                first_name=full_name,
            )

            login(request, user)
            messages.success(request, '¡Registro exitoso! Te hemos iniciado sesión.')
            return redirect('index') 
            
        except IntegrityError:
            # Correo duplicado
            messages.error(request, 'Este correo electrónico ya está registrado.')
            
        except Exception as e:
            messages.error(request, f'Ocurrió un error al guardar: {e}')
            
        return render(request, 'registro.html') 
    return render(request, 'registro.html')

def inicio_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('usuario')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido, {user.first_name}")


            return redirect('index')
        else:
            messages.error(request, "Correo o contraeña incorrectos")

    return render(request, 'inicio_sesion.html')

def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('index')

def add_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    carrito = request.session.get('carrito', {})

    producto_id_str = str(producto.id)

    if producto_id_str in carrito:
        carrito[producto_id_str]['cantidad'] += 1
    else:
        carrito[producto_id_str] = {
            'id': producto.id,
            'nombre': producto.nombre_producto,
            'precio': str(producto.precio),
            'cantidad': 1
        }

    request.session['carrito'] = carrito
    request.session.modified = True

    messages.success(request, f"'{producto.nombre_producto}' agregado al carrito.")

    return redirect('index')

def view_cart(request):
  
    carrito_session = request.session.get('carrito', {})
    carrito_items = []
    total_carrito = Decimal(0) 

    for producto_id_str, data in carrito_session.items():
        try:
            
            producto = Producto.objects.get(id=int(producto_id_str))
           
            imagen_producto = ImagenProducto.objects.filter(producto=producto).first()
        
            # Si hay imagen, usa su URL. Si no, usa None.
            imagen_url = imagen_producto.imagen.url if imagen_producto else None
            
            # Convertimos el precio de string a Decimal para el cálculo.
            precio = Decimal(data.get('precio', '0'))
            cantidad = data.get('cantidad', 0)
            subtotal = precio * cantidad
            total_carrito += subtotal

            # Construir el diccionario final para el template
            carrito_items.append({
                'id': producto.id,
                'nombre': data['nombre'],
                'precio': precio,
                'cantidad': cantidad,
                'subtotal': f'{subtotal:.2f}', 
                'imagen_url': imagen_url,      
            })

        except Producto.DoesNotExist:
            continue
        except Exception as e:
            
            print(f"Error procesando ítem {producto_id_str}: {e}")
            continue

    context = {
        'carrito_items': carrito_items,
        'total_carrito': f'${total_carrito:.2f}', 
    }
    
    return render(request, 'cart.html', context)

def remove_cart(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)
    

    if producto_id_str in carrito:
        # 2. Obtener el nombre del producto 
        nombre_producto = carrito[producto_id_str]['nombre']
        
        # Eliminar el producto del diccionario
        del carrito[producto_id_str]
        
        # Guardar y modificar la sesión
        request.session['carrito'] = carrito
        request.session.modified = True
        
        messages.success(request, f"'{nombre_producto}' eliminado del carrito.")
    
    else:
        messages.error(request, "El producto no se encontró en el carrito.")
        
    # 5. Redirigir de vuelta a la vista del carrito para actualizar la página
    return redirect('carrito')
