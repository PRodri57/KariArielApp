```markdown
# KariArielApp

Aplicación de escritorio desarrollada en **Python** con **PySide6** e integrada con **Supabase**.  
Permite la gestión de usuarios mediante autenticación (login / registro) y ofrece una interfaz gráfica moderna y modular.

---

## 🚀 Características principales
- Interfaz gráfica construida con **PySide6 (Qt)**.  
- Autenticación de usuarios con **Supabase**.  
- Gestión segura de credenciales mediante **dotenv** y **cryptography**.  
- Organización modular del código: `model`, `view`, `utils`, `config`.  
- Integración de imágenes e íconos personalizados.  

---

## 📂 Estructura del proyecto
```

KariArielApp/
│── assets/     # Imágenes e íconos del proyecto
│── config/     # Configuraciones de la base de datos (Supabase, etc.)
│── model/      # Modelos y clases de la aplicación
│── utils/      # Microservicios y pseudo-frameworks de soporte
│── view/       # Interfaces gráficas (Qt)
│── run\_qt.py   # Punto de entrada principal de la app
│── mainGUI\_qt.py
│── login\_qt.py
│── .env        # Variables de entorno (API keys, configuración sensible)

````

---

## 🛠️ Instalación y configuración

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/PRodri57/KariArielApp.git
   cd KariArielApp
````

2. **Crear entorno virtual (opcional, recomendado)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

   *(Si no existe el archivo `requirements.txt`, instalá manualmente)*:

   ```bash
   pip install python-dotenv pyside6 cryptography supabase pillow
   ```

4. **Configurar variables de entorno**
   Crear un archivo `.env` en la raíz del proyecto con los datos de Supabase:

   ```ini
   SUPABASE_URL=tu_url_de_supabase
   SUPABASE_KEY=tu_api_key
   ```

---

## ▶️ Uso

Ejecutar la aplicación con:

```bash
python run_qt.py
```

* Ingresar credenciales si ya tenés cuenta.
* O bien, crear un nuevo usuario desde la misma interfaz.

---

## 📦 Dependencias principales

* [PySide6](https://doc.qt.io/qtforpython/) – Interfaz gráfica Qt.
* [Supabase-py](https://github.com/supabase-community/supabase-py) – Cliente Python para Supabase.
* [python-dotenv](https://pypi.org/project/python-dotenv/) – Manejo de variables de entorno.
* [cryptography](https://pypi.org/project/cryptography/) – Seguridad y encriptación.
* [Pillow](https://pypi.org/project/Pillow/) – Manipulación de imágenes.


---

## 👤 Autor

Desarrollado por [PRodri57](https://github.com/PRodri57)
