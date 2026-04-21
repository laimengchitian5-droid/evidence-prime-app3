import streamlit as st
from auth import require_auth
from logic import QuantumEngine
from config import Config
import ui
import uuid

# 1. ページ全体の初期設定
st.set_page_config(page_title="Quantum Evidence Pro", layout="wide")

# 2. エンジンとセッションの初期化（プロ仕様の状態管理）
if "engine" not in st.session_state:
    st.session_state.engine = QuantumEngine()

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
    
    # 3. 自己最適化UIの適用（重要：色を2種類受け取る）
    l_score = engine.get_load_score()
    design_color, pure_color = Config.get_adaptive_color(st.session_state.u_color)
    p_mode = ui.apply_adaptive_ui(design_color, l_score)

    # 4. サイドバー構築
    with st.sidebar:
        st.title(t_strings["welcome"])
        st.session_state.u_color = st.color_picker("Energy Color（ベース色）", st.session_state.u_color)
        
        if st.button(t_strings["new_chat"], use_container_width=True): 
            new_id = str(uuid.uuid4())
            st.session_state.threads[new_id] = {"messages": [], "title": "新規チャット"}
            st.session_state.current_tid = new_id
            st.rerun()
        
        st.divider()
        st.write(t_strings["history"])
        for tid, data in st.session_state.threads.items():
            if st.button(data["title"], key=f"thread_{tid}", use_container_width=True):
                st.session_state.current_tid = tid
                st.rerun()
        
        st.divider()
        st.caption(f"Mode: {p_mode} | Load: {l_score}")

    # --- メインコンテンツ ---

    # 5. 精密性格診断フェーズ
    if st.session_state.q_idx < len(Config.QUESTIONS):
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader("🧬 精密性格診断")
        
        q_type, q_text = Config.QUESTIONS[st.session_state.q_idx]
        progress = (st.session_state.q_idx) / len(Config.QUESTIONS)
        st.progress(progress)
        
        st.write(f"**Q{st.session_state.q_idx + 1}: {q_text}**")
        
        ans_label = st.select_slider(
            "あてはまるものを選んでください",
            options=["全く違う", "違う", "少し違う", "どちらでもない", "少しそう思う", "そう思う", "非常にそう思う"],
            value="どちらでもない",
            key=f"q_slider_{st.session_state.q_idx}"
        )
        
        mapping = {"全く違う":1, "違う":2, "少し違う":3, "どちらでもない":4, "少しそう思う":5, "そう思う":6, "非常にそう思う":7}
        
        if st.button(t_strings["next_btn"], use_container_width=True):
            score_val = mapping[ans_label]
            # 100点満点換算の移動平均
            st.session_state.scores[q_type] = (st.session_state.scores[q_type] + score_val * 14) / 2
            st.session_state.q_idx += 1
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 6. チャット & 先読みフェーズ
    else:
        # YouTube風先読み提案（診断結果に基づき自動生成）
        st.write(t_strings["oracle_msg"])
        cols = st.columns(3)
        cards = engine.get_oracle_cards(st.session_state.scores)
        selected_card = None
        for i, card in enumerate(cards):
            if cols[i].button(card, key=f"card_{i}", use_container_width=True):
                selected_card = card

        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        # 自己分析チャート（安全な pure_color を渡す）
        with st.expander(t_strings["analysis_chart"]):
            ui.render_chart(st.session_state.scores, pure_color)
            for trait, val in st.session_state.scores.items():
                st.session_state.scores[trait] = st.slider(f"手動調整: {trait}", 0, 100, int(val))

        # 負荷計測開始
        monitor = engine.monitor_load()
        next(monitor)

        # スレッド管理
        thread = st.session_state.threads[st.session_state.current_tid]
        for msg in thread["messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # 入力処理（先読みカード or 通常入力）
        prompt_input = st.chat_input(t_strings["placeholder"])
        final_prompt = selected_card if selected_card else prompt_input

        if final_prompt:
            thread["messages"].append({"role": "user", "content": final_prompt})
            with st.chat_message("user"):
                st.write(final_prompt)
            
            with st.chat_message("assistant"):
                # ストリーミング応答
                response_stream = engine.generate_stream(final_prompt, st.session_state.scores, "Quantum")
                full_res = st.write_stream(response_stream)
                thread["messages"].append({"role": "assistant", "content": full_res})
                
                # タイトルの自動更新
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
