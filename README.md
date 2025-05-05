 SPADE Sequential Pattern Mining Application

📚 Giới thiệu

Ứng dụng này được xây dựng nhằm "Khai phá các mẫu tuần tự phổ biến" từ tập dữ liệu giao dịch khách hàng, sử dụng *thuật toán SPADE* (Sequential Pattern Discovery using Equivalence classes).
Dự án nhằm mục tiêu hỗ trợ phân tích hành vi tiêu dùng, gợi ý sản phẩm, và tối ưu hóa hoạt động kinh doanh.

Các chức năng chính bao gồm:

* Tiền xử lý và làm sạch dữ liệu giao dịch.
* Chạy thuật toán SPADE để phát hiện các mẫu tuần tự phổ biến.
* Hiển thị kết quả khai phá dưới dạng danh sách và biểu đồ trực quan.
* Gợi ý sản phẩm dựa trên hành vi mua sắm tuần tự.

---

🛠️ Công nghệ sử dụng

* Python 3.8+
* Tkinter (giao diện người dùng)
* Pandas (xử lý dữ liệu)
* Matplotlib, Seaborn (vẽ biểu đồ)
* SPADE Algorithm (cài đặt từ đầu)

---

📦 Cài đặt

1. Clone hoặc tải về mã nguồn:

git clone https://github.com/but0401/DoAn.git



2. Cài đặt các thư viện cần thiết:

pip install pandas matplotlib seaborn

 🚀 Cách sử dụng

1. Chạy ứng dụng:

```
python main.py
```

2. Các bước thao tác trong ứng dụng:

* **Import Data**: Tải file CSV 'sample_data.csv' dữ liệu giao dịch.
* **Clean Data**: Làm sạch dữ liệu (xử lý missing values, trùng lặp, chuẩn hóa thời gian).
* **Run SPADE Algorithm**: Cấu hình tham số `Minimum Support`, chạy khai phá mẫu tuần tự.
* **View Frequent Patterns**: Xem danh sách mẫu tuần tự được khai phá.
* **Statistics**: Phân tích tổng quan số lượng sản phẩm, khách hàng, đơn hàng.
* **Visualizations**: Xem biểu đồ phân phối sản phẩm, khách hàng, thời gian giao dịch.
* **Recommendations**: Gợi ý sản phẩm tiếp theo dựa trên mẫu tuần tự phổ biến.

---

📊 Giao diện mẫu

* Import dữ liệu, xử lý dữ liệu, và hiển thị thống kê tổng quan.
* Trực quan hóa Top 10 sản phẩm bán chạy, xu hướng mua hàng theo thời gian.
* Xem danh sách mẫu tuần tự cùng độ hỗ trợ (`support`) chi tiết.

---

📈 Tính năng nổi bật

* Triển khai thuật toán SPADE tối ưu hóa bằng vertical id-list.
* Điều chỉnh linh hoạt ngưỡng `Minimum Support`.
* Giao diện thân thiện, dễ sử dụng cho người không chuyên về kỹ thuật.
* Hỗ trợ phân tích hành vi khách hàng, gợi ý bán hàng thông minh.

---

📌 Ghi chú

* Dữ liệu mẫu (`sample_data.csv`) đã được cung cấp kèm dự án.
* Hệ thống phù hợp để thử nghiệm với các tập dữ liệu nhỏ đến trung bình (vài ngàn dòng).
* Để xử lý dữ liệu lớn (hàng triệu dòng), cần tối ưu thuật toán hoặc triển khai phân tán.

---

🎯 Cảm ơn!

Cảm ơn thầy đã theo dõi và đánh giá đề tài!

---
