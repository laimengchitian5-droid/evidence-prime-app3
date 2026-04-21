# ui.py
import streamlit as st
import plotly.express as px
import pandas as pd

def apply_adaptive_ui(color, load_score):
    is_heavy = load_score > 100
    blur = "0px" if is_heavy else "12px"
    opacity = "0.95" if is_heavy else "0.3"
    
    # 【プロの工夫】文字を読みやすくするための影とコントラスト設定
    st.markdown(f"""
        <style>
        .stApp {{ 
            background: radial-gradient(circle at top, {color}, #050505); 
            color: #ffffff !important; 
        }}
        /* 全てのテキストに薄い影をつけて背景から浮かせ、可読性を確保 */
        p, span, label, .stMarkdown {{
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
            color: #ffffff !important;
        }}
        .main-card {{
            background: rgba(0,0,0,{opacity});
            backdrop-filter: blur({blur});
            border: 1px solid {color};
            border-radius: 20px; padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        /* スライダーの文字も見やすく */
        .stSlider label {{
            background: rgba(0,0,0,0.4);
            padding: 2px 10px;
            border-radius: 5px;
        }}
        </style>
    """, unsafe_allow_html=True)
    return "ECO" if is_heavy else "High-Def"

def render_chart(scores, color):
    # 既存のチャートコードを維持
    df = pd.DataFrame(dict(r=list(scores.values()), theta=list(scores.keys())))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself', line_color=color)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            angularaxis=dict(color="white", gridcolor="rgba(255,255,255,0.2)"),
            radialaxis=dict(visible=False)
        )
    )
    st.plotly_chart(fig, use_container_width=True)
