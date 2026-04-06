# Bộ từ điển từ khóa cảm xúc tiếng Việt (Vietnam Sentiment Lexicon)
# Dùng để hỗ trợ tính năng Giải thích AI (Explainability) và Highlights

EMOTION_LEXICON = {
    "Enjoyment": [
        "vui", "sướng", "hạnh phúc", "tuyệt", "ngon", "đẹp", "xịn", "thích", "yêu", "đỉnh", 
        "mừng", "mê", "phê", "đã", "hợp", "dui", "hí", "hehe", "haha", "kkk", "smile", 
        "good", "nice", "love", "heart", "♥️", "❤️", "🥰", "😍", "🤩", "😊", "😄", "😁",
        "hài lòng", "ok", "ổn", "chuẩn", "chất", "top", "best", "vip", "xịn sò", "mượt",
        "phê lòi", "đỉnh chóp", "mê ly", "tuyệt cú mèo", "iu nhất", "cưng xỉu"
    ],
    "Sadness": [
        "buồn", "khóc", "hổ thẹn", "đau", "khổ", "mệt", "chán", "thất vọng", "tiếc", "nhớ",
        "huhu", "hic", "haizz", "sad", "bad", "tệ", "kém", "mất", "hết", "tan nát", "chia tay",
        "😭", "😢", "☹️", "😔", "😞", "😟", "😿", "💔", "🥀", "đen", "xui", "đắng", "khinh",
        "bế tắc", "buông xuôi", "tan chậm", "nặng lòng", "vụn vỡ", "ế"
    ],
    "Anger": [
        "giận", "điên", "bực", "ghét", "chửi", "láo", "đểu", "ức", "vcl", "vãi", "cmn", "đéo",
        "tức", "hận", "khùng", "đất", "phẫn nộ", "độc", "ác", "tồi", "tổ", "nóng", "cáu",
        "😡", "😠", "🤬", "👿", "💢", "👊", "🖕", "quạo", "coi khinh", "coi thường", "lừa",
        "bực bội", "ức chế", "bố láo", "mất dạy", "đồ hèn", "đồ súc vật"
    ],
    "Fear": [
        "sợ", "hãi", "lo", "hãi hùng", "kinh", "ghê", "run", "ám", "ma", "nguy", "hiểm",
        "cướp", "giật", "chết", "máu", "tai nạn", "bão", "dịch", "rung", "hốt", "hoảng",
        "😰", "😨", "😱", "😬", "🥶", "🆘", "💀", "💩", "quỷ", "tâm linh", "điềm",
        "thót tim", "hú hồn", "rợn người", "sợ vcl", "run cầm cập"
    ],
    "Disgust": [
        "ghê", "tởm", "bẩn", "kinh", "ô", "uế", "rác", "xấu", "mùi", "thối", "hôi", "ghét",
        "khinh", "rẻ", "đê tiện", "biến thái", "dâm", "mù", "quáng", "ngu", "đần",
        "🤮", "🤢", "😷", "💩", "👎", "🙄", "🤨", "rẻ tiền", "không ra gì", "dơ",
        "kinh tởm", "hãm", "tởm lợm", "phát gớm", "coi rẻ"
    ],
    "Surprise": [
        "ngạc nhiên", "sốc", "wow", "ủa", "alo", "gì", "thế", "nào", "không ngờ", "twists",
        "lạ", "kỳ", "biến", "phốt", "tin", "shock", "bất ngờ", "đột nhiên", "tự nhiên",
        "😲", "😮", "🤯", "🧐", "❓", "⁉️", "đỉnh vậy", "thật không", "ảo", "vãi nồi",
        "bật ngửa", "hết hồn", "chấn động"
    ]
}

def get_all_keywords():
    all_k = []
    for words in EMOTION_LEXICON.values():
        all_k.extend(words)
    return list(set(all_k))
