import streamlit as st # Import Streamlit
import google.generativeai as genai
import os
# from dotenv import load_dotenv # Ya no es necesario

# load_dotenv()  # Ya no es necesario

# Obtiene la API key desde st.secrets
# Asegúrate de que el nombre de la clave aquí coincida con el de tu archivo secrets.toml
#GENAI_API_KEY = st.secrets.get("gemini_api_key") 
GENAI_API_KEY = st.secrets["gemini_api_key"] 
# Configura genai con la API key
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest") 
else:
    model = None
    # Opcional: Mostrar una advertencia en la app si la clave no está configurada al iniciar
    # st.warning("La API key de Gemini no está configurada en los secretos de Streamlit. La funcionalidad de IA estará deshabilitada.")


def generate_recipe_prompt(ingredients, diet_restrictions=None, fitness_goal=None, unavailable_utensils=None):
    """
    Crea un prompt para Gemini solicitando recetas, incluyendo objetivos de fitness, 
    restricciones de utensilios y formato específico.
    Maneja el caso de no tener ingredientes para una receta aleatoria.
    """
    if ingredients and len(ingredients) > 0:
        prompt_intro = f"Actúa como un chef experto y nutricionista deportivo. Dame una receta detallada que use principalmente los siguientes ingredientes: {', '.join(ingredients)}."
    else:
        prompt_intro = "Actúa como un chef experto y nutricionista deportivo. Sorpréndeme con una receta creativa, deliciosa y relativamente fácil de preparar."

    prompt = prompt_intro
    
    if diet_restrictions:
        prompt += f" La receta debe ser apta para: {', '.join(diet_restrictions)}."
    
    if fitness_goal and fitness_goal != "General":
        prompt += f" Esta receta debe estar optimizada para el objetivo de '{fitness_goal}'."
    else: 
        if not ingredients: # Si no hay ingredientes, el objetivo fitness es el principal descriptor
             prompt += f" Esta receta debe ser ideal para un enfoque '{fitness_goal}' en general."
    
    if unavailable_utensils:
        prompt += f" IMPORTANTE: La receta NO debe requerir el uso de los siguientes utensilios: {', '.join(unavailable_utensils)}."

    prompt += """

Por favor, formatea la respuesta de la siguiente manera usando Markdown:

## Nombre de la Receta

**Tiempo estimado de preparación:** (ej: 20 minutos)
**Tiempo estimado de cocción:** (ej: 30 minutos)
**Dificultad:** (ej: Fácil/Media/Difícil)
**Ideal para:** (Aquí puedes reiterar el objetivo fitness o el tipo de plato si es aleatorio, ej: Comida Ligera y Saludable / Una Sorpresa Deliciosa)

### Ingredientes:
(Lista con guiones, incluyendo cantidades exactas)
- Cantidad - Ingrediente 1
- Cantidad - Ingrediente 2

### Pasos de Preparación:
(Lista numerada. Cada paso debe ser MUY DETALLADO y EXPLICATIVO. Incluye técnicas, temperaturas si son relevantes, y el porqué de ciertas acciones si ayuda a la comprensión. No escatimes en detalles para asegurar que alguien con poca experiencia pueda seguirla fácilmente.)
1. **Preparación Inicial:** Describe detalladamente cómo preparar los ingredientes antes de cocinar (lavar, picar, medir, etc.). Por ejemplo, 'Pica la cebolla en brunoise fina (cuadritos pequeños de unos 2-3 mm). Para ello, corta la cebolla por la mitad...'
2. **Proceso de Cocción Principal:** Explica cada fase de la cocción con sumo detalle. Por ejemplo, 'Calienta una sartén grande a fuego medio-alto. Añade una cucharada de aceite de oliva. Cuando el aceite esté caliente (verás que brilla un poco), añade la cebolla picada y sofríe durante 5-7 minutos, removiendo ocasionalmente, hasta que esté traslúcida y ligeramente dorada. Esto desarrolla su dulzor.'
3. **Pasos Siguientes y Finalización:** Continúa con el mismo nivel de detalle para el resto de la receta, incluyendo cómo saber cuándo está lista, cómo servir, etc.

### Notas Adicionales o Consejos:
(Si aplica, por ejemplo, cómo ajustar para más proteína, o alternativas de ingredientes)

### Estimación Nutricional (por porción):
(Indica que es una estimación)
- Calorías: Aproximadamente X kcal
- Proteínas: Aproximadamente Y g
- Carbohidratos: Aproximadamente Z g
- Grasas: Aproximadamente A g

Asegúrate de que la respuesta sea clara, concisa y fácil de seguir, especialmente en los pasos de preparación.
"""
    return prompt

def generate_pro_recipe_prompt(essential_ingredients, nutritional_targets, diet_restrictions=None, unavailable_utensils=None):
    """
    Crea un prompt para Gemini para el Modo Pro, enfocándose en macros, sugiriendo ingredientes y considerando utensilios no disponibles.
    """
    prompt = f"Actúa como un nutricionista deportivo y chef de élite. Necesito una receta que cumpla con los siguientes objetivos nutricionales por porción: \n"
    prompt += f"- Calorías: Aproximadamente {nutritional_targets['calories']} kcal\n"
    prompt += f"- Proteínas: Aproximadamente {nutritional_targets['protein']} g\n"
    prompt += f"- Carbohidratos: Aproximadamente {nutritional_targets['carbs']} g\n"
    prompt += f"- Grasas: Aproximadamente {nutritional_targets['fats']} g\n\n"
    
    prompt += f"Debes utilizar OBLIGATORIAMENTE los siguientes ingredientes esenciales que ya tengo: {', '.join(essential_ingredients)}.\n"
    prompt += "Si es necesario para alcanzar los macros o mejorar la receta, puedes sugerir ingredientes ADICIONALES, indicando claramente cuáles son los esenciales que proporcioné y cuáles son sugerencias tuyas.\n"

    if diet_restrictions:
        prompt += f"La receta también debe ser apta para: {', '.join(diet_restrictions)}.\n"

    if unavailable_utensils:
        prompt += f"MUY IMPORTANTE: La receta NO debe requerir el uso de los siguientes utensilios de cocina: {', '.join(unavailable_utensils)}. Adapta las técnicas de cocción si es necesario.\n"

    prompt += """
Por favor, estructura la receta de la siguiente manera usando Markdown:

## Nombre de la Receta Pro

**Objetivos Nutricionales Clave:**
- Calorías: ~X kcal
- Proteínas: ~Y g
- Carbohidratos: ~Z g
- Grasas: ~A g

**Tiempo estimado de preparación:** (ej: 25 minutos)
**Tiempo estimado de cocción:** (ej: 35 minutos)
**Dificultad:** (ej: Media)

### Ingredientes:
(Indica claramente cuáles son los **[ESENCIALES PROPORCIONADOS]** y cuáles son **[SUGERIDOS ADICIONALES]**)
- Cantidad - Ingrediente 1 [ESENCIAL PROPORCIONADO / SUGERIDO ADICIONAL]
- Cantidad - Ingrediente 2 [ESENCIAL PROPORCIONADO / SUGERIDO ADICIONAL]

### Pasos de Preparación:
(Lista numerada. Cada paso debe ser EXTREMADAMENTE DETALLADO, PROFESIONAL y EXPLICATIVO, como si se lo explicaras a un aprendiz de cocina que necesita entender cada técnica y el porqué de cada acción. Incluye temperaturas exactas, tiempos precisos, técnicas culinarias específicas (ej: 'deglasear', 'montar al pil pil'), y consejos para asegurar el éxito y la calidad del plato. No omitas ningún detalle crucial.)
1. **Mise en Place Detallada:** Describe con precisión cómo preparar cada ingrediente antes de comenzar la cocción. Por ejemplo, 'Para el pollo, asegúrate de que esté a temperatura ambiente. Sécalo completamente con papel de cocina para un dorado óptimo. Corta las pechugas en medallones de 2 cm de grosor, buscando uniformidad para una cocción pareja.'
2. **Técnicas de Cocción Avanzadas (si aplica) y Proceso Principal:** Explica cada fase con un lenguaje técnico pero comprensible. Por ejemplo, 'En una sartén de fondo grueso, calienta el aceite de oliva virgen extra a 180°C (fuego medio-alto). Sella los medallones de pollo por tandas, 2-3 minutos por cada lado, hasta obtener una costra dorada (reacción de Maillard). Retira y reserva. En la misma sartén, añade la chalota finamente picada y pocha a fuego bajo durante 8-10 minutos hasta que esté caramelizada, removiendo constantemente para evitar que se queme.'
3. **Integración y Finalización del Plato:** Continúa con el mismo nivel de detalle hasta el emplatado, explicando cómo integrar los sabores y texturas.

### Justificación de Ingredientes Sugeridos (si aplica):
(Breve explicación de por qué se sugieren ciertos ingredientes adicionales para alcanzar los macros o mejorar el plato)

### Notas del Nutricionista Pro:
(Consejos sobre cómo ajustar la receta, momentos ideales para consumirla según los macros, etc.)

### Estimación Nutricional Detallada (por porción):
(Intenta ser lo más preciso posible con la estimación basada en los ingredientes y cantidades)
- Calorías: X kcal
- Proteínas: Y g
- Carbohidratos: Z g
- Grasas: A g
- Fibra (opcional): B g

Asegúrate de que la receta sea realista, deliciosa y cumpla lo mejor posible con los requerimientos, con una sección de preparación impecablemente detallada.
"""
    return prompt

def get_recipe_from_gemini(ingredients, diet_restrictions=None, fitness_goal=None, unavailable_utensils=None, custom_prompt=None):
    """
    Obtiene una receta de Gemini. Puede usar un prompt pre-generado o construir uno.
    """
    if not model:
        # Intentar obtener la clave de nuevo si el modelo no se inicializó (puede ser útil si los secretos se cargan tarde)
        global GENAI_API_KEY, model
        GENAI_API_KEY = st.secrets.get("gemini_api_key")
        if GENAI_API_KEY:
            genai.configure(api_key=GENAI_API_KEY)
            model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
        
        if not model: # Si sigue sin estar configurado, retorna el error
            return "Error: La API key de Gemini no está configurada en los secretos de Streamlit (st.secrets) o el modelo no pudo ser inicializado."
    
    try:
        final_prompt = custom_prompt
        if not final_prompt: 
            valid_ingredients = []
            if ingredients:
                for item in ingredients:
                    if item.strip(): 
                        valid_ingredients.append(item.strip())
            
            final_prompt = generate_recipe_prompt(
                valid_ingredients, 
                diet_restrictions, 
                fitness_goal,
                unavailable_utensils
            )
        
        response = model.generate_content(final_prompt)
        
        if hasattr(response, 'text'):
            return response.text
        elif response.parts and hasattr(response.parts[0], 'text'):
            return response.parts[0].text
        else:
            try:
                if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                    return response.candidates[0].content.parts[0].text
            except (AttributeError, IndexError):
                pass 
            
            print(f"Respuesta inesperada de Gemini: {response}")
            return "Error: No se pudo extraer el texto de la respuesta de Gemini. La estructura de la respuesta puede haber cambiado."

    except Exception as e:
        print(f"Error completo de API: {e}") 
        error_message = f"Error al contactar con Gemini API. Verifica tu conexión, la API key o los límites de la API. (Detalle: {str(e)[:150]}...)"
        return error_message