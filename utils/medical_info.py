"""
Medical Information Helper Module
---------------------------------
Provides disease descriptions, medical precautions, categories, and report formatting.
"""

# Disease Precautions Dictionary
DISEASE_PRECAUTIONS = {
    'Drug Reaction': [
        'Stop taking the suspected medication immediately',
        'Consult a physician or allergist',
        'Monitor for signs of anaphylaxis (difficulty breathing, swelling)',
        'Maintain hydration and avoid self-medicating with unprescribed drugs'
    ],
    'Malaria': [
        'Consult a doctor for antimalarial medication immediately',
        'Use mosquito nets and repellents to prevent further bites',
        'Take adequate rest and consume plenty of fluids',
        'Avoid stagnant water around living areas'
    ],
    'Allergy': [
        'Identify and avoid known allergen triggers',
        'Use prescribed antihistamines as directed',
        'Keep living spaces clean and free of dust mites/pollen',
        'Seek immediate medical help if throat tightness occurs'
    ],
    'Hypothyroidism': [
        'Take regular thyroid hormone replacement (Levothyroxine) as prescribed',
        'Maintain a balanced diet rich in iodine and selenium',
        'Monitor thyroid levels (TSH, T3, T4) periodically',
        'Exercise regularly to combat fatigue and weight gain'
    ],
    'Psoriasis': [
        'Apply topical moisturizers and prescribed corticosteroid creams',
        'Avoid harsh soaps and hot showers that dry the skin',
        'Manage stress through mindfulness or light exercise',
        'Get controlled exposure to sunlight under medical guidance'
    ],
    'Gerd': [
        'Avoid spicy, fatty, and acidic foods',
        'Eat smaller, more frequent meals',
        'Do not lie down immediately after eating (wait 2-3 hours)',
        'Elevate the head of your bed during sleep'
    ],
    'Chronic Cholestasis': [
        'Follow a low-fat, high-vitamin diet (Vitamin A, D, E, K)',
        'Avoid alcohol and liver-toxic substances',
        'Consult a hepatologist for bile acid therapy',
        'Stay hydrated and monitor skin itching'
    ],
    'Peptic Ulcer Disease': [
        'Avoid NSAIDs (ibuprofen, aspirin) and stomach irritants',
        'Limit caffeine, alcohol, and spicy foods',
        'Take prescribed antacids or proton pump inhibitors (PPIs)',
        'Manage psychological stress'
    ],
    'Aids': [
        'Adhere strictly to prescribed Antiretroviral Therapy (ART)',
        'Practice safe hygiene and avoid exposure to opportunistic infections',
        'Maintain a nutritious diet and exercise regularly',
        'Schedule routine CD4 count and viral load monitoring'
    ],
    'Diabetes': [
        'Monitor blood glucose levels regularly',
        'Follow a low-glycemic, fiber-rich diet',
        'Engage in regular physical activity',
        'Take prescribed insulin or oral antidiabetic drugs consistently'
    ],
    'Gastroenteritis': [
        'Drink Oral Rehydration Solutions (ORS) to prevent dehydration',
        'Eat a soft BRAT diet (Bananas, Rice, Applesauce, Toast)',
        'Avoid dairy, fatty, and spicy foods',
        'Wash hands frequently to avoid spreading gastrointestinal infections'
    ],
    'Bronchial Asthma': [
        'Keep rescue inhalers accessible at all times',
        'Avoid cold air, smoke, pollen, and dust triggers',
        'Take long-term controller medications as prescribed',
        'Use a peak flow meter to monitor lung function'
    ],
    'Hypertension': [
        'Reduce sodium intake (< 2,000 mg/day)',
        'Exercise regularly (30 mins/day)',
        'Monitor blood pressure daily and record readings',
        'Avoid smoking and limit alcohol consumption'
    ],
    'Migraine': [
        'Rest in a quiet, dark room during an episode',
        'Apply cold compresses to the forehead or neck',
        'Identify and avoid personal trigger foods (aged cheese, caffeine)',
        'Stay well-hydrated and maintain consistent sleep schedules'
    ],
    'Cervical Spondylosis': [
        'Perform neck strengthening and stretching exercises',
        'Maintain proper ergonomic posture when working at computers',
        'Apply hot or cold therapy to soothe neck muscle spasms',
        'Use a supportive cervical pillow for sleeping'
    ],
    'Paralysis (Brain Hemorrhage)': [
        'Seek emergency medical stroke care immediately',
        'Undergo physical therapy and rehabilitation programs',
        'Control blood pressure strictly with medication',
        'Prevent bedsores through frequent repositioning'
    ],
    'Jaundice': [
        'Drink plenty of fluids and rest adequately',
        'Strictly avoid alcohol and liver-fatiguing foods',
        'Eat a high-carbohydrate, easily digestible diet',
        'Consult a doctor to evaluate underlying bilirubin causes'
    ],
    'Chicken Pox': [
        'Avoid scratching blisters to prevent bacterial skin infections',
        'Apply calamine lotion or cool oatmeal baths to relieve itching',
        'Take paracetamol for fever (avoid aspirin in children)',
        'Isolate to prevent spreading varicella virus to others'
    ],
    'Dengue': [
        'Ensure continuous fluid intake (ORS, coconut water, fluids)',
        'Monitor blood platelet count regularly',
        'Use paracetamol for fever and body pain (avoid NSAIDs/aspirin)',
        'Rest adequately and watch for warning signs of severe dengue'
    ],
    'Typhoid': [
        'Complete the full course of prescribed antibiotics',
        'Drink boiled or purified water only',
        'Eat bland, nutritious, well-cooked meals',
        'Wash hands thoroughly before eating and preparing food'
    ],
    'Hepatitis A': [
        'Get plenty of bed rest',
        'Eat small, high-calorie meals to combat nausea',
        'Avoid alcohol and medications processed by the liver',
        'Practice strict hand hygiene'
    ],
    'Hepatitis B': [
        'Consult a gastroenterologist/hepatologist for antiviral therapy',
        'Avoid alcohol and liver-damaging substances completely',
        'Eat a healthy, balanced diet low in saturated fats',
        'Ensure family members are vaccinated against Hepatitis B'
    ],
    'Hepatitis C': [
        'Take direct-acting antiviral (DAA) medications as directed',
        'Avoid alcohol and illicit drugs',
        'Maintain routine liver ultrasound and monitoring',
        'Eat a liver-healthy diet'
    ],
    'Hepatitis D': [
        'Follow hepatologist guidance for interferon therapy',
        'Avoid alcohol completely',
        'Prevent coinfection risks',
        'Rest and maintain proper nutritional intake'
    ],
    'Hepatitis E': [
        'Rest and stay hydrated',
        'Consume clean, boiled drinking water',
        'Avoid alcohol and heavy meals',
        'Seek medical monitoring if pregnant'
    ],
    'Alcoholic Hepatitis': [
        'Completely abstain from alcohol consumption',
        'Undergo nutritional therapy and vitamin supplementation',
        'Consult a liver specialist for anti-inflammatory treatment',
        'Participate in addiction recovery support programs'
    ],
    'Tuberculosis': [
        'Complete the full multi-month course of Directly Observed Therapy (DOTS)',
        'Wear a mask to prevent airborne transmission',
        'Ensure proper ventilation in living spaces',
        'Eat a high-protein, nutrient-dense diet'
    ],
    'Common Cold': [
        'Rest and stay well-hydrated with warm liquids',
        'Use saline nasal sprays or steam inhalation for congestion',
        'Gargle with warm salt water for throat irritation',
        'Wash hands frequently'
    ],
    'Pneumonia': [
        'Take prescribed antibiotics or antivirals completely',
        'Get plenty of bed rest and use a humidifier',
        'Stay hydrated to help thin lung secretions',
        'Seek urgent care if shortness of breath worsens'
    ],
    'Dimorphic Hemorrhoids (Piles)': [
        'Eat a high-fiber diet to ensure soft stools',
        'Drink at least 8-10 glasses of water daily',
        'Take warm sitz baths for 15 minutes twice daily',
        'Avoid prolonged sitting or straining during bowel movements'
    ],
    'Heart Attack': [
        'Call emergency medical services immediately (911 / 102)',
        'Chew an aspirin if recommended by emergency dispatch',
        'Undergo emergency cardiac catheterization/treatment',
        'Enroll in cardiac rehabilitation and strictly take blood thinners'
    ],
    'Varicose Veins': [
        'Elevate legs above heart level when resting',
        'Wear gradient compression stockings',
        'Avoid standing or sitting for prolonged unbroken periods',
        'Engage in regular walking exercise'
    ],
    'Hyperthyroidism': [
        'Take prescribed antithyroid medications (Methimazole/PTU)',
        'Avoid excessive iodine intake',
        'Monitor heart rate and blood pressure',
        'Manage stress and stay cool in hot environments'
    ],
    'Hypoglycemia': [
        'Follow the 15-15 rule: Consume 15g fast-acting carbohydrates (juice/candy)',
        'Recheck blood glucose after 15 minutes',
        'Carry emergency glucose tablets or gel at all times',
        'Eat regular, balanced meals to stabilize blood sugar'
    ],
    'Osteoarthristis': [
        'Engage in low-impact joint exercises (swimming, cycling)',
        'Maintain a healthy weight to reduce pressure on knees/hips',
        'Apply heat or ice packs to painful joints',
        'Use supportive footwear or joint braces'
    ],
    'Arthritis': [
        'Take prescribed anti-inflammatory drugs or DMARDs',
        'Perform gentle range-of-motion physical therapy exercises',
        'Apply warm compresses to stiff joints in the morning',
        'Eat an anti-inflammatory diet rich in Omega-3 fatty acids'
    ],
    '(Vertigo) Paroymsal Positional Vertigo': [
        'Perform Epley maneuver under physical therapy guidance',
        'Avoid sudden head movements or turning quickly',
        'Sit on the edge of the bed for a minute before standing up',
        'Sleep with head slightly elevated on pillows'
    ],
    'Acne': [
        'Wash face twice daily with a gentle non-comedogenic cleanser',
        'Avoid picking or squeezing acne lesions',
        'Apply prescribed topical benzoyl peroxide or retinoids',
        'Use oil-free moisturizers and sunscreen'
    ],
    'Urinary Tract Infection': [
        'Drink plenty of water to flush bacteria from the urinary tract',
        'Complete the full course of prescribed antibiotics',
        'Avoid caffeine, alcohol, and spicy foods that irritate the bladder',
        'Maintain proper personal hygiene'
    ],
    'Impetigo': [
        'Gently wash crusts with warm soapy water',
        'Apply prescribed topical antibiotic ointment',
        'Keep infected areas covered with clean gauze',
        'Wash clothes, towels, and bedsheets daily in hot water'
    ],
    'Fungal Infection': [
        'Keep the affected skin area clean and dry',
        'Apply prescribed topical antifungal creams regularly',
        'Avoid sharing personal items like towels or clothing',
        'Wear breathable cotton clothing'
    ]
}

# Fallback precautions for unspecified diseases
DEFAULT_PRECAUTIONS = [
    'Consult a qualified medical healthcare professional for diagnostic evaluation',
    'Follow all prescribed medication dosages and treatment schedules',
    'Maintain adequate hydration and rest',
    'Seek immediate medical care if severe symptoms develop'
]

def get_precautions(disease_name):
    """Retrieves medical precautions for a given disease name."""
    if not disease_name:
        return DEFAULT_PRECAUTIONS
    for k in DISEASE_PRECAUTIONS:
        if k.lower() == str(disease_name).strip().lower():
            return DISEASE_PRECAUTIONS[k]
    return DEFAULT_PRECAUTIONS

def generate_patient_report(patient_info, predicted_disease, confidence_score, top_symptoms, recommendations, precautions):
    """Generates a clean text/markdown patient summary report."""
    report = f"""
================================================================================
 PERSONALIZED HEALTHCARE & MEDICINE RECOMMENDATION SYSTEM - DIAGNOSTIC REPORT
================================================================================
Date & Time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

1. PATIENT DEMOGRAPHICS & CLINICAL BIOMARKERS
--------------------------------------------------------------------------------
Patient Name:        {patient_info.get('Name', 'Anonymous')}
Age:                 {patient_info.get('Age', 'N/A')} years
Gender:              {patient_info.get('Sex', 'N/A')}
Blood Pressure:      {patient_info.get('BP', 'N/A')}
Cholesterol Level:   {patient_info.get('Cholesterol', 'N/A')}
Na/K Ratio:          {patient_info.get('Na_to_K', 'N/A')}

2. ACTIVE PATIENT SYMPTOMS
--------------------------------------------------------------------------------
{', '.join(top_symptoms) if top_symptoms else 'None specified'}

3. AI DIAGNOSTIC MODEL PREDICTION
--------------------------------------------------------------------------------
Predicted Disease:   {predicted_disease}
Model Confidence:    {confidence_score:.1f}%

4. RECOMMENDED MEDICATIONS (CONTENT-BASED TF-IDF & SENTIMENT MATCHING)
--------------------------------------------------------------------------------
"""
    if not recommendations.empty:
        for idx, row in recommendations.iterrows():
            report += f"{idx+1}. {row['Drug_Name']} | Rating: {row['Average_Rating']}/10 | Useful Votes: {row['Useful_Review_Count']:,} | Match Score: {row['Recommendation_Score']}%\n"
    else:
        report += "No medication recommendations available.\n"

    report += """
5. MEDICAL PRECAUTIONS & HEALTHCARE ADVICE
--------------------------------------------------------------------------------
"""
    for idx, prec in enumerate(precautions, 1):
        report += f"{idx}. {prec}\n"

    report += """
================================================================================
 DISCLAIMER: This report is generated by an AI decision-support tool and does
 not replace professional medical diagnosis, advice, or treatment. Always
 consult a licensed healthcare professional before starting any medication.
================================================================================
"""
    return report
