# config.py
import datetime

class Config:
    QUESTIONS = [
        ("開放性", "新しいアイデアや概念を考えるのが好きだ"), ("開放性", "芸術的な活動に強い関心がある"), ("開放性", "想像力が豊かだ"),
        ("誠実性", "物事を効率よく丁寧に進められる"), ("誠実性", "計画を最後までやり遂げる"), ("誠実性", "細かいミスにも気づく"),
        ("外向性", "初対面の人とでも楽しく話せる"), ("外向性", "活発でエネルギーに満ちている"), ("外向性", "グループで中心的な役割を担う"),
        ("協調性", "他人の感情に共感できる"), ("協調性", "人を信じ親切に接する"), ("協調性", "周囲との調和を重視する"),
        ("情緒安定性", "ストレス場面でも冷静でいられる"), ("情緒安定性", "感情の起伏が穏やかだ"), ("情緒安定性", "些細なことで不安にならない")
    ]

    STRINGS = {
        "welcome": "🛡️ Quantum Evidence Pro",
        "oracle_msg": "💡 AIからの先読み提案（思考の種）",
        "placeholder": "論理の検察官にメッセージを送信...",
        "new_chat": "＋ 新規チャット",
        "history": "🕒 会話履歴",
        "sync_setting": "⚙️ 性格の自動修正",
        "analysis_chart": "📊 自己分析チャート",
        "next_btn": "回答を確定して次へ"
    }

    @staticmethod
    def get_adaptive_color(base_hex):
        """
        グラフエラー回避版：
        デザイン用の複雑な色(mix)と、グラフ用の純粋な色(pure)を両方返す
        """
        hour = datetime.datetime.now().hour
        is_dark = 18 <= hour or hour < 5
        
        # グラフ用の純粋な色（エラー防止）
        pure_color = base_hex 
        
        # CSSデザイン用の装飾色
        if is_dark:
            design_color = f"color-mix(in srgb, {base_hex}, black 60%)"
        else:
            design_color = base_hex
            
        return design_color, pure_color
