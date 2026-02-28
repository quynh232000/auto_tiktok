import pyautogui
import time
import random
import os

# Cấu hình
CONFIDENCE_LEVEL = 0.9  
HEART_IMG = 'heart.png'
COMMENT_IMG = 'comment_box.png'
FOLLOW_IMG = 'follow.png'

# Danh sách comment đa dạng
MY_COMMENTS = [
    "Video hay quá bạn ơi! ❤️",
    "Nội dung chất lượng thật sự.",
    "Rất hữu ích, cảm ơn bạn!",
    "Chill phết nhỉ, thả tim nha.",
    "Đỉnh quá chủ thớt ơi!",
    "Tương tác cùng nhau phát triển nhé!"
]

def human_click(pos):
    """Di chuyển chuột mượt mà và click"""
    # pyautogui.easeOutQuad giúp chuột di chuyển chậm dần khi đến đích (giống người)
    pyautogui.moveTo(pos[0], pos[1], 
                     duration=random.uniform(0.5, 1.2), 
                     tween=pyautogui.easeOutQuad)
    
    time.sleep(random.uniform(0.2, 0.5))
    pyautogui.click()

def start_bot():
    print("🚀 Bot đang khởi động... Hãy mở trình duyệt TikTok PC!")
    time.sleep(5)
    
    while True:
        try:
            # 1. Thả tim
            heart = pyautogui.locateCenterOnScreen(HEART_IMG, confidence=CONFIDENCE_LEVEL)
            if heart:
                human_click(heart)
                print("❤️ Đã thả tim")
                time.sleep(random.uniform(1, 2))
            
            # 2. Follow
            follow = pyautogui.locateCenterOnScreen(FOLLOW_IMG, confidence=CONFIDENCE_LEVEL)
            if follow:
                human_click(follow)
                print("➕ Đã Follow")
                time.sleep(random.uniform(1, 2))

            # 3. Comment
            comment_box = pyautogui.locateCenterOnScreen(COMMENT_IMG, confidence=CONFIDENCE_LEVEL)
            if comment_box:
                human_click(comment_box)
                time.sleep(random.uniform(1, 2))
                
                content = random.choice(MY_COMMENTS)
                # Gõ từng chữ với tốc độ khác nhau
                for char in content:
                    pyautogui.write(char)
                    time.sleep(random.uniform(0.05, 0.2))
                
                time.sleep(random.uniform(0.5, 1))
                pyautogui.press('enter')
                print(f"💬 Đã comment: {content}")
                
            # 4. Xem video ngẫu nhiên từ 10-20 giây
            wait_time = random.randint(10, 20)
            print(f"👀 Đang xem video trong {wait_time}s...")
            time.sleep(wait_time)

            # 5. Chuyển video (Phím mũi tên xuống cho TikTok Web)
            pyautogui.press('down')
            print("⏭️ Đã chuyển video tiếp theo")
            time.sleep(random.uniform(3, 5))

        except Exception as e:
            print(f"🔍 Đang quét màn hình... (Chờ video tải)")
            pyautogui.press('down') # Nếu bị kẹt thì chuyển video luôn
            time.sleep(5)

if __name__ == "__main__":
    # Đảm bảo các file ảnh tồn tại
    if os.path.exists(HEART_IMG) and os.path.exists(COMMENT_IMG):
        start_bot()
    else:
        print("❌ Lỗi: Bạn chưa có file heart.png hoặc comment_box.png trong thư mục!")