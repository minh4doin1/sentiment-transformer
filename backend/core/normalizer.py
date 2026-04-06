import re

# Từ điển Teencode mở rộng
TEENCODE_DICT = {
    " ko ": " không ",
    " k ": " không ",
    " kh ": " không ",
    " h ": " giờ ",
    " dc ": " được ",
    " đc ": " được ",
    " đk ": " được ",
    " j ": " gì ",
    " vcl ": " rất ",
    " vclll ": " rất ",
    " vãi ": " rất ",
    " oke ": " ok ",
    " ok ": " ok ",
    " fb ": " facebook ",
    " ns ": " nói ",
    " bik ": " biết ",
    " bít ": " biết ",
    " mk ": " mình ",
    " m ": " mình ",
    " t ": " mình ",
    " cậu ": " bạn ",
    " c ": " bạn ",
    " uk ": " ừ ",
    " uh ": " ừ ",
    " gđ ": " gia đình ",
    " mng ": " mọi người ",
    " mn ": " mọi người ",
    " nv ": " nhân viên ",
    " nt ": " nhắn tin ",
    " r ": " rồi ",
    " rùi ": " rồi ",
    " thik ": " thích ",
    " thjk ": " thích ",
    " iu ": " yêu ",
    " chs ": " chơi ",
    " cx ": " cũng ",
    " v ":" vậy ",
    " thê ":" thế ",
    " b ":" bạn ",
    " bbi ":" bạn ",
    " mún ":" muốn ",
    " ncl ":" nói chung là ",
    " thui ":" thôi ",
    " kiki ":" cười ",
    " hihi ":" cười ",
    " haha ":" cười ",
    " hnay ": " hôm nay ",
    " hwa ": " hôm qua ",
    " chuẩn ": " đúng ",
    " đm ": " giận ",
    " đcm ": " giận ",
    " dume ": " giận ",
    " vcl ": " rất ",
    " vclll ": " rất ",
    " vãi ": " rất ",
    " hic ": " buồn ",
    " uhu ": " buồn ",
    " woa ": " ngạc nhiên ",
    " ui ": " ngạc nhiên ",
    " ôi ": " ngạc nhiên ",
    " oai ": " ngạc nhiên ",
    " gồi ": " rồi ",
    " r ": " rồi ",
    " chén ": " ăn ",
    " mừ ": " mà ",
    " bik ": " biết ",
    " mik ": " mình ",
    " tui ": " mình ",
}

# Ánh xạ Icons sang cảm xúc (Xử lý trước khi xóa ký tự đặc biệt)
ICON_DICT = {
    ":)": " vui ", ":D": " vui ", "=)": " vui ", ":(": " buồn ", ":'(": " khóc ",
    "XD": " vui ", "<3": " yêu ", "❤️": " yêu ", "😂": " cười ", "🤣": " cười ",
    "😍": " thích ", "🥰": " yêu ", "😡": " giận ", "🤬": " giận ",
    "😭": " khóc ", "😢": " buồn ", "😱": " sợ ", "😨": " sợ ",
}

def normalize_teencode(text):
    if not text: return ""
    
    # 1. Icons to text
    for icon, val in ICON_DICT.items():
        text = text.replace(icon, val)
        
    # 2. To lower
    text = text.lower()
    
    # 3. Lọc kéo dài (vuiiiii -> vui) - Chỉ lọc nếu lặp > 2 lần để tránh sai từ gốc
    text = re.sub(r'([a-z])\1{2,}', r'\1', text)
    
    # 4. Đặc biệt: xóa ký tự đặc biệt NHƯNG giữ lại khoảng trắng
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # 5. Bao quanh bằng khoảng trắng để replace chính xác từ lẻ
    text = f" {text} "
    for code, standard in TEENCODE_DICT.items():
        text = text.replace(code, standard)
        
    # 6. Clean extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

if __name__ == "__main__":
    test_cases = [
        "Hnay đi chơi vuiiii lắm luôn :))",
        "t thấy ntn? cx đc nhỉ <3",
        "đm vcl thật sự 😡",
        "iu b nhìu lém bbi",
    ]
    for t in test_cases:
        print(f"Original: {t}")
        print(f"Normalized: {normalize_teencode(t)}")
        print("-" * 20)
