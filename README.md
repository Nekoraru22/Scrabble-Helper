# Scrabble Helper
Una aplicación para ayudarte a encontrar las mejores palabras en Scrabble.

## Instalación fácil y rápida
Simplemente clica dos veces en el archivo `scrabble-helper.exe` para iniciar la aplicación. No se requiere instalación adicional.

## Instalación manual

### Requisitos previos

Antes de comenzar, asegúrate de tener instalados los siguientes programas:

  * **Python 3.x**: Puedes descargarlo desde [python.org](https://www.python.org/).
  * **Node.js y npm**: Node.js incluye **npm** (Node Package Manager) por defecto. Si aún no lo tienes, puedes instalarlo desde [nodejs.org](https://nodejs.org/). Si necesitas instalarlo en Windows y tienes Scoop, puedes hacerlo con el comando `scoop install nodejs`. En macOS, con Homebrew, usa `brew install node`.

-----

### Pasos para la instalación y ejecución

Sigue estos pasos para configurar y ejecutar la aplicación en tu entorno local:

1.  **Configuración del entorno virtual de Python**
    Crea y activa un entorno virtual para aislar las dependencias del proyecto.

    ```bash
    python -m venv myvenv
    myvenv\Scripts\activate
    ```

    En linux o macOS, usa:

    ```bash
    python -m venv myvenv
    source myvenv/bin/activate
    ```

2.  **Instalación de dependencias del backend**
    Instala las librerías de Python requeridas desde el archivo `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

3.  **Instalación de dependencias del frontend**
    Navega al directorio del frontend e instala las dependencias de Node.js.

    ```bash
    cd scrabble-helper
    npm install
    ```

4.  **Compilación del frontend**
    Compila el código del frontend para preparar los archivos estáticos necesarios para la aplicación.

    ```bash
    npm run build
    ```

5.  **Ejecución de la aplicación**
    Regresa al directorio raíz y ejecuta el script principal de Python para iniciar la aplicación.

    ```bash
    cd ..
    python main.py
    ```

¡Listo\! La aplicación ya debería estar funcionando. Si tienes algún problema, no dudes en abrir un *issue* en este repositorio.

## Compilación del proyecto en un ejecutable
### Instalar PyInstaller
Execute `./compile.bat` to create the executable file.