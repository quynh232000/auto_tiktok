import pyautogui
import time
import random
import os
import pyperclip
import pygetwindow as gw

# UI
import tkinter as tk
from tkinter import filedialog, messagebox,scrolledtext
from PIL import Image, ImageTk
import shutil
import threading
import sys
import keyboard
# init 
running_flag = False

# --- CẤU HÌNH ---
def resource_path(relative_path):
    """ Lấy đường dẫn tuyệt đối đến tài nguyên, dùng cho cả dev và PyInstaller """
    try:
        # PyInstaller tạo một thư mục tạm và lưu đường dẫn trong _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
CONFIDENCE_LEVEL = 0.8
HEART_IMG = resource_path('image/heart.png')
FOLLOW_IMG = resource_path('image/follow.png')
COMMENT_IMG = resource_path('image/comment_box.png')
COPPY_IMG = resource_path('image/copy.png')
DOWN_IMG = resource_path('image/down.png')
NOT_FULL_SCREEN = resource_path("image/not_full.png")

MY_COMMENTS = [
    "Video hay quá, cho mình xin lại 1 follow nhé!",
    "Clip cuốn quá bạn ơi, cho mình xin 1 follow với nha.",
    "Hay quá, mình đã thả tim và follow bạn, cho mình xin lại 1 follow nhé!",
    "Nội dung chất quá, chủ thớt cho mình xin lại 1 follow nhé.",
    "Hay thực sự, đã tim và follow, bạn follow lại mình với nha.",
    "Video tuyệt quá, mình follow bạn rồi, xin lại 1 follow từ bạn nhé!",
    "Đỉnh quá, cho mình xin lại 1 follow để cùng tương tác nhé.",
    "Chill quá bạn ơi, cho mình xin lại 1 follow nhé!",
    "Cực kỳ hữu ích, mình đã follow bạn, cho mình xin lại 1 follow nhé.",
]
DEFAULT_COMMENTS = "\n".join(MY_COMMENTS)


def smart_sleep(seconds, ui_instance):
    global running_flag
    for _ in range(int(seconds * 10)): 
        if not running_flag:
            return False 
        time.sleep(0.1)
    return True
def countdown_timer(seconds, ui_instance):
    """Đếm ngược và cập nhật trên dòng cuối cùng của Log Box"""
    global running_flag
    
    # Ghi dòng đầu tiên để có cái mà xóa
    print("👀 Đang chuẩn bị xem video...") 

    for i in range(seconds, 0, -1):
        if not running_flag: 
            break
            
        msg = f"👀 Đang xem video... Còn lại {i} giây"
        
        # Cập nhật giao diện
        ui_instance.log_box.config(state="normal")
        # Xóa từ dòng cuối cùng ngược lên 1 dòng
        ui_instance.log_box.delete("insert-1l", "insert") 
        ui_instance.log_box.insert(tk.END, msg + "\n")
        ui_instance.log_box.see(tk.END)
        ui_instance.log_box.config(state="disabled")
        
        # BẮT BUỘC có dòng này để Tkinter vẽ lại giao diện ngay lập tức
        ui_instance.window.update_idletasks() 
        
        time.sleep(1)
        
    print("⏭️ Đã xem xong!                                ")

def human_click(pos):
    """Di chuyển chuột mượt và click"""
    pyautogui.moveTo(pos[0], pos[1], 
                     duration=random.uniform(0.6, 1), 
                     tween=pyautogui.easeOutQuad)
    time.sleep(random.uniform(1,5))
    offset_x = random.randint(-5, 5)
    offset_y = random.randint(-5, 5)
    pyautogui.click(pos[0] + offset_x, pos[1] + offset_y)

def paste_comment(text):
    """Copy và dán nội dung vào ô comment"""
    pyperclip.copy(text)
    time.sleep(random.uniform(1, 3))
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(random.uniform(1, 3))
    pyautogui.press('enter')
    # print(f"✅ Đã gửi: {text}")
    time.sleep(random.uniform(1, 3))


def action_down():
    try:
        down_btn = pyautogui.locateCenterOnScreen(DOWN_IMG, confidence=CONFIDENCE_LEVEL)
        if down_btn:
            human_click(down_btn)
            return {
                "status":True,
                "message":f"-> Đã bấm nút NEXT (Down)"
            }
        else:
            pyautogui.press('down')
            return {
                "status":True,
                "message":f"-> Đã nhấn phím DOWN để NEXT"
            }
    except Exception as e:
        return {
                "status":False,
                "message":f"Error: {e}"
            }
def action_heart():
    try:
        heart = pyautogui.locateCenterOnScreen(HEART_IMG, confidence=CONFIDENCE_LEVEL)
        if heart:
            human_click(heart)
            time.sleep(random.uniform(1, 2))
            return {
                "status":True,
                "message":f"+ Đã thả tim"
            }
        else:
            return {
                "status":False,
                "message":f"xxx Không tìm thấy nút tim"
            }
    except Exception as e:
        return {
                "status":False,
                "message":f"Error: {e}"
            }
def action_follow():
    try:
        heart = pyautogui.locateCenterOnScreen(FOLLOW_IMG, confidence=CONFIDENCE_LEVEL)
        if heart:
            human_click(heart)
            time.sleep(random.uniform(1, 2))
            return {
                "status":True,
                "message":f"+ Đã bấm Follow"
            }
        else:
            return {
                "status":False,
                "message":f"xxx Không tìm thấy nút follow"
            }
    except Exception as e:
        return {
                "status":False,
                "message":f"Error: {e}"
            }
def action_comment(ui_instance):
    try:
        # 1. Tìm ô comment
        comment_box = pyautogui.locateCenterOnScreen(COMMENT_IMG, confidence=CONFIDENCE_LEVEL)
        if comment_box:
            human_click(comment_box)
            time.sleep(random.uniform(1, 2))
            
            # 2. Lấy dữ liệu từ giao diện
            raw_text = ui_instance.comment_input.get("1.0", tk.END).strip()
            # Tách dòng thành mảng, bỏ dòng trống
            comment_list = [line.strip() for line in raw_text.split('\n') if line.strip()]
            
            if not comment_list:
                return {"status": False, "message": "⚠️ Ô comment trống, không có gì để gửi!"}
                
            # 3. Chọn ngẫu nhiên và gửi
            content = random.choice(comment_list)
            paste_comment(content)
            return {"status": True, "message": f"+ Đã gửi: {content}"}
        else:
            return {"status": False, "message": "xxx Không thấy ô comment"}
    except Exception as e:
        return {"status": False, "message": f"Error: {e}"}
def action_coppy():
    try:
        coppy_image = pyautogui.locateCenterOnScreen(COPPY_IMG, confidence=CONFIDENCE_LEVEL)
        if coppy_image:
            human_click(coppy_image)
            time.sleep(random.uniform(1, 2))
            return {
                "status":True,
                "message":"+ Đã bấm copy"
            }
        else:
            return {
                "status":False,
                "message":"xxx Không tìm thấy nút coppy"
            }
    except Exception as e:
        return {
                "status":False,
                "message":f"Error: {e}"
            }
def ensure_fullscreen():
    try:
        window = gw.getActiveWindow()
        
        screen_width, screen_height = pyautogui.size()
        if window.width < screen_width or window.height < screen_height:
            print("🖥️ Màn hình chưa Full. Đang nhấn F11...")
            pyautogui.press('f11')
            time.sleep(2)
            return False
        else:
            print("✅ Màn hình đã ở chế độ Full Screen.")
            return True
    except Exception as e:
        print(f"⚠️ Không thể kiểm tra cửa sổ: {e}")
        pyautogui.press('f11')
def check_f11_by_image():
    try:
        if pyautogui.locateOnScreen(NOT_FULL_SCREEN, confidence=CONFIDENCE_LEVEL):
            pyautogui.press('f11')
            print("⌨️ Đã nhấn F11")
    except Exception as e:
        print("⌨️ Màn hình phải full")   
        
        
# start bot
def start_bot(ui_instance):
    running_flag = True
    # print("🚀 BOT ĐANG KHỞI ĐỘNG ...")
    time.sleep(random.uniform(5,8))
    print("... Check full màn hình ...")
    check_f11_by_image()
    time.sleep(random.uniform(1,3))
    

    try_count = 0
    while running_flag:
        
        if try_count >= 10:
            print("❌ Lỗi quá nhiều lần, dừng bot để kiểm tra.")
            break
        
        try:
            time.sleep(random.uniform(0.5, 1))
            print("\n" + "="*30)
            res_follow = action_follow()
            print(res_follow["message"])
            if res_follow["status"] == False:
                print("⚠️ Không follow được, chuyển video ngay lập tức...")
                action_down()
                time.sleep(random.uniform(2, 6)) # Đợi một chút cho video load
                continue
            # 0. Xem video
            
            watch_time = random.randint(5, 20)
            countdown_timer(watch_time,ui_instance)
            
            # 1. Thả tim (Xác suất 50% như code của bạn)
            
            if random.random() < 0.5:
                res_heart = action_heart()
                print(res_heart["message"])
            
            # 3. Comment
            if random.random() < 0.7: # Nên thêm xác suất để tránh bị đánh dấu spam
                res_comment = action_comment(ui_instance)
                print(res_comment["message"])

            
            # 4. Copy link (Tăng tương tác ảo)
            if random.random() < 0.6:
                res_copy = action_coppy()
                print(res_copy["message"])
                
            
            # 5. Chuyển video
            res_down = action_down()
            print(res_down["message"])
            
            try_count = 0 
            time.sleep(random.uniform(3, 6))

        except Exception as e:
            
            print(f"⚠️ Lỗi phát sinh: {e}")
            action_down()
            try_count += 1
        if not running_flag: break
        time.sleep(random.uniform(3, 6))
    print("🛑 Bot đã dừng hoàn toàn.")

COMMENT_FILE = "my_comments.txt"

def save_comments_to_file(text):
    """Lưu nội dung từ ô nhập liệu vào file txt"""
    try:
        with open(COMMENT_FILE, "w", encoding="utf-8") as f:
            f.write(text.strip())
    except Exception as e:
        print(f"❌ Lỗi lưu file: {e}")

def load_comments_from_file():
    """Tải nội dung từ file txt, nếu không có thì dùng mặc định"""
    if os.path.exists(COMMENT_FILE):
        try:
            with open(COMMENT_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content: return content
        except Exception as e:
            print(f"❌ Lỗi đọc file: {e}")
    return DEFAULT_COMMENTS # Trả về mảng mặc định nếu file trống/lỗi
# ---------------- MAIN --------------------    
#  UI

# --- ĐƯỜNG DẪN ẢNH ---
IMAGE_DIR = "image"
IMAGE_CONFIG = {
    "HEART_IMG": {
        "path": os.path.join(IMAGE_DIR, "heart.png"),
        "label": "Nút Thả Tim",
        "desc": "Ảnh nút trái tim chưa bấm."
    },
    "FOLLOW_IMG": {
        "path": os.path.join(IMAGE_DIR, "follow.png"),
        "label": "Nút Follow",
        "desc": "Ảnh nút 'Follow' cộng đỏ trên avatar."
    },
    "COMMENT_IMG": {
        "path": os.path.join(IMAGE_DIR, "comment_box.png"),
        "label": "Ô Comment",
        "desc": "Ảnh 'Thêm bình luận' để click nhập liệu."
    },
    "COPPY_IMG": {
        "path": os.path.join(IMAGE_DIR, "copy.png"),
        "label": "Nút Copy Link",
        "desc": "Ảnh nút sao chép liên kết video."
    },
    "DOWN_IMG": {
        "path": os.path.join(IMAGE_DIR, "down.png"),
        "label": "Nút Next Video",
        "desc": "Ảnh nút mũi tên xuống trên video."
    },
    "NOT_FULL_SCREEN": {
        "path": os.path.join(IMAGE_DIR, "not_full.png"),
        "label": "Check FullScreen",
        "desc": "Ảnh một góc trình duyệt (để biết chưa nhấn F11)."
    }
}


class BotUI:
    def __init__(self, window):
        self.window = window
        self.window.title("TikTok Bot Config - Manager")
        self.window.geometry("1400x850") # Tăng chiều rộng để Log nhìn rõ hơn
        self.window.configure(bg="#f0f0f0")
        
        self.bot_thread = None
        self.is_running = False

        self.setup_ui()
        # Tải dữ liệu từ file vào ô nhập ngay khi mở App
        saved_text = load_comments_from_file()
        self.comment_input.delete("1.0", tk.END)
        self.comment_input.insert(tk.END, saved_text)
        
        # Chuyển hướng sys.stdout để in log vào GUI
        sys.stdout = self # Lát nữa ta định nghĩa hàm write
        messagebox.showinfo("Lưu ý nhỏ", "Khi chạy vui lòng cho chuột ra màn hình tiktok. Không để màn hình nào xuất hiện trước màn tiktok")

    def setup_ui(self):
        # --- TIÊU ĐỀ CHÍNH ---
        tk.Label(self.window, text="🚀 TIKTOK AUTOMATION CONTROL PANEL", 
                 font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(pady=15)

        # --- KHUNG CHÍNH CHỨA 2 CỘT ---
        main_container = tk.Frame(self.window, bg="#f0f0f0")
        main_container.pack(fill="both", expand=True, padx=20)

        # ================= CỘT TRÁI: SETUP ẢNH =================
        left_column = tk.LabelFrame(main_container, text="📸 Cấu Hình Hình Ảnh", 
                                    font=("Arial", 10, "bold"), bg="#f0f0f0", padx=10, pady=10)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        canvas = tk.Canvas(left_column, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(left_column, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg="#f0f0f0")

        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ================= CỘT PHẢI: COMMENT & LOG =================
        right_column = tk.Frame(main_container, bg="#f0f0f0")
        right_column.pack(side="right", fill="both", expand=True)

        # 1. Box nhập Comment
        comment_frame = tk.LabelFrame(right_column, text="💬 Danh Sách Comment (Mỗi câu 1 dòng)", 
                                      font=("Arial", 10, "bold"), bg="#f0f0f0", padx=10, pady=5)
        comment_frame.pack(fill="x", pady=(0, 10))
        
        self.comment_input = scrolledtext.ScrolledText(comment_frame, height=8, font=("Arial", 10), bd=2)
        self.comment_input.pack(fill="x")
        self.comment_input.insert(tk.END, DEFAULT_COMMENTS) # Chèn mảng mặc định vào

        # 2. Box Show Log
        log_frame = tk.LabelFrame(right_column, text="📜 Nhật Ký Hoạt Động (Logs)", 
                                  font=("Arial", 10, "bold"), bg="#f0f0f0", padx=10, pady=5)
        log_frame.pack(fill="both", expand=True)
        
        self.log_box = scrolledtext.ScrolledText(log_frame, font=("Consolas", 9), bg="#1e1e1e", fg="#00ff00")
        self.log_box.pack(fill="both", expand=True)

        # ================= DƯỚI CÙNG: NÚT ACTION =================
        action_frame = tk.Frame(self.window, bg="#f0f0f0", pady=20)
        action_frame.pack(fill="x")

        self.btn_run = tk.Button(action_frame, text="▶ CHẠY BOT", bg="#27ae60", fg="white", 
                                 font=("Arial", 11, "bold"), width=15, height=2, command=self.run_bot)
        self.btn_run.pack(side="left", padx=(250, 20))

        self.btn_stop = tk.Button(action_frame, text="⏹ DỪNG", bg="#e74c3c", fg="white", 
                                  font=("Arial", 11, "bold"), width=15, height=2, command=self.stop_bot, state="disabled")
        self.btn_stop.pack(side="left", padx=20)

        self.btn_restart = tk.Button(action_frame, text="🔄 CHẠY LẠI", bg="#f1c40f", fg="black", 
                                     font=("Arial", 11, "bold"), width=15, height=2, command=self.restart_bot)
        self.btn_restart.pack(side="left", padx=20)


        # Thêm một nút "Lưu Comment" thủ công nếu muốn (Tùy chọn)
        self.btn_save_cm = tk.Button(comment_frame, text="💾 Lưu danh sách", 
                                     command=self.manual_save, font=("Arial", 8))
        self.btn_save_cm.pack(pady=2)
        # Khởi tạo danh sách ảnh ban đầu
        self.refresh_images()

    # --- HÀM XỬ LÝ LOG ---
    def write(self, text):
        """Hàm này giúp hứng toàn bộ lệnh print() và đẩy vào log_box"""
        self.log_box.insert(tk.END, text)
        self.log_box.see(tk.END) # Tự động cuộn xuống dòng mới nhất

    def flush(self):
        pass # Bắt buộc phải có để giả lập stdout

    # --- ĐIỀU KHIỂN BOT ---
    def manual_save(self):
        content = self.comment_input.get("1.0", tk.END)
        save_comments_to_file(content)
        messagebox.showinfo("Thông báo", "Đã lưu danh sách comment vào file!")
    def run_bot(self):
        if not self.is_running:
            # 1. Lấy dữ liệu và lưu file trước
            content = self.comment_input.get("1.0", tk.END)
            save_comments_to_file(content)
            print("💾 Đã lưu cấu hình comment mới nhất.")

            # 2. Thay đổi trạng thái UI
            print("🚀 Đang khởi động Bot...")
            self.is_running = True
            self.btn_run.config(state="disabled", text="🤖 ĐANG CHẠY...")
            self.btn_stop.config(state="normal") # Đừng quên bật nút Stop lên nhé

            # 3. Chạy Bot
            self.bot_thread = threading.Thread(target=lambda: start_bot(self), daemon=True)
            self.bot_thread.start()
        else:
            messagebox.showwarning("Cảnh báo", "Bot đang chạy rồi!")
    def stop_bot(self):
        global running_flag
        running_flag = False
       
        print("⏹ Đang gửi lệnh dừng (Vui lòng đợi hết vòng lặp)...")
        self.btn_run.config(state="normal")
        self.btn_stop.config(state="disabled")

    def restart_bot(self):
        print("🔄 Đang yêu cầu khởi động lại...")
        # Lưu ý: PyAutoGUI khó dừng ngang xương, 
        self.stop_bot()
        self.window.after(2000, self.run_bot)
        # Cách đơn giản nhất là nhắc người dùng di chuyển chuột ra góc màn hình hoặc báo restart
        messagebox.showinfo("Thông báo", "Vui lòng đợi chu kỳ hiện tại kết thúc hoặc di chuyển chuột ra góc màn hình để dừng, sau đó nhấn Run lại.")
        # Thêm logic reset nếu start_bot của bạn có vòng lặp kiểm tra biến is_running

    def refresh_images(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for key, info in IMAGE_CONFIG.items():
            card = tk.Frame(self.scroll_frame, bg="white", bd=1, relief="groove", padx=10, pady=10)
            card.pack(fill="x", pady=5, padx=5)
            
            # Cấu hình để cột 1 (Mô tả) tự động dãn rộng ra
            card.grid_columnconfigure(1, weight=1)

            # Cột 0: Ảnh hiển thị (Cố định bên trái)
            img_path = info["path"]
            if os.path.exists(img_path):
                try:
                    raw_img = Image.open(img_path).resize((50, 50))
                    render_img = ImageTk.PhotoImage(raw_img)
                    lbl_img = tk.Label(card, image=render_img, bg="white")
                    lbl_img.image = render_img
                    lbl_img.grid(row=0, column=0, rowspan=2, padx=(0, 15)) # Thêm khoảng cách bên phải ảnh
                except:
                    tk.Label(card, text="Lỗi ảnh", fg="red", bg="white").grid(row=0, column=0, rowspan=2, padx=10)
            else:
                tk.Label(card, text="Thiếu ảnh", fg="gray", bg="white").grid(row=0, column=0, rowspan=2, padx=10)

            # Cột 1: Tiêu đề và Mô tả (Cột này sẽ dãn ra nhờ weight=1)
            tk.Label(card, text=info["label"], font=("Arial", 11, "bold"), bg="white", anchor="w").grid(row=0, column=1, sticky="w")
            tk.Label(card, text=info["desc"], font=("Arial", 9), fg="#666", bg="white", 
                     wraplength=250, justify="left").grid(row=1, column=1, sticky="w")

            # Cột 2: Nút bấm (Sát lề phải)
            tk.Button(card, 
                      text="Thay đổi", 
                      bg="#007bff", 
                      fg="white", 
                      font=("Arial", 9, "bold"),
                      relief="flat",
                      padx=10,
                      command=lambda p=img_path: self.change_image(p)).grid(row=0, column=2, rowspan=2, padx=5, sticky="e")

    def change_image(self, target_path):
        new_file = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
        if new_file:
            try:
                if not os.path.exists(IMAGE_DIR):
                    os.makedirs(IMAGE_DIR)
                
                # Copy đè lên file cũ (shutil.copy tự động ghi đè)
                shutil.copy(new_file, target_path)
                messagebox.showinfo("Thành công", f"Đã cập nhật: {os.path.basename(target_path)}")
                self.refresh_images()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu ảnh: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BotUI(root)
    root.mainloop()
# Khởi chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = BotUI(root)
    root.mainloop()