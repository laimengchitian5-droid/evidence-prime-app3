import streamlit as st
import plotly.express as px
import pandas as pd

def apply_adaptive_ui(color, load_score):
    # 負荷が高い(100以上)と透過とボケをオフにして高速化
    is_heavy = load_score > 100
    blur = "0px" if is_heavy else "12px"
    opacity = "0.95" if is_heavy else "0.2"
    
    st.markdown(f"""
        <style>
        .stApp {{ background: radial-gradient(circle at top, {color}, #050505); }}
        .main-card {{
            background: rgba(0,0,0,{opacity});
            backdrop-filter: blur({blur});
            border: 1px solid {color};
            border-radius: 20px; padding: 25px;
        }}
        .oracle-btn {{ border: 1px solid {color} !important; border-radius: 10px !important; }}
        </style>
    """, unsafe_allow_html=True)
    return "ECO" if is_heavy else "High-Def"

def render_chart(scores, color):
    df = pd.DataFrame(dict(r=list(scores.values()), theta=list(scores.keys())))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself', line_color=color)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', polar=dict(bgcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig, use_container_width=True)
