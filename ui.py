import streamlit as st
import plotly.express as px
import pandas as pd

def apply_adaptive_ui(color, load_score):
    # 背景変化を強調するため、グラデーションの範囲を広げる
    st.markdown(f"""
        <style>
        .stApp {{ 
            background: linear-gradient(135deg, {color} 0%, #000000 100%) !important;
            background-attachment: fixed;
        }}
        
        /* 文字の可読性を極限まで高める（黒縁取り） */
        p, span, label, h1, h2, h3, .stMarkdown {{
            color: #ffffff !important;
            text-shadow: 2px 2px 4px #000000, -1px -1px 0 #000000, 1px -1px 0 #000000, -1px 1px 0 #000000, 1px 1px 0 #000000 !important;
        }}
        
        .main-card {{
            background: rgba(0,0,0, 0.6);
            backdrop-filter: blur(10px);
            border: 2px solid {color}; /* 選択した色で縁取る */
            border-radius: 15px; padding: 25px;
            box-shadow: 0 0 20px {color}; /* 外側に発光エフェクト */
        }}
        </style>
    """, unsafe_allow_html=True)
    return "High-Def"

def render_chart(scores, color):
    """見やすさ・扱いやすさNo.1のネオン・レーダーチャート"""
    df = pd.DataFrame(dict(
        r=list(scores.values()),
        theta=list(scores.keys())
    ))
    
    # 頂点を閉じるための処理
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_traces(
        fill='toself', 
        line_color=color, 
        line_width=4,
        fillcolor=f"rgba(255, 255, 255, 0.2)"
    )
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0.3)',
            radialaxis=dict(visible=True, range=, gridcolor="rgba(255,255,255,0.2)"),
            angularaxis=dict(color="white", font=dict(size=14, weight="bold"))
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=50, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)
