"""
BMI Calculator & Metabolic Assessment Module
"""

def calculate_bmi(weight_kg: float, height_cm: float):
    """
    Calculates Body Mass Index (BMI), category, ideal weight range,
    weight difference to target ideal BMI (22.0), and BMR calorie estimate.
    """
    if height_cm <= 0 or weight_kg <= 0:
        return {
            "error": "Height and weight must be positive numbers."
        }
    
    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m ** 2), 1)

    if bmi < 18.5:
        category = "Underweight"
        category_color = "#3B82F6"  # Blue
        risk_note = "Increased risk of nutritional deficiency and osteoporosis."
    elif 18.5 <= bmi <= 24.9:
        category = "Normal weight"
        category_color = "#10B981"  # Emerald / Green
        risk_note = "Lowest risk of metabolic and cardiovascular diseases."
    elif 25.0 <= bmi <= 29.9:
        category = "Overweight"
        category_color = "#F59E0B"  # Amber / Yellow
        risk_note = "Moderate risk of hypertension, type 2 diabetes, and CVD."
    elif 30.0 <= bmi <= 34.9:
        category = "Obese (Class I)"
        category_color = "#EF4444"  # Red
        risk_note = "High risk of metabolic syndrome and osteoarthritis."
    elif 35.0 <= bmi <= 39.9:
        category = "Obese (Class II)"
        category_color = "#DC2626"  # Dark Red
        risk_note = "Very high risk of severe health complications."
    else:
        category = "Obese (Class III)"
        category_color = "#991B1B"  # Extreme Red
        risk_note = "Extremely high risk of cardiovascular failure and reduced life expectancy."

    # Healthy Weight Range for height (BMI 18.5 to 24.9)
    min_healthy_weight = round(18.5 * (height_m ** 2), 1)
    max_healthy_weight = round(24.9 * (height_m ** 2), 1)
    ideal_weight = round(22.0 * (height_m ** 2), 1)
    weight_diff = round(weight_kg - ideal_weight, 1)

    # Estimate BMR (Mifflin-St Jeor equation assuming average adult)
    # Defaulting age=30, male/female average factor
    bmr_kcal = round(10 * weight_kg + 6.25 * height_cm - 5 * 30 + 5)

    return {
        "bmi": bmi,
        "category": category,
        "category_color": category_color,
        "risk_note": risk_note,
        "min_healthy_weight_kg": min_healthy_weight,
        "max_healthy_weight_kg": max_healthy_weight,
        "ideal_weight_kg": ideal_weight,
        "weight_difference_kg": weight_diff,
        "estimated_bmr_kcal": bmr_kcal,
        "height_cm": height_cm,
        "weight_kg": weight_kg
    }
