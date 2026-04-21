import datetime

class Config:
    # 質問データは維持（省略）
    QUESTIONS = [
        ("開放性", "新しいアイデアや概念を考えるのが好きだ"), ("開放性", "芸術的な活動に強い関心がある"), ("開放性", "想像力が豊かだ"),
        ("誠実性", "物事を効率よく丁寧に進められる"), ("誠実性", "計画を最後までやり遂げる"), ("誠実性", "細かいミスにも気づく"),
        ("外向性", "初対面の人とでも楽しく話せる"), ("外向性", "活発でエネルギーに満ちている"), ("外向性", "グループで中心的な役割を担う"),
        ("協調性", "他人の感情に共感できる"), ("協調性", "人を信じ親切に接する"), ("協調性", "周囲との調和を重視する"),
        ("情緒安定性", "ストレス場面でも冷静でいられる"), ("情緒安定性", "感情の起伏が穏やかだ"), ("情緒安定性", "些細なことで不安にならない")
    ]

    STRINGS = {
        "welcome": "🛡️ Quantum Evidence Pro",
        "oracle_msg": "💡 AIからの先読み提案",
        "placeholder": "メッセージを送信...",
        "new_chat": "＋ 新規チャット",
        "history": "🕒 会話履歴",
        "sync_setting": "⚙️ 性格の修正",
        "analysis_chart": "📊 性格分析（リアルタイム）",
        "next_btn": "確定して次へ"
    }

    @staticmethod
    def get_adaptive_color(base_hex):
        """変化がはっきりわかるように色の配合を100%以上に強化"""
        hour = datetime.datetime.now().hour
        # 夜間はベース色を濃くし、昼間は明るさを強調
        if 18 <= hour or hour < 5:
            # 黒との配合を強めて重厚に
            design_color = f"color-mix(in srgb, {base_hex}, #000000 80%)"
        else:
            # 白との配合を強めて鮮やかに
            design_color = f"color-mix(in srgb, {base_hex}, #ffffff 20%)"
        return design_color, base_hex
