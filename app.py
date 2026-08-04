"""
Personalized Healthcare & Medicine Recommendation System
--------------------------------------------------------
Single-file Streamlit SaaS Web Application
"""

import os
import pickle
import pandas as pd
import numpy as np
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Personalized Healthcare & Medicine Recommendation System",
    page_icon="🩺",
    layout="wide"
)

# 2. Inject CSS Theme Block AT VERY TOP before any UI render
from theme import apply_theme
apply_theme()

# Explicitly import MedicineRecommender to prevent pickle deserialization errors
from recommend_medicine import MedicineRecommender

# Custom Helper Modules
from components.sidebar import render_sidebar
from components.kpi_cards import render_dashboard_kpis, render_custom_kpis, render_kpi_box

from utils.model_loader import load_disease_model, load_recommender, load_sentiment_classifier
from utils.medical_info import get_precautions

from charts.plotly_charts import (
    render_chart_panel,
    create_sentiment_donut,
    create_top_prescribed_bar,
    create_top_reviewed_bar,
    create_rating_histogram,
    create_powerbi_disease_chart,
    create_powerbi_medicine_chart,
    create_powerbi_patient_chart,
    create_powerbi_review_chart,
    create_powerbi_rec_chart
)

# 3. Render Sidebar Navigation & Theme Switcher
selected_page = render_sidebar()

# 4. Authentication gate
if not st.session_state.get("authenticated", False):
    from components.auth import render_auth_page
    render_auth_page()
    st.stop()


# ==============================================================================
# PAGE 1: 🏠 DASHBOARD
# ==============================================================================
if selected_page == "🏠 Dashboard":
    st.markdown("<h2 style='margin-bottom: 4px;'>🏠 Executive Healthcare Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Overview of diagnostic model accuracy, patient feedback, and indexed prescription profiles.</p>", unsafe_allow_html=True)

    # 6 KPI Cards (2 rows of 3)
    render_dashboard_kpis()

    # Section Spacer
    st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

    # 2 Charts Side-by-Side wrapped in Card Panels with Subtitles
    col1, col2 = st.columns(2)
    with col1:
        render_chart_panel(
            create_sentiment_donut(), 
            "Patient Sentiment Classification Split", 
            "Breakdown of patient feedback sentiment across all 161,297 reviews", 
            "🍩"
        )
    with col2:
        render_chart_panel(
            create_top_prescribed_bar(), 
            "Top 5 Most Prescribed Medications", 
            "Medications ranked by total patient prescription volume in dataset", 
            "📊"
        )

    # Section Spacer
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # Supporting Detail in Expander
    with st.expander("ℹ️ System Architecture & Pipeline Overview"):
        st.markdown("""
        - **Data Preprocessing**: Stripped scraper HTML tags, unescaped entities, and capped numerical outliers via IQR.
        - **Exploratory Data Analysis**: Analyzed 161,297 reviews across 8,423 drug profiles and 41 disease classes.
        - **Machine Learning Models**: Trained Logistic Regression ($100.0\%$ accuracy), Random Forest ($100.0\%$), XGBoost ($88.5\%$), and Decision Tree ($63.9\%$).
        - **Recommendation Engine**: TF-IDF Vectorization ($5,000$ n-gram features) + Cosine Similarity hybrid scoring.
        - **Sentiment Analysis**: NLTK tokenization + TF-IDF Logistic Regression classifier ($77.31\%$ test accuracy).
        """)


# ==============================================================================
# PAGE 2: 🩺 DISEASE PREDICTION
# ==============================================================================
elif selected_page == "🩺 Disease Prediction":
    st.markdown("<h2 style='margin-bottom: 4px;'>🩺 AI Disease Prediction Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Select patient active symptoms to execute multi-class disease diagnosis.</p>", unsafe_allow_html=True)

    disease_model, label_encoder, symptom_features = load_disease_model()

    # Searchable Multi-select Symptom Input (132 symptoms)
    symptom_display_map = {s: s.replace('_', ' ').title() for s in symptom_features}
    display_to_raw = {v: k for k, v in symptom_display_map.items()}

    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    selected_symptoms_labels = st.multiselect(
        "Search and Select Active Symptoms (132 Available):",
        options=sorted(list(symptom_display_map.values())),
        default=["Fatigue", "High Fever", "Vomiting"]
    )

    predict_clicked = st.button("🚀 Predict Disease Diagnosis")
    st.markdown("</div>", unsafe_allow_html=True)

    if predict_clicked:
        if not selected_symptoms_labels:
            st.warning("⚠️ Please select at least one symptom.")
        else:
            selected_raw = [display_to_raw[l] for l in selected_symptoms_labels]
            input_vector = [1 if s in selected_raw else 0 for s in symptom_features]

            pred_code = disease_model.predict([input_vector])[0]
            pred_disease = label_encoder['label_to_disease'][pred_code]

            if hasattr(disease_model, 'predict_proba'):
                probs = disease_model.predict_proba([input_vector])[0]
                conf_score = round(float(max(probs)) * 100, 1)
            else:
                conf_score = 100.0

            # Retrieve recommended medicines for this disease from the recommender engine
            try:
                recommender = load_recommender()
                rec_res = recommender.recommend(pred_disease, top_n=5)
                top_df = rec_res['Top_5_Recommendations']
                med_names = ", ".join(top_df['Drug_Name'].tolist())
            except Exception:
                med_names = "None"

            # Log prediction to SQLite
            from utils.db_manager import save_prediction
            symptoms_str = ", ".join(selected_symptoms_labels)
            save_prediction(
                username=st.session_state.get("username", "Guest"),
                symptoms=symptoms_str,
                disease=pred_disease,
                medicines=med_names,
                confidence=conf_score
            )

            st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

            # Result Card
            st.markdown(f"""
            <div class="saas-card" style="border-left: 5px solid var(--accent-primary);">
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--accent-primary); text-transform: uppercase; letter-spacing: 0.08em;">
                    AI Diagnostic Prediction Result
                </span>
                <h2 style="font-size: 1.8rem; margin: 6px 0 8px 0; color: var(--text-primary);">{pred_disease}</h2>
                <span style="background: rgba(99, 102, 241, 0.15); color: var(--accent-primary); border: 1px solid var(--accent-primary); padding: 4px 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 700;">
                    Model Confidence: {conf_score}%
                </span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

            # Supporting Guidance in 3 Tabs
            tab1, tab2, tab3 = st.tabs(["🛡️ Precautions", "🥗 Healthy Diet Tips", "🏃 Exercise Guidance"])
            
            with tab1:
                st.markdown("#### Medical Precautions")
                precs = get_precautions(pred_disease)
                for p in precs:
                    st.markdown(f"- {p}")

            with tab2:
                st.markdown("#### Dietary Recommendations")
                st.markdown("- Maintain a balanced diet rich in whole grains, fresh vegetables, and lean proteins.")
                st.markdown("- Hydrate adequately with 2.5 to 3 liters of water daily.")
                st.markdown("- Reduce sodium, refined sugars, and ultra-processed food intake.")

            with tab3:
                st.markdown("#### Physical Activity Guidance")
                st.markdown("- Engage in 30 minutes of moderate aerobic exercise 5 days per week.")
                st.markdown("- Incorporate light resistance training or yoga twice weekly.")
                st.markdown("- Ensure 7 to 8 hours of restful sleep for recovery.")


# ==============================================================================
# PAGE 3: ⚖️ BMI CALCULATOR
# ==============================================================================
elif selected_page == "⚖️ BMI Calculator":
    st.markdown("<h2 style='margin-bottom: 4px; color: var(--text-primary);'>⚖️ BMI & Metabolic Assessment Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Calculate Body Mass Index (BMI), healthy weight bounds, and BMR caloric requirements.</p>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        col_w, col_h = st.columns(2)
        with col_w:
            weight_kg = st.number_input("Body Weight (kg):", min_value=10.0, max_value=300.0, value=75.0, step=0.5)
        with col_h:
            height_cm = st.number_input("Height (cm):", min_value=50.0, max_value=250.0, value=175.0, step=0.5)
        st.markdown("</div>", unsafe_allow_html=True)

    from utils.bmi import calculate_bmi
    bmi_res = calculate_bmi(weight_kg, height_cm)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi_box("CALCULATED BMI", f"{bmi_res['bmi']}", f"Category: {bmi_res['category']}"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_box("HEALTHY WEIGHT RANGE", f"{bmi_res['min_healthy_weight_kg']} - {bmi_res['max_healthy_weight_kg']} kg", "BMI 18.5 to 24.9"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_box("IDEAL WEIGHT TARGET", f"{bmi_res['ideal_weight_kg']} kg", f"Difference: {bmi_res['weight_difference_kg']:+} kg"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_kpi_box("ESTIMATED BMR", f"{bmi_res['estimated_bmr_kcal']} kcal", "Mifflin-St Jeor Formula"), unsafe_allow_html=True)

    st.markdown(f"""
    <div class="saas-card" style="margin-top: 20px; border-left: 6px solid {bmi_res['category_color']};">
        <h4 style="margin:0; color: var(--text-primary);">Classification: <strong style="color: {bmi_res['category_color']};">{bmi_res['category']}</strong></h4>
        <p style="margin-top: 6px; color: var(--text-secondary);">{bmi_res['risk_note']}</p>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# PAGE 4: 🛡️ HEALTH RISK SCORE
# ==============================================================================
elif selected_page == "🛡️ Health Risk Score":
    st.markdown("<h2 style='margin-bottom: 4px; color: var(--text-primary);'>🛡️ Comprehensive Health Risk Assessment</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Evaluate multi-factorial clinical risk index based on vitals, demographics, and lifestyle factors.</p>", unsafe_allow_html=True)

    with st.form("health_risk_form"):
        st.markdown("<h4 style='color: var(--text-primary);'>Patient Clinical Parameters</h4>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            age_in = st.number_input("Age (Years)", min_value=1, max_value=120, value=45)
            sex_in = st.selectbox("Gender", ["Male", "Female"])
            bp_in = st.selectbox("Blood Pressure Level", ["HIGH", "NORMAL", "LOW"])
        with c2:
            chol_in = st.selectbox("Cholesterol Level", ["HIGH", "NORMAL"])
            nak_in = st.number_input("Na to K Ratio", min_value=1.0, max_value=50.0, value=14.5)
            bmi_in = st.number_input("Body Mass Index (BMI)", min_value=10.0, max_value=60.0, value=26.5)
        with c3:
            smoke_in = st.checkbox("Active Tobacco Smoking")
            alcohol_in = st.checkbox("Frequent Alcohol Consumption")
            activity_in = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
            family_in = st.checkbox("Family History of Chronic Disease")

        submit_risk = st.form_submit_button("🛡️ Compute Health Risk Score")

    from utils.health_risk import calculate_health_risk
    risk_res = calculate_health_risk({
        'age': age_in, 'sex': sex_in, 'bp': bp_in, 'cholesterol': chol_in,
        'na_to_k': nak_in, 'bmi': bmi_in, 'smoking': smoke_in, 'alcohol': alcohol_in,
        'physical_activity': activity_in, 'family_history': family_in
    })

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="saas-card" style="border-left: 6px solid {risk_res['risk_color']};">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:0.75rem; font-weight:700; text-transform:uppercase; color:var(--text-secondary);">Overall Health Risk Index</span>
                <h2 style="font-size: 2.2rem; font-weight: 800; margin: 4px 0; color: var(--text-primary);">{risk_res['overall_risk_score']} / 100</h2>
                <p style="color: var(--text-secondary); margin:0;">{risk_res['summary']}</p>
            </div>
            <div style="text-align:right;">
                <span style="background:{risk_res['risk_color']}20; color:{risk_res['risk_color']}; border:1px solid {risk_res['risk_color']}; padding:6px 16px; border-radius:20px; font-weight:800; font-size:1.1rem;">
                    {risk_res['risk_level']} Risk
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(render_kpi_box("CARDIOVASCULAR RISK", f"{risk_res['cardiovascular_risk_percent']}%", "Hypertension & Lipid Sub-Score"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_box("METABOLIC RISK", f"{risk_res['metabolic_risk_percent']}%", "Obesity & Na/K Sub-Score"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_box("LIFESTYLE RISK", f"{risk_res['lifestyle_risk_percent']}%", "Smoking & Activity Sub-Score"), unsafe_allow_html=True)

    if risk_res['identified_risk_factors']:
        st.markdown("<h4 style='color: var(--text-primary); margin-top: 20px;'>⚠️ Identified Risk Drivers</h4>", unsafe_allow_html=True)
        for rf in risk_res['identified_risk_factors']:
            st.markdown(f"- **{rf}**")

    if risk_res['preventive_interventions']:
        st.markdown("<h4 style='color: var(--text-primary); margin-top: 16px;'>🩺 Recommended Clinical Interventions</h4>", unsafe_allow_html=True)
        for iv in risk_res['preventive_interventions']:
            st.markdown(f"- {iv}")


# ==============================================================================
# PAGE 5: 🌿 LIFESTYLE RECOMMENDATION
# ==============================================================================
elif selected_page == "🌿 Lifestyle Recommendation":
    st.markdown("<h2 style='margin-bottom: 4px; color: var(--text-primary);'>🌿 Personalized Lifestyle & Wellness Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Tailored daily nutrition, fitness routine, sleep hygiene, and stress management.</p>", unsafe_allow_html=True)

    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        bmi_in = st.number_input("Your BMI Value", min_value=12.0, max_value=50.0, value=25.5)
        diet_pref = st.selectbox("Dietary Preference", ["Balanced", "Vegetarian", "Vegan", "Keto", "Low Carb"])
    with c2:
        act_in = st.selectbox("Current Activity Level", ["Low", "Moderate", "High"])
        sleep_in = st.number_input("Average Daily Sleep (Hours)", min_value=3.0, max_value=12.0, value=6.5)
    with c3:
        stress_in = st.selectbox("Perceived Stress Level", ["Low", "Moderate", "High"])
        disease_in = st.text_input("Existing Health Condition", value="Hypertension")
    st.markdown("</div>", unsafe_allow_html=True)

    from utils.lifestyle import generate_lifestyle_recommendation
    plan = generate_lifestyle_recommendation({
        'bmi': bmi_in, 'risk_level': 'Moderate', 'disease': disease_in,
        'activity_level': act_in, 'dietary_pref': diet_pref,
        'sleep_hours': sleep_in, 'stress_level': stress_in
    })

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["🥗 Nutrition & Diet Plan", "🏋️ Physical Activity Routine", "🧘 Sleep & Stress Recovery", "📋 Daily Health Habits"])

    with t1:
        st.markdown(f"#### Caloric Strategy: **{plan['nutrition']['caloric_strategy']}**")
        st.markdown(f"#### Macronutrient Target: **{plan['nutrition']['macronutrient_split']}**")
        st.markdown(f"#### Hydration Target: **{plan['nutrition']['hydration_goal_liters']} Liters/Day**")
        col_good, col_bad = st.columns(2)
        with col_good:
            st.markdown("##### ✅ Recommended Foods")
            for f in plan['nutrition']['recommended_foods']:
                st.markdown(f"- {f}")
        with col_bad:
            st.markdown("##### ❌ Foods to Avoid / Limit")
            for f in plan['nutrition']['foods_to_avoid']:
                st.markdown(f"- {f}")

    with t2:
        st.markdown(f"#### Weekly Training Frequency: **{plan['fitness']['weekly_frequency']}**")
        st.markdown(f"#### Daily Step Goal: **{plan['fitness']['daily_step_goal']}**")
        st.markdown(f"- **Aerobic Cardio Routine**: {plan['fitness']['aerobic_routine']}")
        st.markdown(f"- **Strength & Conditioning**: {plan['fitness']['strength_routine']}")

    with t3:
        st.markdown("#### 💤 Sleep Optimization")
        st.markdown(f"- {plan['recovery']['sleep_recommendation']}")
        st.markdown("#### 🧠 Stress Management")
        st.markdown(f"- {plan['recovery']['stress_recommendation']}")

    with t4:
        st.markdown("#### 📋 Core Daily Habit Modifications")
        for h in plan['habit_modifications']:
            st.markdown(f"- {h}")


# ==============================================================================
# PAGE 6: 💊 MEDICINE RECOMMENDATION
# ==============================================================================
elif selected_page == "💊 Medicine Recommendation":
    st.markdown("<h2 style='margin-bottom: 4px;'>💊 Content-Based Medicine Recommendation Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Search medications using TF-IDF text vectorization and hybrid rating scores.</p>", unsafe_allow_html=True)

    recommender = load_recommender()

    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    disease_query = st.text_input("Enter Medical Condition or Drug Name:", value="Acne")
    search_clicked = st.button("🔍 Search Recommended Medicines")
    st.markdown("</div>", unsafe_allow_html=True)

    if search_clicked or disease_query:
        res = recommender.recommend(disease_query, top_n=5)
        top_df = res['Top_5_Recommendations']
        alt_df = res['Alternative_Medicines']

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        st.markdown(f"### Top 5 Recommended Medicines for **{disease_query}**")
        
        # Display Top 5 as Clean Cards
        for idx, row in top_df.iterrows():
            cnt_val = row.get('Useful_Review_Count')
            if pd.notnull(cnt_val) and cnt_val:
                try:
                    cnt_str = f"{int(cnt_val):,}"
                except (ValueError, TypeError):
                    cnt_str = str(cnt_val)
            else:
                cnt_str = "N/A"

            st.markdown(f"""
            <div class="saas-card" style="border-left: 4px solid var(--accent-success); margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 1.1rem; color: var(--text-primary);">{idx+1}. {row['Drug_Name']}</strong>
                        <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px;">
                            ⭐ Avg Rating: <strong>{row['Average_Rating']} / 10</strong> &nbsp;|&nbsp; 
                            👍 Useful Count: <strong>{cnt_str}</strong> &nbsp;|&nbsp; 
                            💬 Reviews: <strong>{row['Total_Reviews']}</strong>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.3rem; font-weight: 800; color: var(--accent-primary);">{row['Recommendation_Score']}%</span>
                        <div style="font-size: 0.7rem; color: var(--text-secondary);">Match Score</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        # Alternative Medications in Collapsible Expander
        with st.expander("🔄 Alternative Medications"):
            st.dataframe(alt_df, use_container_width=True)


# ==============================================================================
# PAGE 4: 📊 DRUG REVIEW ANALYSIS
# ==============================================================================
elif selected_page == "📊 Drug Review Analysis":
    st.markdown("<h2 style='margin-bottom: 4px;'>📊 Drug Review Analysis & Feedback Metrics</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Explore prescription volume metrics and rating distribution across patient reviews.</p>", unsafe_allow_html=True)

    # KPI Row (3 cards)
    review_kpis = [
        {"title": "TOTAL REVIEWS", "value": "161,297", "sub": "Patient Feedback Entries"},
        {"title": "UNIQUE MEDICINES", "value": "8,423", "sub": "Indexed Drug Profiles"},
        {"title": "UNIQUE CONDITIONS", "value": "800+", "sub": "Clinical Indications"}
    ]
    render_custom_kpis(review_kpis)

    st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

    # 2 Charts Side-by-Side in Card Panels
    col1, col2 = st.columns(2)
    with col1:
        render_chart_panel(
            create_top_reviewed_bar(), 
            "Top Prescribed & Reviewed Medications", 
            "Medications with highest total patient review entries in dataset", 
            "📊"
        )
    with col2:
        render_chart_panel(
            create_rating_histogram(), 
            "Patient Satisfaction Rating Distribution", 
            "Distribution of patient satisfaction ratings on a 1 to 10 scale", 
            "📈"
        )

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # IQR Outlier Audit in Expander
    with st.expander("🔍 Outlier & IQR Preprocessing Audit"):
        st.markdown("""
        - **usefulCount Outliers**: Capped extreme counts beyond $Q_3 + 1.5 \times \text{IQR}$ to prevent popularity bias.
        - **Na_to_K Ratio**: Applied $\log(1+x)$ transformation to stabilize variance across biomarker distributions.
        - **Text Cleaning**: Stripped web scraper tags and normalized HTML entity encodings.
        """)


# ==============================================================================
# PAGE 5: 😊 SENTIMENT ANALYSIS
# ==============================================================================
elif selected_page == "😊 Sentiment Analysis":
    st.markdown("<h2 style='margin-bottom: 4px;'>😊 NLP Patient Sentiment Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Categorization of patient feedback sentiment using NLTK and Scikit-learn TF-IDF classifier.</p>", unsafe_allow_html=True)

    # KPI Row (4 cards)
    sentiment_kpis = [
        {"title": "POSITIVE REVIEWS", "value": "66.25%", "sub": "Ratings 7 to 10"},
        {"title": "NEUTRAL REVIEWS", "value": "12.01%", "sub": "Ratings 4 to 6"},
        {"title": "NEGATIVE REVIEWS", "value": "21.74%", "sub": "Ratings 1 to 3"},
        {"title": "NLP TEST ACCURACY", "value": "77.31%", "sub": "TF-IDF Classifier"}
    ]
    render_custom_kpis(sentiment_kpis)

    st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

    # Donut Chart Primary View wrapped in Panel
    render_chart_panel(
        create_sentiment_donut(), 
        "Patient Sentiment Classification Split", 
        "Distribution of Positive, Neutral, and Negative feedback across reviews", 
        "🍩"
    )

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # Supporting Table in Expander
    with st.expander("📋 Highest Rated Medicines with Positive Reviews"):
        cleaned_reviews_path = os.path.join(os.path.dirname(__file__), 'cleaned_data', 'highest_rated_positive_medicines.csv')
        if os.path.exists(cleaned_reviews_path):
            df_pos = pd.read_csv(cleaned_reviews_path)
            st.dataframe(df_pos, use_container_width=True)


# ==============================================================================
# PAGE 6: 📈 POWER BI-STYLE ANALYTICS
# ==============================================================================
elif selected_page == "📈 Power BI-style Analytics":
    st.markdown("<h2 style='margin-bottom: 4px;'>📈 Power BI Style Executive Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Native Streamlit dashboards recreating the 5 Power BI datasets.</p>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Disease Analysis",
        "Medicine Analysis",
        "Patient Analysis",
        "Drug Review",
        "Recommendation Scores"
    ])

    # Tab 1: Disease Analysis (1 chart panel + 1 table)
    with tab1:
        render_chart_panel(
            create_powerbi_disease_chart(), 
            "Top 10 Diseases by Symptom Complexity", 
            "Total symptoms identified per prognosis category", 
            "🩺"
        )
        df1 = pd.read_csv('powerbi_data/powerbi_disease_analysis.csv')
        st.dataframe(df1, use_container_width=True)

    # Tab 2: Medicine Analysis (1 chart panel + 1 table)
    with tab2:
        render_chart_panel(
            create_powerbi_medicine_chart(), 
            "Top Prescribed Medications Market Share (%)", 
            "Prescription market share across top drug profiles", 
            "💊"
        )
        df2 = pd.read_csv('powerbi_data/powerbi_medicine_analysis.csv')
        st.dataframe(df2, use_container_width=True)

    # Tab 3: Patient Analysis (1 chart panel + 1 table)
    with tab3:
        render_chart_panel(
            create_powerbi_patient_chart(), 
            "Patient Biomarkers: Age vs Na_to_K Ratio", 
            "Scatter relationship between patient age and sodium-potassium ratio", 
            "👤"
        )
        df3 = pd.read_csv('powerbi_data/powerbi_patient_demographics.csv')
        st.dataframe(df3, use_container_width=True)

    # Tab 4: Drug Review (1 chart panel + 1 table)
    with tab4:
        render_chart_panel(
            create_powerbi_review_chart(), 
            "Top 10 Drugs Sentiment Breakdown", 
            "Stacked positive, neutral, and negative review distribution", 
            "💬"
        )
        df4 = pd.read_csv('powerbi_data/powerbi_drug_reviews_summary.csv')
        st.dataframe(df4, use_container_width=True)

    # Tab 5: Recommendation Scores (1 chart panel + 1 table)
    with tab5:
        render_chart_panel(
            create_powerbi_rec_chart(), 
            "Recommendation Confidence Score by Disease (%)", 
            "Match score accuracy percentages across disease categories", 
            "🎯"
        )
        df5 = pd.read_csv('powerbi_data/powerbi_recommendation_engine.csv')
        st.dataframe(df5, use_container_width=True)


# ==============================================================================
# PAGE 7: 📚 DISEASE KNOWLEDGE BASE
# ==============================================================================
elif selected_page == "📚 Disease Knowledge Base":
    st.markdown("<h2 style='margin-bottom: 4px;'>📚 Disease Knowledge Base</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Searchable index of all 41 diseases and their defining symptoms.</p>", unsafe_allow_html=True)

    @st.cache_data
    def load_disease_knowledgebase():
        train_path = os.path.join(os.path.dirname(__file__), 'cleaned_data', 'cleaned_disease_symptoms_train.csv')
        df_train = pd.read_csv(train_path)
        
        symptom_cols = [c for c in df_train.columns if c not in ['prognosis', 'prognosis_encoded', 'symptom_count']]
        
        records = []
        for disease, group in df_train.groupby('prognosis'):
            active_symptoms = [c.replace('_', ' ').title() for c in symptom_cols if group[c].sum() > 0]
            records.append({
                'Disease Diagnosis': disease,
                'Total Associated Symptoms': len(active_symptoms),
                'Defining Symptoms': ", ".join(active_symptoms[:8]) + ("..." if len(active_symptoms) > 8 else "")
            })
        return pd.DataFrame(records)

    df_kb = load_disease_knowledgebase()
    st.dataframe(df_kb, use_container_width=True, height=500)


# ==============================================================================
# PAGE 8: 📜 PREDICTION HISTORY
# ==============================================================================
elif selected_page == "📜 Prediction History":
    st.markdown("<h2 style='margin-bottom: 4px;'>📜 Prediction History Log</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Browse, search, sort, and manage your clinical prediction logs and recommendations.</p>", unsafe_allow_html=True)

    from utils.db_manager import get_user_predictions, delete_prediction, clear_user_history
    username = st.session_state.get("username", "Guest")
    records = get_user_predictions(username)

    if not records:
        st.info("ℹ️ No prediction history found. Make a diagnosis in the AI Disease Prediction Engine page to save records.")
    else:
        # Convert records to a DataFrame for rich UI representation
        df_records = pd.DataFrame(
            records,
            columns=["ID", "Date & Time", "Symptoms", "Predicted Disease", "Recommended Medicines", "Confidence Score (%)"]
        )

        # Show searchable and sortable table
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 Prediction Records")
        st.dataframe(df_records, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Download CSV option
        csv_data = df_records.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download History as CSV",
            data=csv_data,
            file_name="healthcare_prediction_history.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

        # Actions (Delete record / Clear all history)
        st.markdown("### 🛠️ Actions & Management")
        
        col_del, col_clear = st.columns(2)

        with col_del:
            st.markdown("<div class='saas-card' style='height: 100%;'>", unsafe_allow_html=True)
            st.markdown("#### 🗑️ Delete Specific Record")
            selected_row = st.selectbox(
                "Choose a record to remove:",
                options=df_records.index,
                format_func=lambda idx: f"ID {df_records.loc[idx, 'ID']} | {df_records.loc[idx, 'Date & Time']} - {df_records.loc[idx, 'Predicted Disease']}"
            )
            if st.button("Delete Record", use_container_width=True, key="delete_record_btn"):
                db_id = int(df_records.loc[selected_row, "ID"])
                success, msg = delete_prediction(db_id, username)
                if success:
                    st.success(f"✔️ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_clear:
            st.markdown("<div class='saas-card' style='height: 100%;'>", unsafe_allow_html=True)
            st.markdown("#### 🚨 Dangerous Actions")
            
            # Use confirmation session state
            if "confirm_clear" not in st.session_state:
                st.session_state["confirm_clear"] = False

            if not st.session_state["confirm_clear"]:
                if st.button("Clear All Prediction History", type="secondary", use_container_width=True, key="start_clear_btn"):
                    st.session_state["confirm_clear"] = True
                    st.rerun()
            else:
                st.warning("⚠️ Are you sure you want to delete ALL prediction records? This cannot be undone.")
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("Yes, delete all", type="primary", use_container_width=True, key="confirm_clear_yes"):
                        success, msg = clear_user_history(username)
                        st.session_state["confirm_clear"] = False
                        if success:
                            st.success(f"✔️ {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                with col_no:
                    if st.button("Cancel", use_container_width=True, key="confirm_clear_no"):
                        st.session_state["confirm_clear"] = False
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# PAGE 9: ⚙ SETTINGS
# ==============================================================================
elif selected_page == "⚙ Settings":
    st.markdown("<h2 style='margin-bottom: 4px;'>⚙ System Settings & Preferences</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-secondary' style='margin-bottom: 24px;'>Manage UI theme configuration and view application metadata.</p>", unsafe_allow_html=True)

    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    st.markdown("### 🌗 Theme Configuration")
    
    current_t = st.session_state.get("theme", "dark")
    is_l = st.toggle("Enable Light Mode", value=(current_t == "light"), key="settings_toggle_switch")
    new_t = "light" if is_l else "dark"
    if new_t != current_t:
        st.session_state["theme"] = new_t
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    st.markdown("### ℹ️ Application Metadata")
    st.markdown("""
    - **System Version**: 2.5.0 SaaS Enterprise Edition
    - **Machine Learning Engine**: Scikit-Learn (Logistic Regression, Random Forest, TF-IDF)
    - **NLP Classifier**: NLTK Lemmatization + TF-IDF Vectorization
    - **Visualization Engine**: Plotly Static Theme System
    - **Developer & Pair Programmer**: Google Antigravity AI
    """)
    st.markdown("</div>", unsafe_allow_html=True)
