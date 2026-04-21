import streamlit as st
import plotly.express as px
import pandas as pd

def apply_adaptive_ui(color, load_score):
    """背景の変化を激変させるグラデーション・エンジン"""
    is_heavy = load_score > 100
    blur = "0px" if is_heavy else "15px"
    
    st.markdown(f"""
        <style>
        .stApp {{ 
            background: linear-gradient(135deg, {color} 0%, #000000 100%) !important;
            background-attachment: fixed;
        }}
        p, span, label, h1, h2, h3, li, .stMarkdown {{
            color: #ffffff !important;
            text-shadow: 2px 2px 4px #000000, 1px 1px 0 #000000 !important;
        }}
        .main-card {{
            background: rgba(0,0,0, 0.65);
            backdrop-filter: blur({blur});
            border: 2px solid {color} !important; 
            border-radius: 20px; padding: 25px;
            box-shadow: 0 0 25px {color}66;
            margin-bottom: 20px;
        }}
        </style>
    """, unsafe_allow_html=True)
    return "ECO" if is_heavy else "HD"

def render_chart(scores, color):
    """
    データの異常を自動修正する堅牢なレーダーチャート。
    """
    try:
        # 1. データのバリデーション（空や異常値を防ぐ）
        if not scores or not isinstance(scores, dict):
            st.warning("性格データがまだ生成されていません。")
            return

        # 数値が文字列になっていたり、Noneだったりする場合に備えて安全に変換
        safe_scores = {}
        traits = ["開放性", "誠実性", "外向性", "協調性", "情緒安定性"]
        for t in traits:
            val = scores.get(t, 50) # データがない場合は中央値の50をセット
            try:
                safe_scores[t] = float(val)
            except:
                safe_scores[t] = 50.0

        # 2. Plotly用データ作成
        df = pd.DataFrame(dict(
            r=list(safe_scores.values()),
            theta=list(safe_scores.keys())
        ))
        
        # 3. 描画（エラー回避のためにシンプルなpx.line_polarを使用）
        fig = px.line_polar(
            df, 
            r='r', 
            theta='theta', 
            line_close=True,
            range_r=[0, 100] # グラフの範囲を0-100に固定
        )
        
        fig.update_traces(
            fill='toself', 
            line_color=color, 
            line_width=4,
            fillcolor="rgba(255, 255, 255, 0.2)",
            markers=True
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                bgcolor='rgba(0,0,0,0.2)',
                radialaxis=dict(visible=True, gridcolor="rgba(255,255,255,0.2)"),
                angularaxis=dict(color="white", font=dict(size=12))
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"グラフ描画システムを再起動中... (Error: {str(e)})")
        # 最悪の場合、表形式でデータを出す（プロの予備プラン）
        st.table(pd.DataFrame([scores]))
