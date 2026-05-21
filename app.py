import streamlit as st
import requests
from openai import OpenAI

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Smart Kitchen AI",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LM STUDIO CONNECTION
# ==========================================

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* =========================================
   GLOBAL
========================================= */

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f172a, #111827);
    color: white;
}

/* =========================================
   MAIN CONTAINER
========================================= */

.block-container {
    padding-top: 6rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* =========================================
   HERO SECTION
========================================= */

.hero-container {
    background: linear-gradient(135deg, #1e293b, #111827);
    padding: 40px;
    border-radius: 30px;
    border: 1px solid #334155;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.title {
    font-size: 60px;
    font-weight: 800;
    color: #facc15;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 20px;
    color: #cbd5e1;
}

/* =========================================
   SIDEBAR
========================================= */

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #374151;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* =========================================
   TEXT AREA
========================================= */

textarea {
    border-radius: 15px !important;
    background-color: #1e293b !important;
    color: white !important;
    border: 1px solid #334155 !important;
    padding: 15px !important;
}

/* =========================================
   SELECTBOX
========================================= */

.stSelectbox div[data-baseweb="select"] {
    background-color: #1e293b;
    border-radius: 12px;
}

/* =========================================
   BUTTONS
========================================= */

.stButton > button {
    width: 100%;
    height: 60px;
    border-radius: 15px;
    border: none;
    background: linear-gradient(135deg, #facc15, #eab308);
    color: black;
    font-size: 20px;
    font-weight: bold;
    transition: 0.3s ease;
    box-shadow: 0 5px 15px rgba(250,204,21,0.3);
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(250,204,21,0.5);
}

/* =========================================
   RECIPE CARD
========================================= */

.recipe-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    padding: 30px;
    border-radius: 25px;
    margin-bottom: 30px;
    border: 1px solid #334155;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    transition: 0.3s ease;
}

.recipe-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
}

/* =========================================
   IMAGE
========================================= */

img {
    border-radius: 20px;
}

/* =========================================
   ALERTS
========================================= */

.stAlert {
    border-radius: 15px;
}

/* =========================================
   SCROLLBAR
========================================= */

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #111827;
}

::-webkit-scrollbar-thumb {
    background: #475569;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #64748b;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero-container">
    <div class="title">🍳 Smart Kitchen AI</div>
    <div class="subtitle">
        AI-powered recipe recommendations using your available ingredients.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## ⚙️ Cooking Preferences")

    cooking_method = st.selectbox(
        "🍳 Cooking Method",
        [
            "Any",
            "Stove",
            "Air Fryer",
            "Microwave",
            "Barbecue",
            "Oven",
            "Deep Fry",
            "Slow Cooker",
            "No-Cook"
        ]
    )

    difficulty = st.selectbox(
        "🔥 Difficulty",
        [
            "Any",
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    cuisine = st.selectbox(
        "🌎 Preferred Cuisine",
        [
            "Any",
            "Filipino",
            "American",
            "Japanese",
            "Korean",
            "Chinese",
            "Italian",
            "Mexican",
            "Indian",
            "Thai"
        ]
    )

    servings = st.slider(
        "🍽️ Servings",
        1,
        10,
        2
    )

    st.divider()

    st.markdown("""
    ### 💡 Tips
    - Separate ingredients with commas
    - Use common ingredient names
    - Add spices and sauces for better results
    - Choose a cuisine for more accurate dishes
    """)

# ==========================================
# MAIN INPUT
# ==========================================

st.subheader("🥬 Available Ingredients")

ingredients = st.text_area(
    "",
    placeholder="Example: chicken, garlic, onion, soy sauce, rice, cheese, egg",
    height=180
)

# ==========================================
# SEARCH ONLINE RECIPES
# ==========================================

def search_mealdb(ingredients_list):

    all_meals = []

    for ingredient in ingredients_list:

        ingredient = ingredient.strip()

        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"

        try:

            response = requests.get(url)

            if response.status_code == 200:

                data = response.json()

                if data["meals"]:

                    for meal in data["meals"]:

                        if meal not in all_meals:
                            all_meals.append(meal)

        except:
            pass

    return all_meals[:10]

# ==========================================
# AI RECIPE GENERATOR
# ==========================================

def generate_recipe(recipe_name):

    if cuisine == "Filipino":

        extra_instruction = """
        Prioritize authentic Filipino dishes such as:
        Adobo, Sinigang, Tinola, Kare-Kare,
        Caldereta, Sisig, Menudo, Bicol Express,
        Pancit, Tapsilog, Bulalo, Ginataang dishes,
        and other local Filipino cuisine.
        """

    else:
        extra_instruction = ""

    prompt = f"""
    You are a professional chef AI.

    Create a complete and delicious recipe.

    IMPORTANT:
    Prioritize dishes from this cuisine:
    {cuisine}

    {extra_instruction}

    USER INGREDIENTS:
    {ingredients}

    COOKING METHOD:
    {cooking_method}

    DIFFICULTY:
    {difficulty}

    SERVINGS:
    {servings}

    RECIPE NAME:
    {recipe_name}

    FORMAT:

    Recipe Name

    Short Description

    Cooking Time

    Difficulty

    Ingredients

    Step-by-Step Instructions

    Cooking Tips

    Ingredient Alternatives
    """

    try:

        completion = client.chat.completions.create(
            model="llama-3.2-3b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert chef assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1200
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"❌ Error:\n\n{str(e)}"

# ==========================================
# FIND RECIPES BUTTON
# ==========================================

if st.button("🔍 Find Delicious Recipes"):

    if not ingredients.strip():

        st.warning("⚠️ Please enter some ingredients.")

    else:

        ingredient_list = ingredients.split(",")

        with st.spinner("🍲 Searching recipes and generating AI instructions..."):

            meals = search_mealdb(ingredient_list)

            # ==========================================
            # RECIPES FOUND
            # ==========================================

            if meals:

                st.success(f"✅ Found {len(meals)} recipe suggestions!")

                for meal in meals:

                    recipe_name = meal["strMeal"]
                    recipe_image = meal["strMealThumb"]

                    st.markdown(
                        '<div class="recipe-card">',
                        unsafe_allow_html=True
                    )

                    col1, col2 = st.columns([1, 2])

                    with col1:

                        st.image(
                            recipe_image,
                            use_container_width=True
                        )

                    with col2:

                        st.subheader(f"🍽️ {recipe_name}")

                        with st.spinner(f"🤖 Generating AI recipe for {recipe_name}..."):

                            recipe = generate_recipe(recipe_name)

                            st.markdown(recipe)

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

            # ==========================================
            # NO RECIPES FOUND
            # ==========================================

            else:

                st.warning(
                    "⚠️ No online recipes found. Creating a custom AI recipe..."
                )

                custom_recipe = generate_recipe("Custom AI Dish")

                st.markdown(
                    '<div class="recipe-card">',
                    unsafe_allow_html=True
                )

                st.subheader("🍽️ Custom AI Recipe")

                st.markdown(custom_recipe)

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )