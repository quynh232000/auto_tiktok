import pyautogui
import time
import random
import os

# --- CẤU HÌNH ---
CONFIDENCE_LEVEL = 0.9
HEART_IMG = 'heart.png'
FOLLOW_IMG = 'follow.png'
COMMENT_IMG = 'comment_box.png'

# Danh sách comment có nghĩa và tự nhiên
MY_COMMENTS = [
    "Video hay qua, cho minh xin lai 1 fl nhe!",
    "Clip cuon qua ban ơi, cho minh xin 1 follow voi nha.",
    "Hay qua, minh da tim va fl ban, cho minh xin lai 1 fl nhe!",
    "Noi dung chat qua, thớt cho minh xin lai 1 follow nhe.",
    "Hay thuc su, da tim va fl, ban fl lai minh voi nha.",
    "Video hay qua, minh fl ban roi, xin lai 1 fl tu ban nhe!",
    "Dinh qua, cho minh xin lai 1 fl de cung tuong tac nhe.",
    "Chill qua ban oi, cho minh xin lai 1 follow nhe!",
    "Cuc ky huu ich, minh da fl ban, cho minh xin lai 1 fl nhe.",
    "Tuong tac cheo nhe ban, video hay qua cho minh xin 1 fl nhe."
]

def human_click(pos):
    """Di chuyển chuột đường cong và click giống người thật"""
    pyautogui.moveTo(pos[0], pos[1], 
                     duration=random.uniform(0.6, 1.2), 
                     tween=pyautogui.easeOutQuad)
    time.sleep(random.uniform(0.2, 0.5))
    pyautogui.click()

def type_like_human(text):
    """Gõ phím từng ký tự với tốc độ ngẫu nhiên (Nhập dần)"""
    for char in text:
        pyautogui.write(char)
        # Nghỉ ngẫu nhiên giữa mỗi phím từ 0.05 đến 0.25 giây
        time.sleep(random.uniform(0.05, 0.25))

def start_bot():
    print("🚀 BOT ĐANG KHỞI ĐỘNG (BẢN TƯƠNG TÁC TỰ NHIÊN)...")
    print("👉 Hãy mở trình duyệt TikTok PC và để cửa sổ hiển thị rõ.")
    time.sleep(5)

    while True:
        try:
            print("\n--- Đang quét video mới ---")
            
            # 1. Thả tim (Xác suất 90% sẽ làm)
            if random.random() < 0.9:
                heart = pyautogui.locateCenterOnScreen(HEART_IMG, confidence=CONFIDENCE_LEVEL)
                if heart:
                    human_click(heart)
                    print("❤️ Đã thả tim")
                    time.sleep(random.uniform(1, 2))

            # 2. Follow (Xác suất 40% sẽ làm để tránh spam follow)
            if random.random() < 0.4:
                follow = pyautogui.locateCenterOnScreen(FOLLOW_IMG, confidence=CONFIDENCE_LEVEL)
                if follow:
                    human_click(follow)
                    print("➕ Đã Follow")
                    time.sleep(random.uniform(1, 2))

            # 3. Comment (Xác suất 60% sẽ làm)
            if random.random() < 0.6:
                comment_box = pyautogui.locateCenterOnScreen(COMMENT_IMG, confidence=CONFIDENCE_LEVEL)
                if comment_box:
                    human_click(comment_box)
                    time.sleep(random.uniform(1.5, 2.5)) # Đợi ô nhập hiện ra hoàn toàn
                    
                    content = random.choice(MY_COMMENTS)
                    print(f"💬 Đang nhập comment dần dần: {content}")
                    type_like_human(content)
                    
                    time.sleep(random.uniform(0.8, 1.5))
                    pyautogui.press('enter')
                    print("✅ Đã gửi bình luận.")

            # 4. Thời gian xem video (Random từ 15 đến 45 giây)
            watch_time = random.randint(15, 45)
            print(f"👀 Đang xem video trong {watch_time} giây...")
            time.sleep(watch_time)

            # 5. Chuyển video (Phím mũi tên xuống)
            pyautogui.press('down')
            print("⏭️ Đã chuyển video tiếp theo.")
            time.sleep(random.uniform(3, 7))

        except Exception as e:
            print(f"🔍 Đang quét màn hình... (Chờ 5s)")
            # Nếu bị kẹt quá lâu, thử chuyển video luôn
            if random.random() < 0.3:
                pyautogui.press('down')
            time.sleep(5)

if __name__ == "__main__":
    # Đảm bảo thư mục làm việc đúng
    if os.path.exists(HEART_IMG) and os.path.exists(COMMENT_IMG):
        try:
            start_bot()
        except KeyboardInterrupt:
            print("\n🛑 Đã dừng Bot.")
    else:
        print("❌ LỖI: Bạn chưa có file heart.png hoặc comment_box.png.")
        print(f"Thư mục hiện tại: {os.getcwd()}")