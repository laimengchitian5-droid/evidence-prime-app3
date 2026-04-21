import streamlit as st
from auth import require_auth
from logic import QuantumEngine
from config import Config
import ui, uuid

st.set_page_config(page_title="Quantum Logic", layout="wide")
engine = QuantumEngine()

# 初期化
if "scores" not in st.session_state: st.session_state.scores = {t[0]: 50 for t in Config.QUESTIONS}
if "threads" not in st.session_state: st.session_state.threads = {"main": {"messages": [], "title": "Main Chat"}}
if "current_tid" not in st.session_state: st.session_state.current_tid = "main"
if "q_idx" not in st.session_state: st.session_state.q_idx = 0
if "u_color" not in st.session_state: st.session_state.u_color = "#00f2ff"

@require_auth
def main():
    # 自己最適化UI
    l_score = engine.get_load_score()
    a_color = Config.get_adaptive_color(st.session_state.u_color)
    p_mode = ui.apply_adaptive_ui(a_color, l_score)

    with st.sidebar:
        st.title("🛡️ Quantum Pro")
        st.session_state.u_color = st.color_picker("Your Energy Color", st.session_state.u_color)
        if st.button("＋ New Chat"): 
            new_id = str(uuid.uuid4())
            st.session_state.threads[new_id] = {"messages": [], "title": "New Chat"}
            st.session_state.current_tid = new_id
            st.rerun()
        st.caption(f"Performance: {p_mode}")

    # 1. 診断フェーズ
    if st.session_state.q_idx < len(Config.QUESTIONS):
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        q_type, q_text = Config.QUESTIONS[st.session_state.q_idx]
        val = st.select_slider(f"Q{st.session_state.q_idx+1}: {q_text}", range(1, 8), 4)
        if st.button("回答確定"):
            st.session_state.scores[q_type] = (st.session_state.scores[q_type] + val*10)/2
            st.session_state.q_idx += 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. メインチャットフェーズ
    else:
        # YouTube風先読み提案
        st.write("💡 あなたへの先読み提案")
        cols = st.columns(3)
        cards = engine.get_oracle_cards(st.session_state.scores)
        selected = None
        for i, card in enumerate(cards):
            if cols[i].button(card, key=f"c_{i}", use_container_width=True): selected = card

        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        # 負荷計測開始
        m = engine.monitor_load(); next(m)

        thread = st.session_state.threads[st.session_state.current_tid]
        for msg in thread["messages"]:
            with st.chat_message(msg["role"]): st.write(msg["content"])

        prompt = st.chat_input("思考を入力...") or selected
        if prompt:
            thread["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            with st.chat_message("assistant"):
                res = st.write_stream(engine.generate_stream(prompt, st.session_state.scores, "Plan"))
                thread["messages"].append({"role": "assistant", "content": res})
                if len(thread["messages"]) <= 2: thread["title"] = prompt[:10]
                st.rerun()

        try: next(m) # 負荷計測終了
        except StopIteration: pass
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__": main()
