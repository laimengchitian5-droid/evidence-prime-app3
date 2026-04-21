# main.py の一部抜粋（チャート呼び出し部分を修正）
    else:
        # 先読み
        st.write(t["oracle_msg"])
        cols = st.columns(3); cards = engine.get_oracle_cards(st.session_state.scores)
        for i, card in enumerate(cards):
            if cols[i].button(card, key=f"c_{i}", use_container_width=True): selected = card

        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        # グラフを「扱いやすく」戻した
        with st.expander(t["analysis_chart"], expanded=True):
            ui.render_chart(st.session_state.scores, p_color) # 以前の名前から変更
            st.write("💡 スライダーで性格を微調整できます")
            for trait in st.session_state.scores.keys():
                st.session_state.scores[trait] = st.slider(trait, 0, 100, int(st.session_state.scores[trait]))

        # チャット履歴（以降、以前のロジックを継続）
