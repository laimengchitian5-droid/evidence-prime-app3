import streamlit as st
import plotly.express as px
import pandas as pd

def apply_adaptive_ui(color, load_score):
    """
    背景色の変化を「激変」させるためのグラデーション・エンジン。
    """
    is_heavy = load_score > 100
    blur = "0px" if is_heavy else "15px"
    
    st.markdown(f"""
        <style>
        /* 背景を単なる色ではなく、選択色から黒への強烈なグラデーションに変更 */
        .stApp {{ 
            background: linear-gradient(135deg, {color} 0%, #000000 100%) !important;
            background-attachment: fixed;
        }}
        
        /* 文字の可読性を極限まで高める（強力なアウトラインと影） */
        p, span, label, h1, h2, h3, li, .stMarkdown {{
            color: #ffffff !important;
            text-shadow: 
                2px 2px 4px #000000, 
                -1px -1px 0 #000000, 
                1px -1px 0 #000000, 
                -1px 1px 0 #000000, 
                1px 1px 0 #000000 !important;
        }}
        
        /* メインカードの枠線をユーザーの色で発光させる */
        .main-card {{
            background: rgba(0,0,0, 0.65);
            backdrop-filter: blur({blur});
            border: 2px solid {color} !important; 
            border-radius: 20px; 
            padding: 25px;
            box-shadow: 0 0 25px {color}66; /* 40%程度の透明度で発光 */
            margin-bottom: 20px;
        }}
        </style>
    """, unsafe_allow_html=True)
    return "ECO" if is_heavy else "HD"

def render_chart(scores, color):
    """
    直感的な多角形レーダーチャート。
    main.pyから呼び出される名前を 'render_chart' に完全固定。
    """
    try:
        # データ構築
        df = pd.DataFrame(dict(
            r=list(scores.values()),
            theta=list(scores.keys())
        ))
        
        # グラフを閉じるための末尾追加
        df_closed = pd.concat([df, df.iloc[[0]]], ignore_index=True)
        
        # 描画設定
        fig = px.line_polar(df_closed, r='r', theta='theta', line_close=True)
        
        fig.update_traces(
            fill='toself', 
            line_color=color, 
            line_width=4,
            fillcolor="rgba(255, 255, 255, 0.25)", # 内部は少し白く透かす
            markers=True # 頂点を強調して扱いやすくする
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            polar=dict(
                bgcolor='rgba(0,0,0,0.2)',
                radialaxis=dict(
                    visible=True, 
                    range=[0, 100], 
                    gridcolor="rgba(255,255,255,0.2)",
                    tickfont=dict(color="white")
                ),
                angularaxis=dict(
                    color="white", 
                    font=dict(size=14, weight="bold"),
                    gridcolor="rgba(255,255,255,0.2)"
                )
            ),
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error("分析チャートの描画中にエラーが発生しました。")
