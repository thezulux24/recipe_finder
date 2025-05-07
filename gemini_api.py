import streamlit as st
import google.generativeai as genai
import os


GENAI_API_KEY = st.secrets.get("gemini_api_key") 

model = None 

if GENAI_API_KEY:
    try:
        genai.configure(api_key=GENAI_API_KEY)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        print("Modelo Gemini inicializado exitosamente al cargar el módulo.")
    except Exception as e:
        print(f"Error al configurar Gemini API o el modelo inicialmente: {e}")

else:
    print("API key de Gemini no encontrada en st.secrets al cargar el módulo.")


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
        if not ingredients: 
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
    Incluye soporte para extraer un enlace a una imagen representativa de la receta.
    """
    global model
    global GENAI_API_KEY 

    if not model:
        print("El modelo no está inicializado. Intentando re-inicializar...")
        current_api_key_retry = st.secrets.get("gemini_api_key")
        if current_api_key_retry:
            if not GENAI_API_KEY: 
                 GENAI_API_KEY = current_api_key_retry
            try:
                genai.configure(api_key=current_api_key_retry)
                model = genai.GenerativeModel(model_name="gemini-2.0-flash-latest")
                print("Modelo Gemini re-inicializado exitosamente en get_recipe_from_gemini.")
            except Exception as e:
                print(f"Error al re-configurar Gemini API en get_recipe_from_gemini: {e}")
                return f"Error al re-configurar la IA: {e}", None
        
        if not model: 
            print("Fallo al re-inicializar el modelo. API key podría faltar o ser inválida.")
            return "Error: La API key de Gemini no está configurada correctamente en los secretos de Streamlit (st.secrets) o el modelo no pudo ser inicializado. Por favor, verifica la configuración de secretos de la app.", None
    
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
        
        # Agregar solicitud de imagen al prompt
        final_prompt += "\nAdemás, proporciona un enlace a una imagen representativa de la receta, si es posible."

        print(f"Enviando prompt a Gemini: {final_prompt[:200]}...") 
        response = model.generate_content(final_prompt)
        print("Respuesta recibida de Gemini.")
        
        if hasattr(response, 'text'):
            recipe_text = response.text
            # Extraer enlace de imagen de la respuesta
            image_url = extract_image_url(recipe_text)
            return recipe_text, image_url
        elif response.parts and hasattr(response.parts[0], 'text'):
            recipe_text = response.parts[0].text
            image_url = extract_image_url(recipe_text)
            return recipe_text, image_url
        else:
            try:
                if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                    recipe_text = response.candidates[0].content.parts[0].text
                    image_url = extract_image_url(recipe_text)
                    return recipe_text, image_url
            except (AttributeError, IndexError):
                pass 
            
            print(f"Respuesta inesperada de Gemini (no se pudo extraer texto): {response}")
            return "Error: No se pudo extraer el texto de la respuesta de Gemini. La estructura de la respuesta puede haber cambiado o estar vacía.", None

    except Exception as e:
        print(f"Error completo en la llamada a Gemini API: {e}") 
        error_message = f"Error al contactar con la IA para generar la receta. (Detalle: {str(e)[:150]}...)"
        return error_message, None


def extract_image_url(recipe_text):
    """
    Extrae un enlace a una imagen de la receta desde el texto generado.
    Busca patrones comunes de URLs en el texto.
    """
    import re
    url_pattern = r'(https?://[^\s]+)'  # Patrón para encontrar URLs
    match = re.search(url_pattern, recipe_text)
    if match:
        return match.group(0)
    return None