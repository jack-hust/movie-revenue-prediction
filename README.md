# 2023.2-Data-Science

Phân tích và dự đoán doanh thu phim chiếu rạp

## Bắt đầu

Hướng dẫn này sẽ giúp bạn thiết lập và chạy dự án trên máy tính của mình để phát triển và thử nghiệm.

### Điều kiện tiên quyết

Những gì bạn cần cài đặt để phần mềm hoạt động:

- [Python 3.x](https://www.python.org/)
- Các thư viện Python cần thiết (liệt kê trong `requirements.txt`)

### Cài đặt
1. Cài đặt các thư viện cần thiết

    ```sh
    pip install -r requirements.txt
    ```

## Chạy chương trình

1. Di chuyển vào thư mục `app`

    ```sh
    cd app
    ```

2. Chạy chương trình

    - Nếu bạn sử dụng Ubuntu:

        ```sh
        python3 app.py
        ```

    - Nếu bạn sử dụng Windows:

        ```sh
        py app.py
        ```

3. Truy cập vào đường dẫn [http://127.0.0.1:5000/](http://127.0.0.1:5000/) để trải nghiệm

## Tính năng cập nhật dữ liệu chạy trên server

Trước tiên cần chạy Runners action local bằng cách liên hệ với chủ repo `QuanTH02`. Khi đã có folder `actions-runner`, thực hiện các bước sau:

1. Di chuyển vào thư mục `actions-runner`

    ```sh
    cd actions-runner
    ```

2. Chạy lệnh

    ```sh
    ./run.cmd
    ```

Lúc này hệ thống đã chạy và sẽ cập nhật dữ liệu liên tục mỗi tháng một lần.

## Phân tích tác dụng của từng folder/file

- **plot.ipynb**: Vẽ biểu đồ phân tích dữ liệu
- **EFA.ipynb**: Phân tích yếu tố tiềm ẩn để giảm chiều dữ liệu
- **feature_selection.py**: Train các model và dump vào các file pkl
- **predict_with_efa.py**: Dự đoán
- **update_model.py**: Chạy tự động mỗi tháng để cập nhật model
- **Folder main**: Chạy tự động mỗi tháng
- **Các folder còn lại**: Crawl dữ liệu