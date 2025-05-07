import streamlit as st
from gemini_api import get_recipe_from_gemini, generate_pro_recipe_prompt 
import re

if 'recipe_suggestion' not in st.session_state:
    st.session_state.recipe_suggestion = None
if 'recipe_title' not in st.session_state:
    st.session_state.recipe_title = ""
if 'pro_recipe_suggestion' not in st.session_state: 
    st.session_state.pro_recipe_suggestion = None
if 'pro_recipe_title' not in st.session_state: 
    st.session_state.pro_recipe_title = ""



st.title("🍳 Buscador de Recetas Inteligente & Fitness 🏋️")


st.sidebar.header("Filtros Generales")
diet_options = ["Ninguna", "Vegano", "Vegetariano", "Sin Gluten", "Bajo en Carbohidratos", "Keto", "Paleo"]
selected_diets = st.sidebar.multiselect("Tipo de Dieta (opcional):", diet_options)

utensil_options = ["Horno", "Microondas", "Licuadora", "Procesador de Alimentos", "Sartén Antiadherente", "Olla a Presión"]
unavailable_utensils = st.sidebar.multiselect("Utensilios NO disponibles (opcional):", utensil_options)

st.sidebar.markdown("---")
st.sidebar.info("App creada con Streamlit y Gemini AI.")


tab1, tab2 = st.tabs(["Búsqueda Normal 🧑‍🍳", "Modo Pro Nutrición Avanzada 🎯"])

with tab1:
    st.header("Búsqueda de Recetas Normal")
    ingredients_input_normal = st.text_area(
        "Escribe los ingredientes que tienes (ej: pollo arroz brócoli)",
        height=100,
        help="Puedes escribir los ingredientes de forma natural, separados por espacios o comas.",
        key="normal_ingredients"
    )

    fitness_goal_options_normal = [
        "General", "Ganar Masa Muscular", "Pérdida de Grasa",
        "Energía Pre-Entreno", "Recuperación Post-Entreno", "Comida Ligera y Saludable"
    ]
    selected_fitness_goal_normal = st.selectbox(
        "Objetivo Fitness/Nutricional:",
        fitness_goal_options_normal,
        key="normal_fitness_goal"
    )

    col1_normal, col2_normal = st.columns(2)
    with col1_normal:
        if st.button("Buscar Recetas 🍳", use_container_width=True, key="normal_search"):
            st.session_state.recipe_suggestion = None 
            if not ingredients_input_normal:
                st.warning("Por favor, ingresa al menos un ingrediente para buscar.")
            else:
                cleaned_input = re.sub(r'[,;]+', ' ', ingredients_input_normal)
                cleaned_input = re.sub(r'\s+', ' ', cleaned_input).strip()
                ingredients_list = [ingredient.lower() for ingredient in cleaned_input.split(' ') if ingredient.strip()]
                actual_diet_restrictions = [diet for diet in selected_diets if diet != "Ninguna"] if selected_diets else None

                if not ingredients_list:
                    st.warning("Por favor, ingresa ingredientes válidos.")
                else:
                    with st.spinner(f"Buscando recetas para '{selected_fitness_goal_normal}'..."):
                        recipe_text = get_recipe_from_gemini(
                            ingredients=ingredients_list,
                            diet_restrictions=actual_diet_restrictions,
                            fitness_goal=selected_fitness_goal_normal,
                            unavailable_utensils=unavailable_utensils 
                        )
                    st.session_state.recipe_suggestion = recipe_text
                    st.session_state.recipe_title = "✨ Tu Receta Personalizada ✨"
    
    with col2_normal:
        if st.button("Sorpréndeme 🎉", use_container_width=True, key="normal_surprise"):
            st.session_state.recipe_suggestion = None
            actual_diet_restrictions = [diet for diet in selected_diets if diet != "Ninguna"] if selected_diets else None
            with st.spinner(f"Buscando una receta sorpresa ({selected_fitness_goal_normal})..."):
                recipe_text = get_recipe_from_gemini(
                    ingredients=None,
                    diet_restrictions=actual_diet_restrictions,
                    fitness_goal=selected_fitness_goal_normal,
                    unavailable_utensils=unavailable_utensils
                )
            st.session_state.recipe_suggestion = recipe_text
            st.session_state.recipe_title = "🎁 ¡Tu Receta Sorpresa! 🎁"


    if st.session_state.recipe_suggestion:
        st.markdown("---")
        st.subheader(st.session_state.recipe_title)
        if st.session_state.recipe_suggestion.startswith("Error:"):
            st.error(st.session_state.recipe_suggestion)
        else:
            st.markdown(st.session_state.recipe_suggestion)

with tab2:
    st.header("Modo Pro: Nutrición Específica")
    st.write("Define tus requerimientos nutricionales y los ingredientes esenciales que tienes.")

    col_pro_1, col_pro_2 = st.columns(2)
    with col_pro_1:
        target_calories = st.number_input("Calorías Objetivo (kcal):", min_value=0, step=100, value=2000)
        target_protein = st.number_input("Proteínas Objetivo (g):", min_value=0, step=5, value=150)
    with col_pro_2:
        target_carbs = st.number_input("Carbohidratos Objetivo (g):", min_value=0, step=10, value=200)
        target_fats = st.number_input("Grasas Objetivo (g):", min_value=0, step=5, value=70)

    essential_ingredients_pro = st.text_area(
        "Ingredientes Esenciales que TIENES (ej: pechuga de pollo, avena, brócoli):",
        height=100,
        help="Lista los ingredientes clave que quieres usar. La IA podrá sugerir otros complementarios.",
        key="pro_ingredients"
    )
    
    if st.button("Generar Receta Pro Nutricional 🎯", use_container_width=True, key="pro_search"):
        st.session_state.pro_recipe_suggestion = None 
        if not essential_ingredients_pro:
            st.warning("Por favor, ingresa al menos un ingrediente esencial.")
        else:
            cleaned_input_pro = re.sub(r'[,;]+', ' ', essential_ingredients_pro)
            cleaned_input_pro = re.sub(r'\s+', ' ', cleaned_input_pro).strip()
            essential_ingredients_list = [ing.lower() for ing in cleaned_input_pro.split(' ') if ing.strip()]
            
            actual_diet_restrictions_pro = [diet for diet in selected_diets if diet != "Ninguna"] if selected_diets else None

            if not essential_ingredients_list:
                st.warning("Por favor, ingresa ingredientes esenciales válidos.")
            else:
                nutritional_targets = {
                    "calories": target_calories,
                    "protein": target_protein,
                    "carbs": target_carbs,
                    "fats": target_fats
                }
                with st.spinner("Diseñando tu receta pro con macros específicos... 🧠💪"):
                    
                    pro_prompt = generate_pro_recipe_prompt(
                        essential_ingredients=essential_ingredients_list,
                        nutritional_targets=nutritional_targets,
                        diet_restrictions=actual_diet_restrictions_pro,
                        unavailable_utensils=unavailable_utensils
                    )
                    recipe_text_pro = get_recipe_from_gemini(
                        ingredients=None, 
                        diet_restrictions=None, 
                        fitness_goal=None, 
                        unavailable_utensils=None, 
                        custom_prompt=pro_prompt 
                    )

                st.session_state.pro_recipe_suggestion = recipe_text_pro
                st.session_state.pro_recipe_title = "🎯 Tu Receta Pro Optimizada 🎯"


    if st.session_state.pro_recipe_suggestion:
        st.markdown("---")
        st.subheader(st.session_state.pro_recipe_title)
        if st.session_state.pro_recipe_suggestion.startswith("Error:"):
            st.error(st.session_state.pro_recipe_suggestion)
        else:
            st.markdown(st.session_state.pro_recipe_suggestion)



st.markdown("---")
st.markdown("💡 **Consejo:** Para la búsqueda normal, cuanto más específico seas con los ingredientes, mejores serán los resultados. ¡Prueba añadir especias o hierbas que tengas!")