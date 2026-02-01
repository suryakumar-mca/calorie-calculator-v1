from flask import Flask, render_template, request, session
from google import genai
from dotenv import load_dotenv
import json
import os


load_dotenv()
app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Needed for session management

# --- SETUP API ---
API_KEY = os.getenv("GEMINI_API_KEY")


def get_nutrition_from_ai(food_text):
    """Sends food text to Gemini and gets a JSON response."""
    prompt = f"""
    You are a nutritionist. Analyze: "{food_text}".
    The input may contain individual meals or meals consumed over the entire day. Treat them as a whole and calculate total consumption and not individually.
    Return a valid JSON object with these exact keys:
    - "item_name": Short summary of food
    - "calories": Integer (total calories)
    - "protein": Integer (grams)
    - "carbs": Integer (grams)
    - "fats": Integer (grams)
    
    Do not use Markdown. Just the raw JSON string.
    """
    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt,)
        print(f"----Printing Gemini's response---{response.text} ")

        # Clean the string just in case the AI adds ```json
        clean_text = response.text.replace(
            '```json', '').replace('```', '')  # type: ignore
        return json.loads(clean_text)
    except Exception as e:
        print(f"API Error: {e}")
        return None


def get_ideal_nutrition_from_ai(user_height, user_weight, user_gender, user_age, food_text):
    """Passing user details to Gemini and collect ideal consumption levels and feedback"""
    prompt = f"""
    System Instruction: You are an API endpoint. 
    Prompt: Act as a clinical nutritionist. I will provide a user's physical details and a description of a meal they just ate.

    User Details:
    Height: {user_height} cm
    Weight: {user_weight} kg
    Gender: {user_gender}
    Age: {user_age}
    Meal Description: "{food_text}"
    
    Your Task:
    Calculate the user's Daily Maintenance Calories (TDEE) using the Mifflin-St Jeor equation (assume Sedentary activity level x1.2).
    Based on this TDEE, calculate ideal daily macro targets (Standard split: 50% Carbs, 30% Protein, 20% Fat).
    Analyze the provided meal description. Provide feedback that is constructive and actionable.
    Generate 3 short specific positive observations about the meal.
    Generate 3 short specific areas for improvement (negatives) based on the meal's nutritional value.

    Guidelines for Feedback:
    Positives: Focus on nutrient density, good food choices, or hydration.
    Negatives: Don't just criticize. Suggest a specific swap or fix (e.g., "High in carbs" -> "Try swapping soda for sparkling water").
    Keep sentences short (under 12 words) to fit the UI cards.

    Output Format: Return ONLY a raw JSON object with no Markdown formatting. 
    JSON should contain 3 keys namely targets, positives and negatives
    targets is an object containing key value mappings of target calories, target protein, target fat and target carbs with the following exact key names: calories, protein, fat and carbs
    positives is an array containing the 3 short specific positive observations about the meal.
    negatives is an array containing 3 short specific areas for improvement (negatives) based on the meal's nutritional value.
    """
    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt,)
        print(f"----Printing Gemini's response---{response.text} ")

        # Clean the string just in case the AI adds ```json
        clean_text = response.text.replace(
            '```json', '').replace('```', '')  # type: ignore
        return json.loads(clean_text)
    except Exception as e:
        print(f"API Error: {e}")
        return None


def construct_formatted_data(food_data, analysed_data):
    analysed_data.update(consumed_data=food_data)
    return analysed_data


def calculate_difference_calories(food_data, analysed_data):
    if analysed_data['targets']['calories'] > food_data['calories']:
        difference_in_calories = analysed_data['targets']['calories'] - \
            food_data['calories']
        calories_status = "DEFICIT"
        difference_in_calories_str = "-" + str(difference_in_calories)

    elif analysed_data['targets']['calories'] == food_data['calories']:
        difference_in_calories = 0
        calories_status = "OPTIMAL"
        difference_in_calories_str = str(difference_in_calories)

    else:
        difference_in_calories = food_data['calories'] - \
            analysed_data['targets']['calories']
        calories_status = "SURPLUS"
        difference_in_calories_str = "+" + str(difference_in_calories)

    return calories_status, difference_in_calories_str


def calculate_difference_protein(food_data, analysed_data):
    if analysed_data['targets']['protein'] > food_data['protein']:
        difference_in_protein = analysed_data['targets']['protein'] - \
            food_data['protein']
        protein_status = "DEFICIT"
        difference_in_protein_str = "-" + str(difference_in_protein)

    elif analysed_data['targets']['protein'] == food_data['protein']:
        difference_in_protein = 0
        protein_status = "OPTIMAL"
        difference_in_protein_str = str(difference_in_protein)

    else:
        difference_in_protein = food_data['protein'] - \
            analysed_data['targets']['protein']
        protein_status = "SURPLUS"
        difference_in_protein_str = "+" + str(difference_in_protein)

    return protein_status, difference_in_protein_str


def calculate_difference_carbs(food_data, analysed_data):
    if analysed_data['targets']['carbs'] > food_data['carbs']:
        difference_in_carbs = analysed_data['targets']['carbs'] - \
            food_data['carbs']
        carbs_status = "DEFICIT"
        difference_in_carbs_str = "-" + str(difference_in_carbs)

    elif analysed_data['targets']['carbs'] == food_data['carbs']:
        difference_in_carbs = 0
        carbs_status = "OPTIMAL"
        difference_in_carbs_str = str(difference_in_carbs)

    else:
        difference_in_carbs = food_data['carbs'] - \
            analysed_data['targets']['carbs']
        carbs_status = "SURPLUS"
        difference_in_carbs_str = "+" + str(difference_in_carbs)

    return carbs_status, difference_in_carbs_str


def calculate_difference_fat(food_data, analysed_data):
    if analysed_data['targets']['fat'] > food_data['fats']:
        difference_in_fat = analysed_data['targets']['fat'] - \
            food_data['fats']
        fat_status = "DEFICIT"
        difference_in_fat_str = "-" + str(difference_in_fat)

    elif analysed_data['targets']['fat'] == food_data['fats']:
        difference_in_fat = 0
        fat_status = "OPTIMAL"
        difference_in_fat_str = str(difference_in_fat)

    else:
        difference_in_fat = food_data['fats'] - \
            analysed_data['targets']['fat']
        fat_status = "SURPLUS"
        difference_in_fat_str = "+" + str(difference_in_fat)

    return fat_status, difference_in_fat_str


def construct_verdict_data(food_data, analysed_data):
    difference_data = {}
    result = calculate_difference_calories(food_data, analysed_data)
    difference_data['status_calories'] = result[0]
    difference_data['difference_in_calories'] = result[1]

    protein_results = calculate_difference_protein(food_data, analysed_data)
    difference_data['status_protein'] = protein_results[0]
    difference_data['difference_in_protein'] = protein_results[1]

    carbs_results = calculate_difference_carbs(food_data, analysed_data)
    difference_data['status_carbs'] = carbs_results[0]
    difference_data['difference_in_carbs'] = carbs_results[1]

    fat_results = calculate_difference_fat(food_data, analysed_data)
    difference_data['status_fat'] = fat_results[0]
    difference_data['difference_in_fat'] = fat_results[1]
    print(difference_data)
    return difference_data


# --- ROUTES ---


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        food_input = request.form['food_text']

        # 1. Call the AI
        nutrition_data = get_nutrition_from_ai(food_input)

        if nutrition_data:
            # 2. Store data in session to pass to next page
            session['nutrition'] = nutrition_data
            # 3. Render the Dashboard immediately with the data
            return render_template('user_details.html', data=nutrition_data)
        else:
            return "Error parsing food data. Please try again."

    return render_template('index.html')


@app.route('/calculate_deficit', methods=['POST'])
def calculate_deficit():
    # 1. Get inputs from the form
    try:
        age = int(request.form['age'])
        gender = request.form['gender']
        height = int(request.form['height'])
        weight = int(request.form['weight'])
    except:
        return "Error: Please enter valid numbers."

    # 2. Get the food calories from the previous step (Session)
    if 'nutrition' not in session:
        return "Error: Session expired. Go back to home page."

    food_data = session['nutrition']

    analysed_data = get_ideal_nutrition_from_ai(
        height, weight, gender, age, food_data)

    if analysed_data:
        formatted_data = construct_formatted_data(food_data, analysed_data)

        verdict_data = construct_verdict_data(food_data, analysed_data)

        formatted_data.update(verdict_data=verdict_data)

        return render_template("verdict.html", data=formatted_data)

    else:
        return "Error parsing the data. Please return to home page"


if __name__ == '__main__':
    app.run(debug=True)
