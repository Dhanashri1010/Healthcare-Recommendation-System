"""
Health Risk Score Model Module
-------------------------------
Calculates overall health risk index (0-100%), risk breakdown across
Cardiovascular, Metabolic, and Lifestyle risk factors, identified risk drivers,
and clinical preventive interventions.
"""

def calculate_health_risk(data: dict):
    """
    Calculates health risk score based on patient profile and biomarkers.
    data fields:
      - age: int
      - sex: str ('Male' / 'Female')
      - bp: str ('HIGH' / 'NORMAL' / 'LOW')
      - cholesterol: str ('HIGH' / 'NORMAL')
      - na_to_k: float
      - bmi: float
      - smoking: bool
      - alcohol: bool
      - physical_activity: str ('Low' / 'Moderate' / 'High')
      - family_history: bool
      - symptoms: list[str]
    """
    age = data.get('age', 45)
    bp = str(data.get('bp', 'NORMAL')).upper()
    cholesterol = str(data.get('cholesterol', 'NORMAL')).upper()
    na_to_k = float(data.get('na_to_k', 14.0))
    bmi = float(data.get('bmi', 24.5))
    smoking = bool(data.get('smoking', False))
    alcohol = bool(data.get('alcohol', False))
    activity = str(data.get('physical_activity', 'Moderate')).lower()
    family_history = bool(data.get('family_history', False))
    symptoms = data.get('symptoms', [])

    # Sub-score points initialization
    cardio_pts = 0
    metabolic_pts = 0
    lifestyle_pts = 0
    identified_risk_factors = []

    # 1. Cardiovascular Risk Points (Max 35)
    if bp == 'HIGH':
        cardio_pts += 15
        identified_risk_factors.append("Hypertension (High BP)")
    elif bp == 'LOW':
        cardio_pts += 5

    if cholesterol == 'HIGH':
        cardio_pts += 12
        identified_risk_factors.append("Hypercholesterolemia (High Cholesterol)")

    if age >= 55:
        cardio_pts += 8
        identified_risk_factors.append("Advanced Age (≥ 55 yrs)")
    elif age >= 45:
        cardio_pts += 5

    # 2. Metabolic Risk Points (Max 35)
    if bmi >= 30.0:
        metabolic_pts += 18
        identified_risk_factors.append("Clinical Obesity (BMI ≥ 30)")
    elif bmi >= 25.0:
        metabolic_pts += 10
        identified_risk_factors.append("Overweight Status (BMI 25-29.9)")

    if na_to_k > 15.0:
        metabolic_pts += 12
        identified_risk_factors.append("Elevated Sodium-to-Potassium Ratio (> 15.0)")

    if family_history:
        metabolic_pts += 5
        identified_risk_factors.append("Family History of Chronic Illness")

    # 3. Lifestyle & Symptomatic Risk Points (Max 30)
    if smoking:
        lifestyle_pts += 12
        identified_risk_factors.append("Active Tobacco Smoking")

    if alcohol:
        lifestyle_pts += 6
        identified_risk_factors.append("Frequent Alcohol Intake")

    if activity == 'low':
        lifestyle_pts += 8
        identified_risk_factors.append("Sedentary Physical Activity")

    symptom_count = len(symptoms)
    if symptom_count >= 5:
        lifestyle_pts += 10
        identified_risk_factors.append(f"Multiple Active Symptoms ({symptom_count} reported)")
    elif symptom_count >= 2:
        lifestyle_pts += 5

    # Aggregated Score out of 100
    total_score = min(cardio_pts + metabolic_pts + lifestyle_pts, 100)

    # Risk Classification
    if total_score <= 25:
        risk_level = "Low"
        risk_color = "#10B981"  # Emerald
        summary = "Your biomarkers indicate low overall health risk. Maintain standard healthy lifestyle practices."
    elif total_score <= 50:
        risk_level = "Moderate"
        risk_color = "#F59E0B"  # Amber
        summary = "Moderate risk detected. Preventive modifications in diet, exercise, and routine monitoring are advised."
    elif total_score <= 75:
        risk_level = "High"
        risk_color = "#EF4444"  # Red
        summary = "High health risk detected. Early clinical consultation and lifestyle targeted intervention are strongly recommended."
    else:
        risk_level = "Critical"
        risk_color = "#991B1B"  # Dark Red
        summary = "Critical health risk level. Immediate medical evaluation and active clinical management required."

    # Interventions
    interventions = []
    if bp == 'HIGH':
        interventions.append("Restrict dietary sodium to < 2,000 mg/day and monitor blood pressure weekly.")
    if cholesterol == 'HIGH':
        interventions.append("Reduce saturated fats and schedule a lipid panel check with your physician.")
    if bmi >= 25.0:
        interventions.append("Target 5-10% body weight reduction through caloric deficit and daily aerobic exercise.")
    if smoking:
        interventions.append("Enroll in a tobacco cessation program to mitigate vascular and respiratory risks.")
    if activity == 'low':
        interventions.append("Incorporate 150 minutes of moderate aerobic exercise per week.")
    if not interventions:
        interventions.append("Continue regular annual checkups and balanced Mediterranean-style nutrition.")

    return {
        "overall_risk_score": total_score,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "summary": summary,
        "cardiovascular_risk_percent": min(round((cardio_pts / 35.0) * 100, 1), 100.0),
        "metabolic_risk_percent": min(round((metabolic_pts / 35.0) * 100, 1), 100.0),
        "lifestyle_risk_percent": min(round((lifestyle_pts / 30.0) * 100, 1), 100.0),
        "identified_risk_factors": identified_risk_factors,
        "preventive_interventions": interventions
    }
