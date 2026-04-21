import time, uuid, streamlit as st
from groq import Groq

class QuantumEngine:
    def monitor_load(self):
        """処理時間を計測し、負荷スコアを算出"""
        start = time.time()
        yield
        duration = time.time() - start
        if "loads" not in st.session_state: st.session_state.loads = []
        st.session_state.loads.append(duration)
        if len(st.session_state.loads) > 5: st.session_state.loads.pop(0)

    def get_load_score(self):
        if "loads" not in st.session_state or not st.session_state.loads: return 0
        return int(sum(st.session_state.loads) / len(st.session_state.loads) * 1000)

    def get_oracle_cards(self, scores):
        """性格に基づく先読み提案リスト"""
        if scores.get("開放性", 50) > 60:
            return ["未来のAI共生社会", "量子コンピュータの衝撃", "意識のデジタル化"]
        return ["論理的思考の強化", "効率的なタスク管理", "現状の課題分析"]

    def generate_stream(self, prompt, scores, mode):
        client = Groq(api_key=st.session_state.api_key)
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"UserPersonality:{scores}. Mode:{mode}. Reply in Japanese."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        for chunk in stream:
            if chunk.choices.delta.content: yield chunk.choices.delta.content
