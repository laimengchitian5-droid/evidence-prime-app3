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
            text-shadow: 2px 2px 4px #000000 !important;
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
    エラーを物理的に回避する堅牢な多角形チャート。
    """
    try:
        # 1. データのクレンジング
        traits = ["開放性", "誠実性", "外向性", "協調性", "情緒安定性"]
        safe_data = []
        for t in traits:
            val = scores.get(t, 50)
            try:
                safe_data.append(dict(項目=t, 値=float(val)))
            except:
                safe_data.append(dict(項目=t, 値=50.0))
        
        df = pd.DataFrame(safe_data)

        # 2. 描画（エラーの出やすい引数を排除し、最小構成で作成）
        fig = px.line_polar(
            df, 
            r='値', 
            theta='項目', 
            line_close=True
        )
        
        # 3. 装飾（バリデーションに通りやすい標準的な設定）
        fig.update_traces(
            fill='toself', 
            line=dict(color=color, width=4),
            marker=dict(size=8, color="white"),
            fillcolor="rgba(255, 255, 255, 0.2)"
        )
        
        # 4. レイアウト調整（rangeの指定を安全な方法に変更）
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                bgcolor='rgba(0,0,0,0.2)',
                radialaxis=dict(
                    visible=True, 
                    range=[0, 100], # リスト形式で明示的に指定
                    gridcolor="rgba(255,255,255,0.2)",
                    tickfont=dict(color="white")
                ),
                angularaxis=dict(
                    color="white",
                    font=dict(size=12)
                )
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"描画エンジンを調整中...")
        # 最終手段：数値のみをシンプルに表示
        cols = st.columns(len(scores))
        for i, (k, v) in enumerate(scores.items()):
            cols[i].metric(k, f"{int(v)}")
