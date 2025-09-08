#  📋 Procesos de Configuración del Sistema de Ventas Concurrentes
## Creado en Flet y Python 




**🏗️ 1. Creación del Entorno Virtual (VENV)**  

*Python -m venv venv*  

¿Por qué es necesario?
La creación de un entorno virtual es un paso fundamental en el desarrollo con Python. Este proceso permite aislar las dependencias y versiones de paquetes específicos para nuestro proyecto, evitando conflictos con otras aplicaciones Python instaladas en el sistema.


**⚡ 2. Activación del Entorno Virtual**  

*venv/Scripts/activate*  

¿Qué significa activar el VENV?
La activación configura la sesión actual de la terminal para utilizar el Python y los paquetes instalados dentro del entorno virtual, en lugar de los globales del sistema.

Cambios que ocurren:

🔄 Redirección de comandos Python y pip al entorno virtual

🌐 Modificación temporal de las variables de entorno del sistema

✅ Indicador visual (venv) que confirma la activación

📍 Rutas específicas para importación de módulos

**🐍 3. Instalación de Python y Flet dentro del Entorno Virtual** 

*pip install flet*  

¿Por qué instalar dentro del VENV?
Aunque Python ya está instalado en el sistema, es necesario asegurar que el entorno virtual tenga acceso a todas las capacidades necesarias y instalar Flet específicamente en este espacio aislado.

**📷 6. Capturas del proyecto** 

📍 Ventana inicial:

![captura](./arch01.png)

📍 Ejemplo de ejecución:

![captura](./archi02.png)

📍 Ventana de login:

![captura](./arc03.png)

📍 Ejemplo de ejecución:

![captura](./arc04.png)