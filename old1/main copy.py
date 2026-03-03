import pyautogui
import time
import random
import os
import pyperclip  # Cài đặt: pip install pyperclip

# --- CẤU HÌNH ---
CONFIDENCE_LEVEL = 0.8
HEART_IMG = 'heart.png'
FOLLOW_IMG = 'follow.png'
COMMENT_IMG = 'comment_box.png'
DOWN_IMG = 'down.png'

# Danh sách comment xin follow
MY_COMMENTS = [
    "Video hay qua, cho minh xin lai 1 fl nhe!",
    "Clip cuon qua ban oi, cho minh xin 1 follow voi nha.",
    "Hay qua, minh da tim va fl ban, cho minh xin lai 1 fl nhe!",
    "Noi dung chat qua, thot cho minh xin lai 1 follow nhe.",
    "Hay thuc su, da tim va fl, ban fl lai minh voi nha.",
    "Video hay qua, minh fl ban roi, xin lai 1 fl tu ban nhe!",
    "Dinh qua, cho minh xin lai 1 fl de cung tuong tac nhe.",
    "Chill qua ban oi, cho minh xin lai 1 follow nhe!",
    "Cuc ky huu ich, minh da fl ban, cho minh xin lai 1 fl nhe.",
    "Tuong tac cheo nhe ban, video hay qua cho minh xin 1 fl nhe."
]

def countdown_timer(seconds):
    """Hiển thị đếm ngược xem video"""
    for i in range(seconds, 0, -1):
        print(f"👀 Đang xem video... Còn lại {i} giây ", end="\r")
        time.sleep(1)
    print("⏭️ Đã xem xong!                                ")

def human_click(pos):
    """Di chuyển chuột mượt và click"""
    pyautogui.moveTo(pos[0], pos[1], 
                     duration=random.uniform(0.6, 1.2), 
                     tween=pyautogui.easeOutQuad)
    time.sleep(random.uniform(0.3, 0.6))
    pyautogui.click()

def paste_comment(text):
    """Copy và dán nội dung vào ô comment"""
    pyperclip.copy(text)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.8)
    pyautogui.press('enter')
    print(f"✅ Đã gửi: {text}")
    
    # --- GIẢI QUYẾT VẤN ĐỀ FOCUS ---
    time.sleep(1)
    # Cách 1: Nhấn ESC để thoát ô nhập liệu
    # pyautogui.press('esc') 
    # # Cách 2: Click đại vào một khoảng không (ví dụ mép trái màn hình) để thoát focus
    # pyautogui.click(100, 400) 
    # print("🔓 Đã Un-focus ô nhập liệu")

def start_bot():
    print("🚀 BOT ĐANG KHỞI ĐỘNG ...")
    time.sleep(8)

    try_count = 0
    while True:
        try:
            print("\n" + "="*30)
            
            # 1. Thả tim
            if random.random() < 0.9:
                heart = pyautogui.locateCenterOnScreen(HEART_IMG, confidence=CONFIDENCE_LEVEL)
                if heart:
                    human_click(heart)
                    print("❤️ Đã thả tim")
                    time.sleep(random.uniform(1, 2))

            # 2. Follow
            if random.random() < 1:
                follow = pyautogui.locateCenterOnScreen(FOLLOW_IMG, confidence=CONFIDENCE_LEVEL)
                if follow:
                    human_click(follow)
                    print("➕ Đã bấm Follow")
                    time.sleep(random.uniform(1, 2))

            # 3. Comment & Un-focus
            if random.random() < 1:
                comment_box = pyautogui.locateCenterOnScreen(COMMENT_IMG, confidence=CONFIDENCE_LEVEL)
                if comment_box:
                    human_click(comment_box)
                    time.sleep(random.uniform(1.5, 2.5))
                    
                    content = random.choice(MY_COMMENTS)
                    paste_comment(content)

            # 4. Countdown thời gian xem
            watch_time = random.randint(10, 20)
            countdown_timer(watch_time)

            # 5. Chuyển video (Lúc này phím DOWN sẽ hoạt động vì đã Un-focus)
            
            down = pyautogui.locateCenterOnScreen(DOWN_IMG, confidence=CONFIDENCE_LEVEL)
            if down:
                    human_click(down)
                    print("➕ Đã bấm down")
                    time.sleep(random.uniform(1, 2))
            else:
                pyautogui.press('down')
                print("➕ Đã press next")
                
                
            time.sleep(random.uniform(3, 6))

        except Exception as e:
            print(f"🔍 Đang tìm video... (Thử lại sau 5s)")
            # pyautogui.press('esc') # Chữa cháy nếu bị kẹt focus
            time.sleep(5)

if __name__ == "__main__":
    if os.path.exists(HEART_IMG) and os.path.exists(COMMENT_IMG):
        try:
            start_bot()
        except KeyboardInterrupt:
            print("\n🛑 Đã dừng Bot.")
    else:
        print("❌ LỖI: Thiếu file ảnh mẫu.")