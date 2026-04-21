import streamlit as st
from auth import require_auth
from logic import QuantumEngine
from config import Config
import ui
import uuid

# ページ設定
st.set_page_config(page_title="Quantum Logic Pro", layout="wide")

# エンジンの初期化
if "engine" not in st.session_state:
    st.session_state.engine = QuantumEngine()

# セッション状態の初期化
if "scores" not in st.session_state:
    st.session_state.scores = {t: 50 for t in ["開放性", "誠実性", "外向性", "協調性", "情緒安定性"]}
if "threads" not in st.session_state:
    st.session_state.threads = {"main": {"messages": [], "title": "メインチャット"}}
if "current_tid" not in st.session_state:
    st.session_state.current_tid = "main"
if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0
if "u_color" not in st.session_state:
    st.session_state.u_color = "#00f2ff"

@require_auth
def main():
    engine = st.session_state.engine
    t_strings = Config.STRINGS
    
    # 1. 自己最適化UIの適用
    l_score = engine.get_load_score()
    a_color = Config.get_adaptive_color(st.session_state.u_color)
    p_mode = ui.apply_adaptive_ui(a_color, l_score)

    # 2. サイドバー構築
    with st.sidebar:
        st.title("🛡️ Quantum Pro")
        st.session_state.u_color = st.color_picker("Energy Color（背景色）", st.session_state.u_color)
        
        if st.button("＋ 新規チャット", use_container_width=True): 
            new_id = str(uuid.uuid4())
            st.session_state.threads[new_id] = {"messages": [], "title": "新規チャット"}
            st.session_state.current_tid = new_id
            st.rerun()
        
        st.divider()
        st.write("🕒 履歴")
        for tid, data in st.session_state.threads.items():
            if st.button(data["title"], key=f"thread_{tid}", use_container_width=True):
                st.session_state.current_tid = tid
                st.rerun()
        
        st.divider()
        st.caption(f"Performance: {p_mode} | Load: {l_score}")

    # --- メインコンテンツエリア ---
    
    # 3. 性格診断フェーズ
    if st.session_state.q_idx < len(Config.QUESTIONS):
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader("🧬 精密性格診断（Big Five）")
        
        q_type, q_text = Config.QUESTIONS[st.session_state.q_idx]
        progress = (st.session_state.q_idx) / len(Config.QUESTIONS)
        st.progress(progress)
        
        st.write(f"**Q{st.session_state.q_idx+1}: {q_text}**")
        
        ans_label = st.select_slider(
            "あてはまるものを選んでください",
            options=["全く違う", "違う", "少し違う", "どちらでもない", "少しそう思う", "そう思う", "非常にそう思う"],
            value="どちらでもない",
            key=f"q_slider_{st.session_state.q_idx}"
        )
        
        mapping = {"全く違う":1, "違う":2, "少し違う":3, "どちらでもない":4, "少しそう思う":5, "そう思う":6, "非常にそう思う":7}
        
        if st.button("回答を確定して次へ", use_container_width=True):
            score_val = mapping[ans_label]
            st.session_state.scores[q_type] = (st.session_state.scores[q_type] + score_val * 14) / 2
            st.session_state.q_idx += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 4. チャット & 先読みフェーズ
    else:
        # YouTube風先読み提案
        st.write("💡 **AIからの先読み提案（思考の種）**")
        cols = st.columns(3)
        cards = engine.get_oracle_cards(st.session_state.scores)
        selected_card = None
        for i, card in enumerate(cards):
            if cols[i].button(card, key=f"card_{i}", use_container_width=True):
                selected_card = card

        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        # 診断結果の表示（折りたたみ）
        with st.expander("📊 あなたの性格分析チャートを表示"):
            ui.render_chart(st.session_state.scores, a_color)
            for trait, val in st.session_state.scores.items():
                st.session_state.scores[trait] = st.slider(f"手動調整: {trait}", 0, 100, int(val))

        # 負荷計測開始
        monitor = engine.monitor_load()
        next(monitor)

        # チャット履歴表示
        thread = st.session_state.threads[st.session_state.current_tid]
        for msg in thread["messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # 入力処理（先読みカードが押されたらそれを優先）
        prompt_input = st.chat_input("論理の検察官にメッセージを送信...")
        final_prompt = selected_card if selected_card else prompt_input

        if final_prompt:
            thread["messages"].append({"role": "user", "content": final_prompt})
            with st.chat_message("user"):
                st.write(final_prompt)
            
            with st.chat_message("assistant"):
                # A-Cモデルの自動判別（簡易版：Planモード固定を動的に）
                response_stream = engine.generate_stream(final_prompt, st.session_state.scores, "Adaptive")
                full_res = st.write_stream(response_stream)
                thread["messages"].append({"role": "assistant", "content": full_res})
                
                # チャットタイトルの自動更新
                if len(thread["messages"]) <= 2:
                    thread["title"] = final_prompt[:12]
                st.rerun()

        try:
            next(monitor)
        except StopIteration:
            pass
            
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
