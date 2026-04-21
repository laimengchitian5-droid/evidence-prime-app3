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
        "sync_setting": "⚙️ 性格の動的修正",
        "analysis_chart": "📊 ニューラル・パルサー（新世代グラフ）",
        "next_btn": "回答を確定して次へ"
    }

    @staticmethod
    def get_adaptive_color(base_hex):
        hour = datetime.datetime.now().hour
        pure_color = base_hex 
        # 夜間(18-5時)はアイケア・アンバーを20%ブレンド
        if 18 <= hour or hour < 5:
            design_color = f"color-mix(in srgb, {base_hex}, #ffaa00 20%, black 70%)"
        else:
            design_color = f"color-mix(in srgb, {base_hex}, #fff5e6 10%, black 40%)"
        return design_color, pure_color
