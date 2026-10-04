# Tarea Semana 16 - Organización Modular y Manejo de Eventos en Python

## Propósito
Evolución de la aplicación `restaurante_app` incorporando la gestión básica de usuarios (CRUD) con interfaz gráfica Tkinter y arquitectura modular basada en POO.

## Eventos e Interacciones Implementadas
- **`<<TreeviewSelect>>`**: Evento asignado mediante `bind()` a la tabla de usuarios. Al seleccionar una fila, carga automáticamente los datos correspondientes en el formulario.
- **`<<ComboboxSelected>>`**: Captura el cambio del selector de rol.
- **`<Return>`**: Atajo de teclado (Enter) para ejecutar directamente el registro de un usuario.
- **`<Escape>`**: Atajo de teclado que limpia los campos del formulario y deselecciona los elementos de la tabla.
- **`command=`**: Utilizado para la ejecución directa de las funciones en los botones (Registrar, Actualizar, Eliminar y Limpiar).

## Roles y Permisos
- **Administrador**: Posee acceso total al módulo de Gestión de Usuarios.
- **Empleado / Cliente**: La pestaña de administración de usuarios muestra un mensaje de acceso restringido.

## Persistencia
Todos los cambios realizados sobre usuarios se persisten mediante el archivo JSON ubicado en `datos/usuarios.json`.

## Ejecución del Sistema
Para iniciar el sistema ejecute el archivo principal desde la consola:

    python main.py

## Credenciales de Prueba
- **Admin**: Usuario: `admin` | Contraseña: `1234`
- **Empleado**: Usuario: `cperez` | Contraseña: `1234`
- **Cliente**: Usuario: `agomez` | Contraseña: `1234`