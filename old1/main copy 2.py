import pyautogui
import time
import random
import os

# --- CẤU HÌNH ---
CONFIDENCE_LEVEL = 0.7  # Độ chính xác (0.9 là rất cao để tránh bấm nhầm)
HEART_IMG = 'heart.png'
FOLLOW_IMG = 'follow.png'
COMMENT_IMG = 'comment_box.png'

# Danh sách nội dung comment ngẫu nhiên
MY_COMMENTS = [
    "Video hay quá bạn ơi! ❤️",
    "Nội dung chất lượng thật sự.",
    "Rất hữu ích, cảm ơn bạn!",
    "Chill phết nhỉ, thả tim nha.",
    "Đỉnh quá chủ thớt ơi!",
    "Tương tác cùng nhau phát triển nhé!",
    "Hay quá, hóng video tiếp theo."
]

def human_move_and_click(pos):
    """Di chuyển chuột mượt mà và click giống người thật"""
    # Di chuyển đến vị trí trong khoảng 0.5 - 1.2 giây
    pyautogui.moveTo(pos[0], pos[1], 
                     duration=random.uniform(0.6, 1.1), 
                     tween=pyautogui.easeOutQuad)
    time.sleep(random.uniform(0.2, 0.4))
    pyautogui.click()

def type_like_human(text):
    """Gõ phím từng chữ với tốc độ ngẫu nhiên"""
    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(0.08, 0.25))

def start_bot():
    # Lấy kích thước màn hình để giới hạn vùng quét (chỉ quét bên phải)
    sw, sh = pyautogui.size()
    # Region = (x, y, width, height) -> Nửa bên phải màn hình
    right_region = (sw // 2, 0, sw // 2, sh)

    print("🚀 Bot đang khởi động... Hãy mở trình duyệt TikTok PC!")
    print("🔔 Mẹo: Để cửa sổ trình duyệt chiếm toàn màn hình.")
    time.sleep(5)

    while True:
        try:
            print("\n--- Đang quét video mới ---")
            
            # 1. Thả tim (Chỉ quét vùng bên phải)
            heart = pyautogui.locateCenterOnScreen(HEART_IMG, region=right_region, confidence=CONFIDENCE_LEVEL)
            if heart:
                human_move_and_click(heart)
                print("❤️ Đã thả tim thành công!")
                time.sleep(random.uniform(1, 2))
            else:
                print("🔍 Không tìm thấy nút Tim (Có thể đã thả hoặc ảnh không khớp).")

            # 2. Follow (Chỉ quét vùng bên phải)
            follow = pyautogui.locateCenterOnScreen(FOLLOW_IMG, region=right_region, confidence=CONFIDENCE_LEVEL)
            if follow:
                human_move_and_click(follow)
                print("➕ Đã nhấn Follow!")
                time.sleep(random.uniform(1, 2))

            # 3. Comment
            comment_box = pyautogui.locateCenterOnScreen(COMMENT_IMG, region=right_region, confidence=CONFIDENCE_LEVEL)
            if comment_box:
                human_move_and_click(comment_box)
                time.sleep(random.uniform(1, 2))
                
                content = random.choice(MY_COMMENTS)
                type_like_human(content)
                
                time.sleep(random.uniform(0.5, 1))
                pyautogui.press('enter')
                print(f"💬 Đã gửi comment: {content}")
            
            # 4. Xem video trong khoảng thời gian ngẫu nhiên (15-35 giây)
            watch_time = random.randint(15, 35)
            print(f"👀 Đang xem video trong {watch_time}s để tránh bị quét Bot...")
            time.sleep(watch_time)

            # 5. Chuyển video (Phím xuống)
            print("⏭️ Đang chuyển sang video tiếp theo...")
            pyautogui.press('down')
            
            # Đợi video mới tải nội dung
            time.sleep(random.uniform(3, 6))

        except Exception as e:
            print(f"⚠️ Đang tìm mục tương tác... (Chờ video load)")
            pyautogui.press('down')
            time.sleep(5)

if __name__ == "__main__":
    # Kiểm tra file ảnh trước khi chạy
    missing = [f for f in [HEART_IMG, FOLLOW_IMG, COMMENT_IMG] if not os.path.exists(f)]
    if missing:
        print(f"❌ Lỗi: Thiếu các file ảnh sau trong thư mục: {missing}")
        print("Hãy chụp màn hình các nút và lưu đúng tên file .png!")
    else:
        try:
            start_bot()
        except KeyboardInterrupt:
            print("\n🛑 Đã dừng Bot.")