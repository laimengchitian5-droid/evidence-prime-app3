import time
import uuid
import streamlit as st
from groq import Groq

class QuantumEngine:
    def __init__(self):
        # 負荷監視用データの初期化
        if "loads" not in st.session_state:
            st.session_state.loads = []

    def monitor_load(self):
        """
        処理時間を計測し、負荷スコアを算出。
        main.pyで generator として呼び出されることを想定。
        """
        start = time.time()
        yield
        duration = time.time() - start
        st.session_state.loads.append(duration)
        # 直近5回分のデータで平均を出す（自己最適化用）
        if len(st.session_state.loads) > 5:
            st.session_state.loads.pop(0)

    def get_load_score(self):
        """負荷状況を数値化（0-1000）"""
        if not st.session_state.get("loads"):
            return 0
        avg = sum(st.session_state.loads) / len(st.session_state.loads)
        return int(avg * 1000)

    def get_oracle_cards(self, scores):
        """性格に基づくYouTube風の先読み提案リスト"""
        # 開放性や誠実性に応じた動的なトピック選定
        openness = scores.get("開放性", 50)
        if openness > 60:
            return ["未来のAI共生社会", "量子コンピュータの衝撃", "意識のデジタル化"]
        elif scores.get("誠実性", 50) > 60:
            return ["論理的思考の強化", "効率的なタスク管理", "現状の課題分析"]
        else:
            return ["自己理解の深化", "新しい視点の獲得", "対話による発想"]

    def generate_stream(self, prompt, scores, mode):
        """
        エラー耐性を極限まで高めたストリーミング生成。
        AttributeErrorを完全に回避します。
        """
        client = Groq(api_key=st.session_state.api_key)
        
        # 思考モードと性格をAIに注入
        system_instruction = (
            f"User Personality: {scores}\n"
            f"Thinking Mode: {mode}\n"
            "Respond in Japanese. Be logical yet empathetic."
        )
        
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )
            
            for chunk in stream:
                # 安全なプロパティアクセスの連鎖（ここがエラー対策の核心）
                if not chunk.choices:
                    continue
                
                delta = chunk.choices[0].delta
                
                # content属性が存在し、かつNoneでない場合のみyield
                if hasattr(delta, 'content') and delta.content is not None:
                    yield delta.content
                    
        except Exception as e:
            yield f"⚠️ システムエラーが発生しました: {str(e)}"
