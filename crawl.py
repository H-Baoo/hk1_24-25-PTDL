import cloudscraper
from bs4 import BeautifulSoup
import urllib3
import time
import csv

# Bỏ qua cảnh báo không an toàn
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Tạo scraper với headers giả lập trình duyệt
scraper = cloudscraper.create_scraper()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Hàm lấy thông tin công ty
def get_company_info(soup):
    company_info = {}
    tax_tag = soup.find("td", itemprop="taxID")
    company_info["Số ĐKKD/MST"] = tax_tag.get_text(strip=True) if tax_tag else "N/A"
    name_tag = soup.find("th", itemprop="name")
    company_info["Tên công ty"] = name_tag.get_text(strip=True) if name_tag else "N/A"
    address_tag = soup.find("td", itemprop="address")
    company_info["Địa chỉ"] = address_tag.get_text(strip=True) if address_tag else "N/A"
    established_date_tag = soup.find("td", itemprop="IncorporatedDate")
    company_info["Ngày thành lập"] = established_date_tag.get_text(strip=True) if established_date_tag else "N/A"
    operationDay_tag = soup.find("td", itemprop="StartDate")
    company_info["Ngày hoạt động"] = operationDay_tag.get_text(strip=True) if operationDay_tag else "N/A"
    status_tag = soup.find("td", itemprop="Status")
    company_info["Trạng thái"] = status_tag.get_text(strip=True) if status_tag else "N/A"
    phone_tag = soup.find("td", itemprop="Phone")
    company_info["Điện thoại"] = phone_tag.get_text(strip=True) if phone_tag else "N/A"
    representative_tag = soup.find("span", itemprop="Owner")
    company_info["Người đại diện"] = representative_tag.get_text(strip=True) if representative_tag else "N/A"
    type_of_business_tag = soup.find("td", itemprop="BusinessClass")
    company_info["Loại hình DN"] = type_of_business_tag.get_text(strip=True) if type_of_business_tag else "N/A"
    last_updated_tag = soup.find("td", colspan="2")
    company_info["Cập nhật lần cuối"] = last_updated_tag.get_text(strip=True) if last_updated_tag else "N/A"
    return company_info

# Hàm ghi thông tin công ty ra file CSV
def write_to_csv(company_info, file_name):
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Ghi dữ liệu ra CSV
        writer.writerow([
            company_info.get("Số ĐKKD/MST", "N/A"),
            company_info.get("Tên công ty", "N/A"),
            company_info.get("Địa chỉ", "N/A"),
            company_info.get("Ngày thành lập", "N/A"),
            company_info.get("Ngày hoạt động", "N/A"),
            company_info.get("Trạng thái", "N/A"),
            company_info.get("Điện thoại", "N/A"),
            company_info.get("Người đại diện", "N/A"),
            company_info.get("Loại hình DN", "N/A"),
            company_info.get("Cập nhật lần cuối", "N/A")
        ])

# Tạo file CSV và ghi tiêu đề
file_name = 'company_info.csv'
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Ghi dòng tiêu đề
    writer.writerow([
        "Số ĐKKD/MST", "Tên công ty", "Địa chỉ", "Ngày thành lập", 
        "Ngày hoạt động", "Trạng thái", "Điện thoại", 
        "Người đại diện", "Loại hình DN", "Cập nhật lần cuối"
    ])

# Vòng lặp qua các trang
for page_number in range(1, 50):  # Thay số 5 bằng số trang bạn muốn duyệt qua
    url = f"https://doanhnghiep.biz/dia-diem/long-an/huyen-ben-luc-80117/?p={page_number}"
    response = scraper.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Bỏ qua các popup hoặc modal nếu có
    popup = soup.find('div', class_='popup-class')  # Thay thế bằng class thực tế của popup
    if popup:
        popup.decompose()  # Loại bỏ popup này khỏi nội dung HTML

    # Lấy các link công ty từ trang hiện tại
    links_elements = soup.find_all('h6')
    links = []
    for link in links_elements:
        a_tag = link.find_next('a')
        if a_tag:
            href = a_tag.get('href')
            if href:  
                links.append(href)
    
    # Duyệt qua các link công ty để lấy thông tin chi tiết
    for link in links:
        full_link = "https://doanhnghiep.biz" + link
        try:
            responseLink = scraper.get(full_link, headers=headers)
            soup = BeautifulSoup(responseLink.content, "html.parser")
            company_info = get_company_info(soup)

            # Ghi thông tin công ty vào file CSV
            write_to_csv(company_info, file_name)

        except Exception as e:
            print(f"Lỗi khi cào link {full_link}: {e}")
        
        # Nghỉ giữa các yêu cầu để tránh bị khóa IP
        time.sleep(5)  # Nghỉ 5 giây giữa mỗi yêu cầu
        
    # Nghỉ giữa các trang để tránh bị khóa IP
    time.sleep(10)  # Nghỉ 10 giây giữa các trang
