# Đường dẫn tới file txt đầu vào và file txt đầu ra
input_file = "link_movie_mojo.txt"
output_file = "link_sach.txt"

# Tạo một set để lưu các dòng duy nhất từ file đầu vào
unique_lines = set()

# Đọc từng dòng từ file đầu vào và thêm vào set
with open(input_file, "r") as file:
    for line in file:
        unique_lines.add(line.strip())

# Ghi các dòng duy nhất vào file đầu ra
with open(output_file, "w") as file:
    for line in unique_lines:
        file.write(line + "\n")