"""
Plotly Interactive Visualization & Card Panel Module
-----------------------------------------------------
Contains static, theme-independent Plotly charts wrapped in polished card-style panels.
Chart colors, chart backgrounds, and data-viz color palettes stay 100% identical in both modes.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Static Palette & Chart Setup (Theme-Independent)
STATIC_COLORS = ['#6366F1', '#10B981', '#F59E0B', '#EC4899', '#8B5CF6', '#06B6D4']

def apply_static_chart_theme(fig, title=None):
    """Applies a single, static theme-independent layout to all Plotly figures."""
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(family="Inter, sans-serif", color='#F1F5F9', size=12),
        margin=dict(l=15, r=15, t=30 if title else 15, b=25),
        xaxis=dict(gridcolor='#1F2937', showgrid=True),
        yaxis=dict(gridcolor='#1F2937', showgrid=True)
    )
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=13, color='#F1F5F9')))
    return fig

def render_chart_panel(fig, title, subtitle="", icon="📊"):
    """
    Wraps a Plotly chart in a card-style container with rounded corners, border, padding, 
    and a clear title row with subtitle separated by a thin divider.
    Removes Plotly modebar clutter (displayModeBar=False).
    """
    st.markdown(f"""
    <div style="
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: var(--card-shadow);
    ">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.15rem;">{icon}</span>
            <div>
                <div style="font-weight: 700; font-size: 0.95rem; color: var(--text-primary);">{title}</div>
                {f'<div style="font-size: 0.78rem; color: var(--text-secondary); margin-top: 2px;">{subtitle}</div>' if subtitle else ''}
            </div>
        </div>
        <hr style="border: none; border-top: 1px solid var(--border); margin: 12px 0 16px 0;" />
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# 1. Donut Chart: Patient Sentiment Split
def create_sentiment_donut():
    labels = ['Positive', 'Negative', 'Neutral']
    values = [106857, 35070, 19370] # Total 161,297 reviews
    colors = ['#10B981', '#EF4444', '#F59E0B']

    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=0.55,
        marker=dict(colors=colors, line=dict(color='#151E2E', width=2)),
        textinfo='percent',
        hovertemplate='<b>%{label} Review Sentiment</b><br>Review Count: <b>%{value:,}</b><br>Percentage: <b>%{percent}</b><extra></extra>'
    )])

    # Center Label inside Donut Hole
    fig.add_annotation(
        text="<b>161,297</b><br><span style='font-size:10px; color:#94A3B8;'>Reviews</span>",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=15, color='#F1F5F9', family='Inter')
    )

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color='#F1F5F9', size=12),
        margin=dict(l=10, r=10, t=10, b=40),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        )
    )
    return fig

# 2. Bar Chart: Top 5 Prescribed Drugs
def create_top_prescribed_bar():
    drugs = ['Ethinyl est. / noreth.', 'Nexplanon', 'Ethinyl estradiol', 'Etonogestrel', 'Levonorgestrel']
    counts = [1845, 2156, 2828, 3336, 3657] # Ordered ascending for horizontal bar

    fig = go.Figure(data=[go.Bar(
        x=counts,
        y=drugs,
        orientation='h',
        text=[f"{c:,}" for c in counts],
        textposition='outside',
        textfont=dict(size=11, color='#F1F5F9', family='Inter'),
        marker=dict(
            color=['#818CF8', '#6366F1', '#4F46E5', '#4338CA', '#3730A3'], # Shades of indigo/blue gradient by rank
            cornerradius=6
        ),
        hovertemplate='<b>%{y}</b><br>Prescription Count: <b>%{x:,}</b><extra></extra>'
    )])

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color='#F1F5F9', size=12),
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis=dict(showgrid=False, zeroline=False, range=[0, 4200]),
        yaxis=dict(showgrid=True, gridcolor='#1F2937'),
        showlegend=False
    )
    return fig

# 3. Horizontal Bar Chart: Top Reviewed Drugs (Drug Review Analysis Page)
def create_top_reviewed_bar():
    drugs = ['Sertraline', 'Escitalopram', 'Miconazole', 'Bupropion', 'Duloxetine']
    reviews = [1420, 1280, 1150, 1090, 980]

    fig = px.bar(
        x=reviews, y=drugs, orientation='h',
        labels={'x': 'Total Reviews', 'y': 'Drug Name'},
        color=reviews,
        color_continuous_scale=['#06B6D4', '#6366F1']
    )
    fig.update_layout(coloraxis_showscale=False)
    fig.update_yaxes(autorange="reversed")
    return apply_static_chart_theme(fig)

# 4. Rating Distribution Histogram (1-10 Scale)
def create_rating_histogram():
    df_rev = pd.read_csv('cleaned_data/cleaned_drug_reviews_train.csv')
    fig = px.histogram(
        df_rev, x='rating', nbins=10,
        color_discrete_sequence=['#8B5CF6'],
        labels={'rating': 'Patient Rating (1 to 10 Scale)', 'count': 'Review Count'}
    )
    fig.update_layout(bargap=0.1)
    return apply_static_chart_theme(fig)

# 5. Native Power BI Tab 1: Disease Analysis Chart
def create_powerbi_disease_chart():
    df = pd.read_csv('powerbi_data/powerbi_disease_analysis.csv').head(10)
    fig = px.bar(
        df, x='Disease_Prognosis', y='Total_Symptoms_Identified',
        color='Avg_Symptom_Count',
        color_continuous_scale='Blues',
        labels={'Disease_Prognosis': 'Disease Diagnosis', 'Total_Symptoms_Identified': 'Total Symptoms Identified'}
    )
    return apply_static_chart_theme(fig)

# 6. Native Power BI Tab 2: Medicine Analysis Chart
def create_powerbi_medicine_chart():
    df = pd.read_csv('powerbi_data/powerbi_medicine_analysis.csv').head(10)
    fig = px.bar(
        df, x='Drug_Name', y='Market_Share_Pct',
        color='Avg_Patient_Age',
        color_continuous_scale='Purples',
        labels={'Drug_Name': 'Medication', 'Market_Share_Pct': 'Market Share (%)'}
    )
    return apply_static_chart_theme(fig)

# 7. Native Power BI Tab 3: Patient Analysis Chart
def create_powerbi_patient_chart():
    df = pd.read_csv('powerbi_data/powerbi_patient_demographics.csv')
    fig = px.scatter(
        df, x='Age', y='Na_to_K', color='Drug', size='Age',
        color_discrete_sequence=STATIC_COLORS,
        labels={'Na_to_K': 'Sodium-to-Potassium Ratio'}
    )
    return apply_static_chart_theme(fig)

# 8. Native Power BI Tab 4: Drug Review Chart
def create_powerbi_review_chart():
    df = pd.read_csv('powerbi_data/powerbi_drug_reviews_summary.csv').head(10)
    fig = px.bar(
        df, x='drugName', y=['Positive_Reviews', 'Neutral_Reviews', 'Negative_Reviews'],
        barmode='stack',
        color_discrete_sequence=['#10B981', '#F59E0B', '#EF4444'],
        labels={'drugName': 'Medication', 'value': 'Review Count'}
    )
    return apply_static_chart_theme(fig)

# 9. Native Power BI Tab 5: Recommendation Scores Chart
def create_powerbi_rec_chart():
    df = pd.read_csv('powerbi_data/powerbi_recommendation_engine.csv').head(10)
    fig = px.line(
        df, x='Disease_Prognosis', y='Recommendation_Confidence_Score',
        markers=True,
        line_shape='spline',
        color_discrete_sequence=['#06B6D4'],
        labels={'Disease_Prognosis': 'Disease', 'Recommendation_Confidence_Score': 'Confidence Score (%)'}
    )
    return apply_static_chart_theme(fig)
