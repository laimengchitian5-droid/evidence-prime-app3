import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def apply_adaptive_ui(color, load_score):
    is_heavy = load_score > 100
    blur = "0px" if is_heavy else "15px"
    
    st.markdown(f"""
        <style>
        .stApp {{ background: radial-gradient(circle at top, {color}, #0d0d0d); background-attachment: fixed; }}
        
        /* アイケア：純白を避け、目に優しいオフホワイト + 影 */
        p, span, label, h1, h2, h3, .stMarkdown {{
            color: #e0e0e0 !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.9) !important;
        }}
        
        .main-card {{
            background: rgba(0,0,0, 0.45);
            backdrop-filter: blur({blur});
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 20px; padding: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
        }}
        
        /* 削除ボタンを小さく赤く設定 */
        .del-btn button {{
            color: #ff4b4b !important;
            border-color: #ff4b4b !important;
            padding: 0px 5px !important;
            font-size: 10px !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    return "ECO" if is_heavy else "HD"

def render_neural_pulsar(scores, color):
    labels = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    # 滑らかな曲線（spline）による波動表現
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill='toself',
        line=dict(color=color, width=4, shape='spline'),
        fillcolor="rgba(0, 242, 255, 0.2)"
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=False, range=[0, 100]),
            angularaxis=dict(color="#e0e0e0", gridcolor="rgba(255,255,255,0.1)")
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)
