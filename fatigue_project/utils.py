# utils.py
import plotly.graph_objects as go
import pandas as pd

# -----------------------------
# Risk Color and Level Helpers
# -----------------------------
def get_risk_color(score: float) -> str:
    """Return color based on fatigue score."""
    if score < 3:
        return "#10b981"  # Green - Safe
    elif score < 5:
        return "#f59e0b"  # Orange - Moderate
    else:
        return "#ef4444"  # Red - High

def get_risk_level(score: float) -> str:
    """Return text risk level based on score."""
    if score < 3:
        return "Low Risk"
    elif score < 5:
        return "Moderate Risk"
    else:
        return "High Risk"

def get_action_message(score: float) -> str:
    """Return safety action message based on fatigue score."""
    if score < 3:
        return ("✅ SAFE: Driver can continue driving. Maintain standard vigilance. "
                "Encourage brief breaks every 2–3 hours.")
    elif score < 5:
        return ("⚠️ CAUTION: Moderate risk — recommend a SHORT rest (15–30 min) and reassess. "
                "Avoid long or monotonous driving until score improves.")
    else:
        return ("🚫 DANGER: High risk — DO NOT DRIVE. Take a sustained rest (1–2 hours) "
                "or seek replacement before resuming.")

# -----------------------------
# Visualization Helpers
# -----------------------------
def create_gauge_chart(score: float, max_score: int = 10):
    """Create a Plotly gauge showing fatigue score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Fatigue Score", 'font': {'size': 24, 'color': '#1f2937'}},
        gauge={
            'axis': {'range': [None, max_score], 'tickwidth': 1},
            'bar': {'color': get_risk_color(score), 'thickness': 0.8},
            'steps': [
                {'range': [0, 3], 'color': '#d1fae5'},
                {'range': [3, 5], 'color': '#fef3c7'},
                {'range': [5, 10], 'color': '#fee2e2'}
            ],
            'threshold': {
                'line': {'color': "#dc2626", 'width': 4},
                'value': 5
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'family': "Inter"},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def create_feature_radar(input_data: dict):
    """Create radar chart showing driver’s current status."""
    categories = ['Sleep Quality', 'Driving Time', 'Caffeine Level', 'Rest Breaks', 'Stress Level']
    values = [
        input_data['Sleep_Hours'] / 12 * 10,
        (16 - input_data['Driving_Hours']) / 16 * 10,
        input_data['Caffeine_Cups'] / 5 * 10,
        input_data['Rest_Breaks'] / 120 * 10,
        (10 - input_data['Stress_Level']) / 10 * 10
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.2)',
        line=dict(color='#3b82f6', width=2),
        name='Current Status'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10]),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#1f2937'),
        height=350,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    return fig


def create_timeline_chart(records: pd.DataFrame):
    """Create timeline chart of fatigue scores."""
    if records.empty:
        return None

    records['Timestamp_dt'] = pd.to_datetime(records['Timestamp'])
    records = records.sort_values('Timestamp_dt')

    fig = go.Figure()
    for status in ['Alert', 'Fatigued']:
        df_status = records[records['Prediction'] == status]
        fig.add_trace(go.Scatter(
            x=df_status['Timestamp_dt'],
            y=df_status['Fatigue_Score'],
            mode='markers+lines',
            name=status,
            marker=dict(
                size=10,
                color='#10b981' if status == 'Alert' else '#ef4444',
                line=dict(width=2, color='white')
            ),
            line=dict(width=2),
            hovertemplate='<b>%{text}</b><br>Score: %{y:.2f}<br>%{x}<extra></extra>',
            text=df_status['Name']
        ))
    fig.update_layout(
        title='Fatigue Score Timeline',
        xaxis_title='Time',
        yaxis_title='Fatigue Score',
        hovermode='closest',
        paper_bgcolor='white',
        height=400,
        margin=dict(l=60, r=40, t=60, b=60),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig
