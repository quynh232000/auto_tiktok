pyinstaller --noconsole --onefile --icon=app.ico main.py


pyinstaller --noconsole --onefile --add-data "image;image" --icon=favicon.ico main.py
<!-- ============ -->
--noconsole (hoặc -w): Ẩn cửa sổ CMD đen khi mở app (vì bạn đã có giao diện UI rồi).

--onefile (hoặc -F): Đóng gói tất cả thành 1 file .exe duy nhất trong thư mục dist.

--icon=app_icon.ico: Tạo icon cho file exe (bỏ qua nếu không có).

--add-data "image;image": Đưa thư mục ảnh vào trong file exe.