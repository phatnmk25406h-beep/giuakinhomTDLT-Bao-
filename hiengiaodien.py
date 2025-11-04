import pandas as pd
import random
import sys
from docchu import *
from PyQt6.QtWidgets import QApplication, QWidget
from tuvungqt6 import *  # Giao diện bạn đã thiết kế sẵn bằng Qt Designer

# --- File dùng để lưu tiến độ học---
TIEN_DO_FILE = "tien_do.xlsx"
list_of_lists = []
D = 0
T = 0
randomlist = []
# ===== HÀM 1: ĐÁNH GIÁ KẾT QUẢ HỌC ======================================
def danhgia(D, T):
    if T == 0:
        return "Chưa có dữ liệu để đánh giá."
    ti_le_dung=round(D/T, 2) *100
    if ti_le_dung <= 0.25:
        k = f"""Tỉ lệ đúng: {ti_le_dung} %
          Bạn mất gốc rồi 😭 
        Ngày mai ôn lại liền nha."""
    elif ti_le_dung <= 0.5:
        k = f"""Tỉ lệ đúng: {ti_le_dung} %
                Bạn thuộc ít quá 😅 
               2 ngày sau ôn lại nhé."""
    elif ti_le_dung <= 0.65:
        k = f"""Tỉ lệ đúng: {ti_le_dung}%
           Bạn chưa thuộc lắm 🤔 
             3 ngày sau ôn lại nhé."""
    elif ti_le_dung <= 0.8:
        k = f"""Tỉ lệ đúng: {ti_le_dung}%
              Tạm ổn rồi 😌 
             4 ngày sau ôn lại nhé."""
    else:
        k = f"""Tỉ lệ đúng: {ti_le_dung}%
            Xuất sắc 🎉 
              Tuần sau ôn lại nhé!"""
    return k


# ===== HÀM 2: BẮT ĐẦU HỌC  ==============
def bat_dau_hoc():
    global list_of_lists, D, T, randomlist
    try:
        a = form.lnenhapfile.text().strip()
        if a == "":
            form.lnetienganh.setText(" Vui lòng nhập đường dẫn file Excel!")
            return
        # Đọc dữ liệu
        DataFrame = pd.read_excel(a)
        list_of_lists = DataFrame.values.tolist()
        D = 0
        T = 0
        form.txtlannhapdung.setText(f"{D} / {T}")
        hien_tu_hoc()
    except FileNotFoundError:
        form.lnetienganh.setText("Không tìm thấy file! Hãy nhập lại chính xác nhé")
    except Exception as e:
        form.lnetienganh.setText(f"Lỗi: {e}")
# ===== HÀM 3: HIỂN THỊ TỪ MỚI  ======================================
def hien_tu_hoc():
    global list_of_lists, randomlist
    if len(list_of_lists) > 0:
        randomlist = random.choice(list_of_lists)
        form.lnetienganh.setText(randomlist[0])
        form.lnetiengviet.setText("")  # xóa ô nhập nghĩa cũ
    else:
        # ---  KHI HỌC XONG ---
        form.lnetienganh.setText(""" HOÀN THÀNH!""")
        form.lnetiengviet.setText("Bạn đã học hết các từ trong file này!")
        k = danhgia(D, T)
        chiGoogle(k)
        form.txtloikhuyen.setText(k)  # Hiển thị đánh giá
# ===== HÀM 4: KIỂM TRA ĐÁP ÁN (CẬP NHẬT) ======================================
def kiem_tra_dap_an():
    global randomlist, D, T, list_of_lists
    try:
        b = form.lnetiengviet.text().strip()
        T += 1
        if b.lower().strip() == randomlist[1].lower().strip():  # lower: viết thường, strip() bỏ khoảng trắng
            list_of_lists.remove(randomlist)
            D += 1
        else:  # Trả lời SAI
            form.txtloikhuyen.setText(f" Sai rồi! Đáp án đúng là: {randomlist[1]}")
            chiGoogle(f" Sai rồi! Đáp án đúng là: {randomlist[1]}")
            luu_tien_do_tu(randomlist[0], randomlist[1]) #sai thì mới lưu từ
        #luu tu
        # randomlist[0]:tu tieng anh, randomlist[1]
        form.txtlannhapdung.setText(f"{D} / {T}")
        # Cập nhật tỉ lệ
        ti_le = (D / T) * 100
        form.progress_tiledungsai.setValue(int(ti_le))
        # Hiện từ mới
        hien_tu_hoc()
    except Exception as e:
        form.txtloikhuyen.setText(f"Lỗi khi kiểm tra: {e}")
# ===== HÀM 5: LƯU TIẾN ĐỘ TỪ  =================================
def luu_tien_do_tu(tu_av, tu_tv):
    # 1. Tạo "dòng mới" (record) dưới dạng dictionary
    record=(tu_av, tu_tv)

    # 2. Tạo một danh sách rỗng để chứa tất cả dữ liệu
    list_of_lists_on_bai = []
    try:
        # 4. Nếu CÓ: Đọc file Excel tiendo_file đã khai báo ở đầu
        list_of_lists_on_bai = pd.read_excel(TIEN_DO_FILE).values.tolist()

        # 5. Thêm "dòng mới" (record_moi) vào cuối danh sách
        list_of_lists_on_bai.append(record)
        # 6. Tạo lại 1 file excel ảo (dataframe) vừa mới cập nhật record
        DataFrame_tiendo = pd.DataFrame(list_of_lists_on_bai)

        # 7. Ghi đè file Excel bằng bảng tổng hợp này
        DataFrame_tiendo.to_excel(TIEN_DO_FILE, index=False)

    except Exception as e:
        form.txtloikhuyen.setText(f"Lỗi: Không thể lưu tiến độ: {e}")


# ===== HÀM 6: ÔN LẠI TỪ SAI (CẬP NHẬT) =====================
def on_lai_tu_sai():
    global T, D, list_of_lists
    try:
        # Đọc toàn bộ file tiến độ
        list_of_lists = pd.read_excel(TIEN_DO_FILE).values.tolist()
        # --- DỌN DẸP FILE NGAY LẬP TỨC ---
        don_dep_toan_bo_file()  # Gọi hàm dọn dẹp
        # Kiểm tra xem có từ sai nào không
        if len(list_of_lists) == 0:
            form.txtloikhuyen.setText("🎉 Không còn từ sai để ôn lại!")
            return
        # Reset điểm và bắt đầu học
        D = 0
        T = 0
        form.progress_tiledungsai.setValue(0)
        form.txtlannhapdung.setText(f"{D} / {T}")
        form.txtloikhuyen.setText(" Bắt đầu ôn lại các từ sai nhé!")
        hien_tu_hoc()

    except Exception as e:
        form.txtloikhuyen.setText(f"Lỗi khi ôn lại: {e}")


# ===== HÀM 7: DỌN DẸP TOÀN BỘ FILE TIẾN ĐỘ (HÀM MỚI) =====
def don_dep_toan_bo_file():
    """
    Hàm này GHI ĐÈ file tien_do.xlsx bằng một file TRẮNG RỖNG
    Nó sẽ xóa sạch toàn bộ lịch sử học cũ.
    """
    try:
        # 1. Tạo 1 DataFrame (bảng) rỗng với 3 cột
        tiendo_rong = pd.DataFrame()

        # 2. Ghi đè file trống tiendo_rong. File cũ sẽ bị xóa sạch nội dung.
        tiendo_rong.to_excel(TIEN_DO_FILE, index=False)
    except Exception as e:
        form.txtloikhuyen.setText(f"Lỗi khi dọn dẹp file: {e}")


# ===== PHẦN KHỞI TẠO CHÍNH ======================================
app = QApplication(sys.argv)
window = QWidget()
form = Ui_Form()
form.setupUi(window)

# Kết nối các nút
form.btnbatdauhoc.clicked.connect(bat_dau_hoc)
form.btnsubmit.clicked.connect(kiem_tra_dap_an)
form.btn_hoclai.clicked.connect(on_lai_tu_sai)
window.show()
app.exec()