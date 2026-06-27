# Dịch Khi Bôi Đen — Công cụ dịch nhanh trên Windows

Một công cụ desktop nhẹ cho Windows: bôi đen bất kỳ đoạn văn bản nào, nhấn phím tắt, và một cửa sổ nổi sẽ hiện ra hiển thị kết quả dịch.

## 📸 Xem trước

![Xem trước kết quả dịch](images/screenshot-20260625-165441.png)

![Xem trước giao diện cài đặt](images/screenshot-20260625-161049.png)

## ✨ Tính năng

- 🌐 **Dịch một chạm** — Bôi đen văn bản, nhấn phím tắt là dịch ngay
- ⌨️ **Phím tắt tùy chỉnh** — Hỗ trợ tự đặt phím tắt dịch qua menu khay hệ thống
- 🔄 **Dịch sang tiếng Việt** — Mọi ngôn ngữ đầu vào đều được dịch sang tiếng Việt
- 🔌 **Hoạt động ngoại tuyến** — Dùng mô hình Tencent Hy-MT2-1.8B, sau khi tải về không cần mạng
- ⚡ **Hiệu năng cao** — Dựa trên engine suy luận llama.cpp, tăng tốc đa luồng CPU
- 🎨 **Giao diện hiện đại** — Cửa sổ nổi tối bán trong suốt, phong cách kính mờ
- 📌 **Khay hệ thống** — Chạy nền thường trực, không chiếm chỗ trên thanh tác vụ
- 📋 **Sao chép một chạm** — Kết quả dịch sao chép vào clipboard chỉ với một nút
- 🖱️ **Định vị thông minh** — Cửa sổ dịch tự bám theo vị trí con trỏ chuột
- 📏 **Chiều cao thích ứng** — Cửa sổ dịch tự điều chỉnh chiều cao theo nội dung, có thanh cuộn
- 🔒 **Chống mở trùng** — Ngăn chạy nhiều bản, tự nhắc khi mở lại

## 🛠️ Công nghệ sử dụng

| Thành phần     | Công nghệ                            | Mô tả                            |
| -------------- | ------------------------------------ | -------------------------------- |
| Engine dịch    | llama-cpp-python + Hy-MT2-1.8B-GGUF  | Mô hình dịch chất lượng cao      |
| Khung GUI      | tkinter                              | GUI đa nền tảng, nhẹ             |
| Lắng nghe phím | pynput                               | Bắt phím tắt toàn cục            |
| Khay hệ thống  | pystray                              | Quản lý biểu tượng khay hệ thống |
| Clipboard      | pyperclip                            | Đọc/ghi clipboard                |
| Xử lý ảnh      | Pillow                               | Sinh biểu tượng khay             |
| Tải mô hình    | huggingface_hub                      | Tải mô hình từ HuggingFace       |

## 📦 Cài đặt

### 1. Cài đặt phụ thuộc Python

```bash
pip install -r requirements.txt
```

**Lưu ý**: `llama-cpp-python` có thể cần môi trường biên dịch C++. Nếu cài đặt thất bại, hãy tham khảo hướng dẫn bên dưới:

#### Cài llama-cpp-python trên Windows

**Cách 1: Dùng wheel biên dịch sẵn (khuyến nghị)**

```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

**Cách 2: Biên dịch từ mã nguồn**

1. Cài Visual Studio Build Tools (gồm trình biên dịch C++)
2. Hoặc cài MinGW-w64
3. Sau đó chạy: `pip install llama-cpp-python`

### 2. Lần chạy đầu tiên (tải mô hình)

Lần khởi động đầu tiên sẽ tự động tải mô hình Hy-MT2-1.8B GGUF (khoảng 1.13GB), cần kết nối mạng.
Sau khi tải xong là có thể dùng ngoại tuyến.

```bash
python main.py
```

## 🚀 Cách dùng

1. Chạy `python main.py`, công cụ sẽ thu nhỏ xuống khay hệ thống
2. **Bôi đen văn bản** trong bất kỳ ứng dụng nào
3. Nhấn phím tắt mặc định `Ctrl+Alt+Q` (có thể tùy chỉnh)
4. Kết quả dịch sẽ hiện ra trong cửa sổ nổi gần con trỏ chuột

### Thao tác nhanh

| Thao tác                 | Mô tả                                              |
| ------------------------ | -------------------------------------------------- |
| `Ctrl+Alt+Q`             | Dịch văn bản đã bôi đen (mặc định, tùy chỉnh được) |
| `Esc`                    | Đóng cửa sổ dịch                                   |
| Nhấp ra ngoài cửa sổ     | Đóng cửa sổ dịch                                   |
| Kéo thanh tiêu đề        | Di chuyển cửa sổ dịch                              |
| Nhấp "Sao chép bản dịch" | Sao chép kết quả dịch vào clipboard                |

### Tùy chỉnh phím tắt

1. Nhấp chuột phải vào biểu tượng khay hệ thống
2. Chọn "Cài đặt phím tắt"
3. Trong cửa sổ cài đặt hiện ra, nhấn tổ hợp phím tắt mới (ví dụ `Ctrl+Shift+T`)
4. Nhấp nút "Lưu", phím tắt có hiệu lực ngay
5. Cài đặt được tự động lưu, lần khởi động sau sẽ tự nạp lại

## 🏗️ Cấu trúc dự án

```
translate-plugin/
├── main.py              # Điểm khởi chạy chính, điều phối các module
├── translator.py        # Bao bọc engine dịch Hy-MT2 (llama.cpp)
├── hotkey_manager.py    # Quản lý phím tắt toàn cục
├── popup_window.py      # Cửa sổ dịch nổi (tkinter)
├── tray_icon.py         # Biểu tượng khay hệ thống (pystray)
├── config_manager.py    # Quản lý cấu hình (lưu cài đặt phím tắt)
├── settings_window.py   # Hộp thoại cài đặt phím tắt
├── models/              # Thư mục lưu mô hình (tự tạo)
├── settings.json        # Tệp cấu hình người dùng (tự sinh)
├── requirements.txt     # Phụ thuộc Python
├── test_llama_cpp.py    # Script kiểm thử tích hợp llama.cpp
└── README.md            # Tài liệu dự án
```

## 🔧 Kiểm thử

Chạy script kiểm thử để xác minh tích hợp llama.cpp:

```bash
python test_llama_cpp.py
```

## ⚠️ Lưu ý

- Cần **Python 3.10+**
- Thư viện `pynput` trong một số trường hợp có thể cần **quyền quản trị** để bắt phím tắt toàn cục
- Lần chạy đầu cần mạng để tải mô hình Hy-MT2-1.8B GGUF (khoảng 1.13GB)
- Chất lượng dịch dựa trên mô hình Tencent Hy-MT2-1.8B
- Mô hình dùng lượng tử hóa Q4_K_M, vừa đảm bảo chất lượng vừa giảm dung lượng bộ nhớ
- Mặc định suy luận đa luồng CPU, không cần GPU
- Cài đặt phím tắt tùy chỉnh được tự lưu vào tệp `settings.json`
- Đã tối ưu hỗ trợ màn hình DPI cao, chữ hiển thị rõ và kích thước phù hợp

## 📊 Thông tin mô hình

| Thuộc tính        | Giá trị                |
| ----------------- | ---------------------- |
| Tên mô hình       | Tencent Hy-MT2-1.8B    |
| Định dạng mô hình | GGUF (lượng tử Q4_K_M) |
| Kích thước        | Khoảng 1.13GB          |
| Engine suy luận   | llama.cpp              |
| Cách tăng tốc     | Đa luồng CPU           |
| Cửa sổ ngữ cảnh   | 4096 tokens            |

## 🐛 Khắc phục sự cố

### 1. Cài llama-cpp-python thất bại

**Vấn đề**: `pip install llama-cpp-python` báo lỗi
**Giải pháp**:

- Dùng wheel biên dịch sẵn (khuyến nghị):
  ```bash
  pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
  ```
- Hoặc cài Visual Studio Build Tools rồi cài lại

### 2. Tải mô hình thất bại

**Vấn đề**: Lần chạy đầu tải mô hình thất bại
**Giải pháp**:

- Kiểm tra kết nối mạng
- Thử dùng máy chủ gương HuggingFace:
  ```bash
  set HF_ENDPOINT=https://hf-mirror.com
  python main.py
  ```
- Hoặc tải thủ công tệp mô hình vào thư mục `models/Hy-MT2-1.8B-GGUF/`

### 3. Dịch chậm

**Vấn đề**: Thời gian phản hồi dịch quá lâu
**Giải pháp**:

- Đảm bảo dùng đa luồng CPU (mặc định bật)
- Kiểm tra mức sử dụng CPU của hệ thống, tắt các chương trình khác đang chiếm CPU
- Cân nhắc dùng phiên bản lượng tử nhỏ hơn (như Q2_K)

### 4. Phím tắt không phản hồi

**Vấn đề**: Nhấn phím tắt không có gì xảy ra
**Giải pháp**:

- Chạy chương trình với quyền quản trị
- Kiểm tra xem có phần mềm khác đang chiếm cùng phím tắt không
- Đặt lại phím tắt qua menu khay hệ thống
- Xem tệp log `translate.log` để biết chi tiết

### 5. Kết quả dịch trống

**Vấn đề**: Cửa sổ dịch hiện ra nhưng không có kết quả
**Giải pháp**:

- Kiểm tra xem văn bản đã bôi đen có hợp lệ không
- Xem tệp log `translate.log` để biết thông tin lỗi
- Thử khởi động lại chương trình

### 6. Báo chương trình đã chạy

**Vấn đề**: Khi khởi động báo "Chương trình đang chạy!"
**Giải pháp**:

- Kiểm tra khu vực khay hệ thống xem có biểu tượng công cụ dịch không
- Nếu cần khởi động lại, hãy chuột phải biểu tượng khay rồi chọn "Thoát"
- Hoặc dùng Trình quản lý tác vụ kết thúc tiến trình rồi khởi động lại

## 📝 Ghi chú phát triển

### Các module cốt lõi

1. **translator.py** - Engine dịch
   - Dùng `llama-cpp-python` để nạp mô hình GGUF
   - Hỗ trợ tự động tải mô hình (qua `huggingface_hub`)
   - Cung cấp giao diện dịch đồng bộ và bất đồng bộ
   - Dịch mọi ngôn ngữ đầu vào sang tiếng Việt

2. **hotkey_manager.py** - Quản lý phím tắt
   - Dùng `pynput` lắng nghe phím tắt toàn cục
   - Lấy văn bản đã bôi đen bằng cách giả lập Ctrl+C
   - Hỗ trợ phím tắt tùy chỉnh

3. **popup_window.py** - Cửa sổ nổi
   - Dùng `tkinter` tạo cửa sổ không viền
   - Hỗ trợ hiệu ứng mờ dần và tự định vị
   - Chủ đề tối, phong cách giao diện hiện đại

4. **tray_icon.py** - Khay hệ thống
   - Dùng `pystray` quản lý biểu tượng khay hệ thống
   - Hiển thị trạng thái dịch và thông tin phím tắt
   - Cung cấp menu cài đặt phím tắt và thoát

5. **config_manager.py** - Quản lý cấu hình
   - Quản lý cấu hình người dùng (phím tắt, v.v.)
   - Lưu cấu hình vào `settings.json`
   - Hỗ trợ gộp cấu hình mặc định và cấu hình người dùng

6. **settings_window.py** - Cửa sổ cài đặt
   - Hộp thoại cài đặt phím tắt
   - Hỗ trợ bắt phím nhập theo thời gian thực
   - Chủ đề tối, đồng bộ phong cách với giao diện chính

### Tham số cấu hình

Các tham số dịch có thể chỉnh trong `translator.py`:

```python
GENERATION_CONFIG = {
    "temperature": 0.7,      # Nhiệt độ sinh
    "top_p": 0.6,           # Tham số lấy mẫu nhân
    "top_k": 20,            # Lấy mẫu Top-K
    "repeat_penalty": 1.05, # Phạt lặp lại
    "max_tokens": 4096,     # Độ dài sinh tối đa
}
```

Cấu hình người dùng được lưu trong tệp `settings.json`:

```json
{
  "hotkey": "<ctrl>+<shift>+t",
  "hotkey_display": "Ctrl+Shift+T"
}
```

### Mở rộng phát triển

Nếu cần thêm hỗ trợ ngôn ngữ khác:

1. Tải mô hình GGUF tương ứng
2. Sửa `MODEL_ID` và `MODEL_FILENAME` trong `translator.py`
3. Cập nhật `PROMPT_TEMPLATE` để hỗ trợ cặp ngôn ngữ mới

## 📄 Giấy phép

Dự án này dùng giấy phép MIT. Xem chi tiết tại tệp [LICENSE](LICENSE).

## 🙏 Lời cảm ơn

- [llama.cpp](https://github.com/ggerganov/llama.cpp) - Engine suy luận LLM hiệu năng cao
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) - Python binding
- [Tencent Hy-MT2](https://huggingface.co/tencent/Hy-MT2-1.8B-GGUF) - Mô hình dịch
- [pynput](https://github.com/moses-palmer/pynput) - Giám sát đầu vào đa nền tảng
- [pystray](https://github.com/moses-palmer/pystray) - Thư viện biểu tượng khay hệ thống
