"""
Lifestyle Recommendation Model Module
--------------------------------------
Generates personalized nutrition, physical activity, sleep & stress management,
and habit modification recommendations based on patient BMI, health risk score,
disease condition, and lifestyle habits.
"""

def generate_lifestyle_recommendation(data: dict):
    """
    Generates personalized lifestyle recommendation plan.
    Input data fields:
      - bmi: float
      - risk_level: str
      - disease: str
      - activity_level: str ('Low', 'Moderate', 'High')
      - dietary_pref: str ('Balanced', 'Vegetarian', 'Vegan', 'Keto', 'Low Carb')
      - sleep_hours: float
      - stress_level: str ('Low', 'Moderate', 'High')
    """
    bmi = float(data.get('bmi', 24.5))
    risk_level = str(data.get('risk_level', 'Low'))
    disease = str(data.get('disease', 'General Wellness'))
    activity = str(data.get('activity_level', 'Moderate')).lower()
    diet_pref = str(data.get('dietary_pref', 'Balanced'))
    sleep_hrs = float(data.get('sleep_hours', 7.5))
    stress = str(data.get('stress_level', 'Moderate')).lower()

    # 1. Nutrition & Meal Plan
    if bmi >= 30.0:
        cal_strategy = "Mild Caloric Deficit (500 kcal reduction/day target)"
        macro_split = "40% Protein, 35% Complex Carbs, 25% Healthy Fats"
    elif bmi >= 25.0:
        cal_strategy = "Controlled Energy Balance (250-300 kcal deficit)"
        macro_split = "35% Protein, 40% Complex Carbs, 25% Healthy Fats"
    elif bmi < 18.5:
        cal_strategy = "Caloric Surplus (300-500 kcal increase/day with nutrient-dense foods)"
        macro_split = "25% Protein, 50% Complex Carbs, 25% Healthy Fats"
    else:
        cal_strategy = "Eucaloric Maintenance (Balanced Energy Intake)"
        macro_split = "30% Protein, 45% Complex Carbs, 25% Healthy Fats"

    recommended_foods = [
        "Leafy Greens & Cruciferous Veggies (Spinach, Kale, Broccoli)",
        "Lean Protein Sources (Chicken Breast, Salmon, Tofu, Legumes)",
        "Whole Grains (Quinoa, Brown Rice, Oats)",
        "Healthy Fats (Avocado, Extra Virgin Olive Oil, Almonds, Walnuts)"
    ]

    foods_to_avoid = [
        "Refined Sugars & Sugary Beverages (Soda, Processed Juices)",
        "Ultra-Processed Foods & Trans-Fats (Fried Foods, Packaged Snacks)",
        "Excessive Dietary Sodium (> 2,300 mg/day)",
        "Refined Carbohydrates (White Bread, Pastries)"
    ]

    # Adjust for specific disease conditions
    if "Hypertension" in disease or "High BP" in disease:
        recommended_foods.append("Potassium-Rich Foods (Bananas, Sweet Potatoes, Beans)")
        foods_to_avoid.append("High-Sodium Canned Soups, Pickles, Cured Meats")
    elif "Diabetes" in disease:
        recommended_foods.append("High-Fiber Legumes & Low-GI Fruits (Berries, Apples)")
        foods_to_avoid.append("High-Glycemic Foods, White Rice, Candy")

    # 2. Fitness & Physical Activity Plan
    if activity == 'low':
        exercise_frequency = "3 to 4 days per week"
        aerobic_target = "20-30 minutes of low-impact cardio (brisk walking, stationary cycling)"
        step_goal = "7,000 to 8,000 steps daily"
    elif activity == 'high':
        exercise_frequency = "5 to 6 days per week"
        aerobic_target = "45-60 minutes of moderate-to-vigorous cardio + HIIT sessions"
        step_goal = "10,000 to 12,000 steps daily"
    else:
        exercise_frequency = "4 to 5 days per week"
        aerobic_target = "30-45 minutes of moderate aerobic exercise"
        step_goal = "8,500 to 10,000 steps daily"

    strength_target = "2 sessions/week focusing on major muscle groups (squats, push-ups, bodyweight exercises)"

    # 3. Sleep & Stress Management
    if sleep_hrs < 7.0:
        sleep_recommendation = f"You are currently sleeping {sleep_hrs} hours. Aim for 7 to 8.5 hours of quality restorative sleep by setting a consistent bedtime schedule and eliminating screens 45 mins before sleep."
    else:
        sleep_recommendation = f"Your average sleep duration of {sleep_hrs} hours is in the optimal range. Continue maintaining sleep hygiene."

    if stress == 'high':
        stress_recommendation = "High stress levels detected. Practice 15 minutes of mindfulness meditation or box-breathing exercises daily. Consider yoga or nature walks."
    else:
        stress_recommendation = "Incorporate 10-15 minutes of daily relaxation routines (guided breathing, stretching) to keep cortisol levels balanced."

    # 4. Habit Modifications
    habits = [
        "Hydration Target: Drink 2.5 - 3.5 Liters of water daily.",
        "Routine Medical Checkups: Schedule bi-annual comprehensive blood work and vital screening.",
        "Mindful Eating: Avoid eating in front of screens; chew slowly to aid digestion."
    ]
    if risk_level in ['High', 'Critical']:
        habits.append("Continuous Vital Monitoring: Check blood pressure and heart rate 3 times weekly.")

    return {
        "nutrition": {
            "caloric_strategy": cal_strategy,
            "macronutrient_split": macro_split,
            "hydration_goal_liters": 3.0,
            "dietary_preference": diet_pref,
            "recommended_foods": recommended_foods,
            "foods_to_avoid": foods_to_avoid
        },
        "fitness": {
            "weekly_frequency": exercise_frequency,
            "aerobic_routine": aerobic_target,
            "strength_routine": strength_target,
            "daily_step_goal": step_goal
        },
        "recovery": {
            "sleep_recommendation": sleep_recommendation,
            "stress_recommendation": stress_recommendation
        },
        "habit_modifications": habits
    }
