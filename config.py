import datetime

class Config:
    # 15問の精密診断質問リスト
    QUESTIONS = [
        ("開放性", "新しいアイデアや概念を考えるのが好きだ"), 
        ("開放性", "芸術的な活動に強い関心がある"), 
        ("開放性", "想像力が豊かだ"),
        ("誠実性", "物事を効率よく丁寧に進められる"), 
        ("誠実性", "計画を最後までやり遂げる"), 
        ("誠実性", "細かいミスにも気づく"),
        ("外向性", "初対面の人とでも楽しく話せる"), 
        ("外向性", "活発でエネルギーに満ちている"), 
        ("外向性", "グループで中心的な役割を担う"),
        ("協調性", "他人の感情に共感できる"), 
        ("協調性", "人を信じ親切に接する"), 
        ("協調性", "周囲との調和を重視する"),
        ("情緒安定性", "ストレス場面でも冷静でいられる"), 
        ("情緒安定性", "感情の起伏が穏やかだ"), 
        ("情緒安定性", "些細なことで不安にならない")
    ]

    # アプリ内の全文字列（日本語化）
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
        """時間帯とユーザーの好みを同期させる色彩アルゴリズム"""
        try:
            hour = datetime.datetime.now().hour
            # 夜間（18時〜5時）は彩度を落として目に優しく
            if 18 <= hour or hour < 5:
                return f"color-mix(in srgb, {base_hex}, black 60%)"
            # 朝（5時〜10時）は少し白を混ぜて爽やかに
            elif 5 <= hour < 10:
                return f"color-mix(in srgb, {base_hex}, white 20%)"
            return base_hex
        except:
            return base_hex # 万が一の時もエラーを出さない
