# main.py の診断部分（修正箇所抜粋）
    if st.session_state.q_idx < len(Config.QUESTIONS):
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        q_type, q_text = Config.QUESTIONS[st.session_state.q_idx]
        
        # 進行度を視覚化
        progress = (st.session_state.q_idx) / len(Config.QUESTIONS)
        st.progress(progress)
        
        st.subheader(f"Q{st.session_state.q_idx+1}: {q_text}")
        
        # 選択肢をより直感的に
        ans = st.select_slider(
            "あなたの傾向を選んでください",
            options=["全く違う", "違う", "少し違う", "どちらでもない", "少しそう思う", "そう思う", "非常にそう思う"],
            value="どちらでもない"
        )
        
        # 文字列を数値に変換するマッピング
        mapping = {"全く違う":1, "違う":2, "少し違う":3, "どちらでもない":4, "少しそう思う":5, "そう思う":6, "非常にそう思う":7}
        
        if st.button("回答を確定して次へ"):
            score_val = mapping[ans]
            # 各因子のスコアを適切に加算（最大100点換算）
            st.session_state.scores[q_type] = (st.session_state.scores[q_type] + score_val * 14) / 2
            st.session_state.q_idx += 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
