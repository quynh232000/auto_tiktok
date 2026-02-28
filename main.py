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
COPPY_IMG = 'copy.png'
DOWN_IMG = 'down.png' # Nút mũi tên xuống trên giao diện TikTok PC

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
    
    # --- GIẢI QUYẾT VẤN ĐỀ FOCUS (BẮT BUỘC) ---
    time.sleep(1.5)
    # Cách 1: Nhấn ESC để thoát ô nhập liệu
    # pyautogui.press('esc') 
    # Cách 2: Click vào vùng trống bên trái (thường là vùng video) để nhả focus
    # pyautogui.click(200, 400) 
    # print("🔓 Đã Un-focus ô nhập liệu")


def action_down():
    down_btn = pyautogui.locateCenterOnScreen(DOWN_IMG, confidence=CONFIDENCE_LEVEL)
    if down_btn:
        human_click(down_btn)
        print("⏭️ Đã bấm nút NEXT (Down)")
    else:
        # Nếu không thấy nút thì bấm phím mũi tên xuống
        pyautogui.press('down')
        print("⏭️ Đã nhấn phím DOWN để NEXT")
def start_bot():
    print("🚀 BOT ĐANG KHỞI ĐỘNG ...")
    time.sleep(5)

    try_count = 0
    while True:
        if try_count >= 10: # Tăng giới hạn lỗi lên 10 lần cho thoải mái
            print("❌ Lỗi quá nhiều lần, dừng bot để kiểm tra.")
            break
        
        try:
            print("\n" + "="*30)
            
            # 1. Thả tim (Xác suất 90%)
            if random.random() < 0.5:
                heart = pyautogui.locateCenterOnScreen(HEART_IMG, confidence=CONFIDENCE_LEVEL)
                if heart:
                    human_click(heart)
                    print("❤️ Đã thả tim")
                    time.sleep(random.uniform(1, 2))
                else:
                    print("xxx Không tìm thấy nút tim")

            # 2. Follow (Xác suất 100% như bạn đặt)
            follow = pyautogui.locateCenterOnScreen(FOLLOW_IMG, confidence=CONFIDENCE_LEVEL)
            if follow:
                human_click(follow)
                print("➕ Đã bấm Follow")
                time.sleep(random.uniform(1, 2))
            else:
                print("xxx Không tìm thấy nút follow")
                
            # 2. Follow (Xác suất 100% như bạn đặt)
            

            # 3. Comment & Un-focus
            comment_box = pyautogui.locateCenterOnScreen(COMMENT_IMG, confidence=CONFIDENCE_LEVEL)
            if comment_box:
                human_click(comment_box)
                time.sleep(random.uniform(1.5, 2.5))
                
                content = random.choice(MY_COMMENTS)
                paste_comment(content)
            else:
                print("xxx Không tìm thấy nút comment")

            if random.random() < 0.6:
                coppy_image = pyautogui.locateCenterOnScreen(COPPY_IMG, confidence=CONFIDENCE_LEVEL)
                if coppy_image:
                    human_click(coppy_image)
                    print(" Đã bấm copy")
                    time.sleep(random.uniform(1, 2))
                else:
                    print("xxx Không tìm thấy nút coppy")
                    
                    
            # 4. Countdown thời gian xem
            watch_time = random.randint(5, 20)
            countdown_timer(watch_time)

            # 5. Chuyển video
            # Thử tìm nút bấm Down trên màn hình trước
            action_down()
                
            # Reset try_count khi một chu kỳ thành công
            try_count = 0
            time.sleep(random.uniform(3, 6))

        except Exception as e:
            print(f"🔍 Không tìm thấy mục tương tác hoặc lỗi: {e}")
            # pyautogui.press('esc') # Thoát mọi cửa sổ hiện hữu nếu có lỗi
            time.sleep(5)
            action_down()
            try_count += 1

if __name__ == "__main__":
    if os.path.exists(HEART_IMG) and os.path.exists(COMMENT_IMG):
        try:
            start_bot()
        except KeyboardInterrupt:
            print("\n🛑 Đã dừng Bot.")
    else:
        print("❌ LỖI: Thiếu file ảnh mẫu (heart.png hoặc comment_box.png).")