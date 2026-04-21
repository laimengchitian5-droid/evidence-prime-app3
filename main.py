import streamlit as st
from auth import require_auth
from logic import QuantumEngine
from config import Config
import ui, uuid

st.set_page_config(page_title="Quantum Logic Pro", layout="wide")

if "engine" not in st.session_state: st.session_state.engine = QuantumEngine()
if "scores" not in st.session_state: st.session_state.scores = {t: 50 for t in ["開放性", "誠実性", "外向性", "協調性", "情緒安定性"]}
if "threads" not in st.session_state: st.session_state.threads = {"main": {"messages": [], "title": "Main Chat"}}
if "current_tid" not in st.session_state: st.session_state.current_tid = "main"
if "q_idx" not in st.session_state: st.session_state.q_idx = 0
if "u_color" not in st.session_state: st.session_state.u_color = "#00f2ff"

@require_auth
def main():
    engine = st.session_state.engine
    t = Config.STRINGS
    l_score = engine.get_load_score()
    d_color, p_color = Config.get_adaptive_color(st.session_state.u_color)
    p_mode = ui.apply_adaptive_ui(d_color, l_score)

    with st.sidebar:
        st.title(t["welcome"])
        st.session_state.u_color = st.color_picker("Energy Color", st.session_state.u_color)
        
        if st.button(t["new_chat"], use_container_width=True): 
            new_id = str(uuid.uuid4())
            st.session_state.threads[new_id] = {"messages": [], "title": "New Chat"}
            st.session_state.current_tid = new_id
            st.rerun()
        
        st.divider()
        st.write(t["history"])
        for tid in list(st.session_state.threads.keys()):
            col_t, col_d = st.columns([0.8, 0.2])
            if col_t.button(st.session_state.threads[tid]["title"], key=f"btn_{tid}", use_container_width=True):
                st.session_state.current_tid = tid
                st.rerun()
            if tid != "main":
                with col_d:
                    st.markdown('<div class="del-btn">', unsafe_allow_html=True)
                    if st.button("×", key=f"del_{tid}"):
                        del st.session_state.threads[tid]
                        st.session_state.current_tid = "main"
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.q_idx < len(Config.QUESTIONS):
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        q_type, q_text = Config.QUESTIONS[st.session_state.q_idx]
        st.progress(st.session_state.q_idx / len(Config.QUESTIONS))
        st.subheader(f"Q{st.session_state.q_idx+1}: {q_text}")
        ans = st.select_slider("傾向を選択", options=["全く違う", "違う", "少し違う", "普通", "少しそう思う", "そう思う", "非常にそう思う"], value="普通")
        mapping = {"全く違う":1, "違う":2, "少し違う":3, "普通":4, "少しそう思う":5, "そう思う":6, "非常にそう思う":7}
        if st.button(t["next_btn"]):
            st.session_state.scores[q_type] = (st.session_state.scores[q_type] + mapping[ans]*14)/2
            st.session_state.q_idx += 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write(t["oracle_msg"])
        cols = st.columns(3); cards = engine.get_oracle_cards(st.session_state.scores)
        selected = None
        for i, card in enumerate(cards):
            if cols[i].button(card, key=f"oracle_{i}", use_container_width=True): selected = card

        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        with st.expander(t["analysis_chart"]):
            ui.render_neural_pulsar(st.session_state.scores, p_color)
        
        m = engine.monitor_load(); next(m)
        thread = st.session_state.threads[st.session_state.current_tid]
        for msg in thread["messages"]:
            with st.chat_message(msg["role"]): st.write(msg["content"])

        prompt = st.chat_input(t["placeholder"]) or selected
        if prompt:
            thread["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            with st.chat_message("assistant"):
                res = st.write_stream(engine.generate_stream(prompt, st.session_state.scores, "Quantum"))
                thread["messages"].append({"role": "assistant", "content": res})
                if len(thread["messages"]) <= 2: thread["title"] = prompt[:12]
                st.rerun()
        try: next(m)
        except StopIteration: pass
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__": main()
