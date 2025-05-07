# 🍳🥗 Recipe Finder Pro & Fitness AI 🏋️‍♂️✨

¡Transforma los ingredientes que tienes en casa en deliciosas recetas personalizadas y alcanza tus metas de fitness con la ayuda de la Inteligencia Artificial!

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://TU_LINK_A_LA_APP_STREAMLIT_AQUI) 



## 🌟 Características Principales

*   **Búsqueda Inteligente de Recetas:** Ingresa los ingredientes que tienes y obtén sugerencias de recetas al instante.
*   **Modo "Sorpréndeme":** ¿No sabes qué cocinar? Deja que la IA te inspire con una receta aleatoria y deliciosa.
*   **🎯 Modo Pro Nutrición Avanzada:**
    *   Define tus **objetivos macro-nutricionales** (calorías, proteínas, carbohidratos, grasas).
    *   Indica **ingredientes esenciales** que quieres usar.
    *   Recibe recetas optimizadas que te ayudarán a cumplir tus metas, con sugerencias de ingredientes adicionales si es necesario.
*   **Filtros Personalizados:**
    *   **Restricciones Dietéticas:** Vegano, Vegetariano, Sin Gluten, Keto, Paleo, y más.
    *   **Objetivos Fitness:** Ganar Masa Muscular, Pérdida de Grasa, Energía Pre-Entreno, etc.
    *   **Utensilios No Disponibles:** ¿No tienes horno? ¡No hay problema! La IA adaptará las recetas.
*   **Instrucciones Detalladas:** Pasos de preparación explicados minuciosamente, ideales tanto para novatos como para cocineros experimentados.
*   **Estimación Nutricional:** Conoce un aproximado de las calorías y macros por porción.
*   **Interfaz Amigable:** Creada con Streamlit para una experiencia de usuario fluida e intuitiva.
*   **Potenciado por Gemini AI:** Utiliza el poder de los modelos de lenguaje avanzados de Google para generar recetas creativas y precisas.

## 🚀 Cómo Empezar

Sigue estos pasos para ejecutar la aplicación en tu entorno local:

### 1. Prerrequisitos

*   Python 3.8 o superior.
*   Git.

### 2. Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/recipe_finder.git
cd recipe_finder
```

### 3. Crear un Entorno Virtual (Recomendado)

```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar la API Key de Gemini

La aplicación utiliza la API de Gemini de Google. Necesitarás obtener una API key desde [Google AI Studio](https://aistudio.google.com/app/apikey) (o el lugar donde gestiones tus claves de Gemini).

Para configurar tu API key de forma segura usando los secretos de Streamlit:

1.  Crea una carpeta llamada `.streamlit` en la raíz de tu proyecto (si no existe).
2.  Dentro de la carpeta `.streamlit`, crea un archivo llamado `secrets.toml`.
3.  Añade tu API key al archivo `secrets.toml` de la siguiente manera:

    ```toml
    # .streamlit/secrets.toml
    gemini_api_key = "TU_API_KEY_DE_GEMINI_AQUI"
    ```
    Reemplaza `"TU_API_KEY_DE_GEMINI_AQUI"` con tu clave real.

    *(Nota: El archivo `gemini_api.py` está configurado para leer la clave llamada `gemini_api_key` desde `st.secrets`)*

### 6. Ejecutar la Aplicación Streamlit

```bash
streamlit run main.py
```

¡Abre tu navegador en la dirección que te indique Streamlit (generalmente `http://localhost:8501`) y empieza a cocinar!

## 🛠️ Tecnologías Utilizadas

*   **Python:** El lenguaje de programación principal.
*   **Streamlit:** Para construir la interfaz de usuario web interactiva.
*   **Google Gemini API:** Para la generación de recetas mediante IA.
*   **Markdown:** Para el formato de las recetas y este README.

## 🔮 Futuras Mejoras (Ideas)

*   [ ] Guardar recetas favoritas.
*   [ ] Historial de búsquedas.
*   [ ] Opción para ajustar el número de porciones.
*   [ ] Integración con APIs de información nutricional más detallada.
*   [ ] Subir una imagen de ingredientes y que la IA los reconozca.
*   [ ] Soporte para múltiples idiomas.

## 🙌 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la app, no dudes en abrir un *issue* o enviar un *pull request*.

1.  Haz un Fork del proyecto.
2.  Crea tu Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Haz Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`).
4.  Push a la Branch (`git push origin feature/AmazingFeature`).
5.  Abre un Pull Request.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Mira el archivo `LICENSE` para más detalles (si decides añadir uno).

---

¡Esperamos que disfrutes usando Recipe Finder Pro & Fitness AI! Si te gusta, ¡dale una estrella ⭐ al repositorio!
```
