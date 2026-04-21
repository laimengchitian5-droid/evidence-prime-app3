import streamlit as st
import plotly.express as px
import pandas as pd

def apply_adaptive_ui(color, load_score):
    """
    負荷(load_score)に応じた自己最適化UI。
    文字の読みやすさを最優先したCSSを注入。
    """
    is_heavy = load_score > 100
    blur = "0px" if is_heavy else "15px"
    opacity = "0.95" if is_heavy else "0.25"
    
    # 【文字の可読性向上】text-shadowを多層化し、どんな背景色でも文字を浮き上がらせる
    st.markdown(f"""
        <style>
        .stApp {{ 
            background: radial-gradient(circle at top, {color}, #050505); 
            background-attachment: fixed;
        }}
        
        /* 全てのテキスト要素に強力な可読性保護を適用 */
        p, span, label, h1, h2, h3, .stMarkdown, .stSelectbox, .stSlider {{
            color: #ffffff !important;
            text-shadow: 
                0px 2px 4px rgba(0,0,0,0.9),
                0px 0px 10px rgba(0,0,0,0.5) !important;
            font-weight: 500 !important;
        }}
        
        /* メインカードの透過・ボケ設定 */
        .main-card {{
            background: rgba(0,0,0,{opacity});
            backdrop-filter: blur({blur});
            -webkit-backdrop-filter: blur({blur});
            border: 1px solid {color};
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.7);
            margin-bottom: 20px;
        }}
        
        /* 入力エリア等の視認性確保 */
        .stChatInputContainer {{
            background-color: rgba(255,255,255,0.05) !important;
            border-radius: 15px !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    return "ECOモード（高速）" if is_heavy else "フルスペック（美麗）"

def render_chart(scores, color):
    """
    新世代レーダーチャート。
    ValueErrorを回避するため、色の指定を安全な形式に限定。
    """
    try:
        # データの構築
        df = pd.DataFrame(dict(
            r=list(scores.values()),
            theta=list(scores.keys())
        ))
        
        # 描画
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        
        # 【重要】colorには純粋な16進数（#RRGGBB）のみを適用する
        fig.update_traces(
            fill='toself', 
            line_color=color, 
            fillcolor=f"rgba(0, 242, 255, 0.3)", # 透過ネオンブルーで固定
            line_width=3
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                angularaxis=dict(
                    color="white", 
                    gridcolor="rgba(255,255,255,0.2)",
                    font=dict(size=12)
                ),
                radialaxis=dict(
                    visible=False, # 目盛りを消してスタイリッシュに
                    range=[0, 100]
                )
            ),
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        # 万が一のエラー時もアプリを止めない
        st.error(f"分析チャートの描画をスキップしました（安全策）")
