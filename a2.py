import pandas as pd
from pymongo import MongoClient

# Bước 1: Đọc file CSV
csv_file_path = 'C:/Users/Admin/DoanhNghiep/hk1_24-25-PTDL/company_info.csv'  # Đường dẫn đầy đủ trên máy tính của bạn
df = pd.read_csv(csv_file_path)

# Bước 2: Kết nối đến MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Thay thế bằng URL MongoDB nếu cần
db = client["dbmycrawler"]  # Sử dụng cơ sở dữ liệu dbmycrawler
collection = db["company_info"]  # Tên collection (bảng) trong cơ sở dữ liệu

# Bước 3: Chuyển dữ liệu từ DataFrame sang dictionary và chèn vào MongoDB
data_dict = df.to_dict("records")  # Chuyển DataFrame thành danh sách các dictionary
collection.insert_many(data_dict)  # Chèn nhiều document vào MongoDB

print("Dữ liệu đã được đưa vào MongoDB trong cơ sở dữ liệu 'dbmycrawler'!")
