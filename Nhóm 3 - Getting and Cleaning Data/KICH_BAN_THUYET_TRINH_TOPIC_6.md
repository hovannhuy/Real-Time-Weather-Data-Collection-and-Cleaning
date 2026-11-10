# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN CUỐI KỲ (BILINGUAL PRESENTATION SCRIPT)
## MÔN HỌC: THU THẬP VÀ TIỀN XỬ LÝ DỮ LIỆU (GETTING AND CLEANING DATA - 261.DAS1204E.A01E)
### ĐỀ TÀI TOPIC 6: THU THẬP VÀ LÀM SẠCH DỮ LIỆU THỜI TIẾT THỜI GIAN THỰC
### (REAL-TIME WEATHER DATA COLLECTION AND CLEANING ACROSS 20 VIETNAM CITIES)

---

## MỤC LỤC TỔNG QUAN (TABLE OF CONTENTS)
1. [Thông tin Đồ án & Phân công Diễn giả](#1-thông-tin-đồ-án--phân-công-diễn-giả)
2. [PHẦN 1: KỊCH BẢN THUYẾT TRÌNH BẰNG TIẾNG VIỆT (SLIDES 01 – 21)](#phần-1-kịch-bản-thuyết-trình-bằng-tiếng-việt-slides-01--21)
3. [PHẦN 2: ENGLISH PRESENTATION SCRIPT (SLIDES 01 – 21)](#phần-2-english-presentation-script-slides-01--21)
4. [PHẦN 3: CÂU HỎI PHẢN BIỆN DỰ PHÒNG & HƯỚNG DẪN TRẢ LỜI (DEFENSE Q&A CHEAT SHEET)](#phần-3-câu-hỏi-phản-biện-dự-phòng--hướng-dẫn-trả-lời-defense-qa-cheat-sheet)

---

## 1. THÔNG TIN ĐỒ ÁN & PHÂN CÔNG DIỄN GIẢ

| Vai trò | Thành viên | Mã số sinh viên (MSSV) | Phụ trách thuyết trình trên Slide |
| :--- | :--- | :---: | :--- |
| **Diễn giả 1 (Speaker 1)** | **Nguyễn Dạ Giao Đăng** | `235210195` | **Mở đầu & Phần 1 (Slides 01 – 06)**: Giới thiệu đề tài, kiến trúc thu thập đa nguồn từ 4 APIs / 5 nhóm endpoint, phạm vi 20 trạm/thành phố thuộc 7 vùng khí hậu, cấu trúc schema (22 thô -> 31 sạch), và kiểm toán định lượng 9 loại lỗi trong 49.109 dòng thô. |
| **Diễn giả 2 (Speaker 2)** | **Hồ Văn Như Ý** | `245191885` | **Phần 2 (Slides 07 – 12)**: Tổng quan đường ống 9 bước tiền xử lý (-4.569 dòng rác), kiểm toán phản hồi thiếu (89/100 OK), chuẩn hóa thời gian UTC+7 & cắt 995 dòng dự báo tương lai, kiểm định vật lý WMO bảo tồn 2.163 cực đoan, thuật toán khử lặp 3 tầng và tái lập lưới giờ 44.540 dòng. |
| **Diễn giả 3 (Speaker 3)** | **Ngô Minh Triết** | `245193038` | **Phần 3 & Kết luận (Slides 13 – 21)**: Bằng chứng định lượng Before-vs-After (Hình 1), hồ sơ phân phối 6 biến (Bảng 10 & Hình 2), 3 phát hiện khoa học (tương quan Clausius-Clapeyron, phân hóa địa hình 20 trạm, phân tích độ lệch API), demo Streamlit UI, bảng tổng kết thành quả và Q&A. |

* **Giảng viên hướng dẫn:** ThS. Trương Bá Vinh (`vinhtb@uef.edu.vn`) — Khoa Công nghệ Thông tin, Trường Đại học Kinh tế - Tài chính TP.HCM (UEF).
* **Quy mô tập dữ liệu:** 93 ngày (17/07/2026 – 17/10/2026), 2.227 giờ/thành phố; 49.109 dòng thô -> 44.540 dòng sạch đạt chuẩn 100% không khuyết thiếu/trùng lặp.
* **Thời lượng đề xuất:** 12 – 15 phút trình bày (mỗi diễn giả 4 – 5 phút) + 5 – 7 phút phản biện Q&A cùng Hội đồng.

---

# PHẦN 1: KỊCH BẢN THUYẾT TRÌNH BẰNG TIẾNG VIỆT (SLIDES 01 – 21)

---

### SLIDE 01: TRANG TIÊU ĐỀ, THÔNG TIN ĐỀ TÀI & NHÓM NGHIÊN CỨU
* **Diễn giả:** Nguyễn Dạ Giao Đăng (MSSV: 235210195)
* **Thời lượng dự kiến:** ~45 – 50 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Đứng thẳng, tự tin, mắt bao quát toàn thể Hội đồng.
  - Tay hướng về màn hình trình chiếu, chỉ vào 5 khối số liệu nổi bật ở góc trên: **4 APIs / 5 Feeds**, **20 Locations**, **49,109 Rows Raw**, **9 Clean Steps**, **44,540 Rows Clean (100% Certified Output)**.
  - Hướng sự chú ý xuống bảng thông tin thành viên nhóm và giảng viên hướng dẫn ThS. Trương Bá Vinh.
* **Lời thoại chi tiết:**
> *"Kính thưa Thầy ThS. Trương Bá Vinh cùng toàn thể quý Thầy Cô trong Hội đồng phản biện môn học Thu thập và Tiền xử lý Dữ liệu!*
>
> *Em tên là **Nguyễn Dạ Giao Đăng**, và hôm nay em cùng hai bạn nhóm viên là **Hồ Văn Như Ý** và **Ngô Minh Triết** rất vinh dự được đại diện cho Nhóm 3 trình bày báo cáo bảo vệ đồ án cuối kỳ với đề tài Topic 6:*
>
> ***'Thu thập và Làm sạch Dữ liệu Thời tiết Thời gian thực: Đường ống xử lý đa nguồn API, Tiền xử lý 9 bước và Đánh giá chất lượng thực nghiệm trên 20 thành phố tại Việt Nam'***.
>
> *Đồ án của nhóm chúng em tập trung giải quyết trọn vẹn bài toán kỹ thuật cốt lõi trong khoa học dữ liệu: Làm thế nào để xây dựng một đường ống tự động hóa hoàn toàn từ khâu thu thập đa nguồn qua 4 nhà cung cấp API độc lập, kiểm toán phát hiện 9 danh mục lỗi bất thường trong 49.109 bản ghi thô, và áp dụng quy trình tiền xử lý 9 bước nghiêm ngặt để tạo ra bộ dữ liệu chuỗi thời gian chuẩn xác gồm 44.540 dòng sạch tuyệt đối, phục vụ tin cậy cho các mô hình phân tích và dự báo tiếp theo. Sau đây, em xin phép được bắt đầu phần trình bày của nhóm."*

---

### SLIDE 02: LỘ TRÌNH BÁO CÁO (PRESENTATION ROADMAP)
* **Diễn giả:** Nguyễn Dạ Giao Đăng
* **Thời lượng dự kiến:** ~35 – 40 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ tay vào 3 khối màu đại diện cho 3 phần chính trên slide, sau đó lia nhẹ qua Bảng ma trận cấu trúc (Structured Presentation Matrix).
  - Nhấn mạnh vào tính logic, liên kết chặt chẽ giữa 3 phần từ khâu thu thập, tiền xử lý đến đánh giá kết quả thực nghiệm.
* **Lời thoại chi tiết:**
> *"Để quý Thầy Cô tiện theo dõi và đánh giá, bài thuyết trình của nhóm được tổ chức chặt chẽ thành 3 phần chính theo đúng tiến trình kỹ thuật của đồ án:*
>
> * * **Phần 1 (Slides 03 đến 06): Thu thập Dữ liệu & Mô tả Bộ Dữ liệu Thô** — Khám phá nguồn gốc dữ liệu từ 4 APIs, chiến lược thu thập có khả năng phục hồi mạng, cấu trúc schema và bản kiểm toán định lượng 9 danh mục khuyết tật trong 49.109 dòng thô ban đầu.*
> * * **Phần 2 (Slides 07 đến 12): Đường ống Làm sạch & Tiền xử lý Dữ liệu** — Do bạn Hồ Văn Như Ý trình bày, đi sâu vào kiến trúc 9 bước tiền xử lý, khử bỏ chính xác 4.569 dòng dư thừa và rò rỉ, áp dụng ngưỡng vật lý WMO để bảo tồn 2.163 giá trị cực đoan tự nhiên, và giải thuật hợp nhất cảm biến đa nguồn.*
> * * **Phần 3 (Slides 13 đến 20): Kết quả & Đánh giá Chất lượng Thực nghiệm** — Do bạn Ngô Minh Triết đảm nhiệm, cung cấp các bằng chứng đối chiếu Before-vs-After, phân tích thống kê 44.540 dòng sạch, 3 phát hiện khoa học chuyên sâu về khí hậu Việt Nam, và trình diễn ứng dụng trực quan Streamlit.*
>
> *Cuối cùng, tại Slide 21, nhóm sẽ tổng kết danh mục bàn giao và sẵn sàng lắng nghe các câu hỏi đóng góp quý báu từ Hội đồng."*

---

### SLIDE 03: 1.1 NGUỒN GỐC DỮ LIỆU (WHERE DATA COMES FROM)
* **Diễn giả:** Nguyễn Dạ Giao Đăng
* **Thời lượng dự kiến:** ~50 – 55 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào 3 thẻ thông số chính: **4 APIs / 5 Endpoints**, **20 Vietnam Cities** (vượt 3,3 lần yêu cầu đề bài), **49,109 Raw Rows** (cửa sổ 93 ngày, 2.227 giờ/trạm).
  - Trỏ vào **Bảng 1 (Table 1)** để nêu tỷ trọng từng API và **Bảng 2 (Table 2)** để nêu 7 vùng khí hậu từ Sa Pa (1.545m) đến Côn Đảo.
* **Lời thoại chi tiết:**
> *"Bước vào Phần 1, câu hỏi đầu tiên đặt ra là: Dữ liệu thời tiết của nhóm được lấy từ đâu?*
>
> *Như quý Thầy Cô có thể quan sát trên **Bảng 1**, thay vì chỉ sử dụng một API đơn lẻ dễ bị sai lệch hay mất kết nối, nhóm đã tích hợp **4 nhà cung cấp thời tiết quốc tế với 5 nhóm endpoint độc lập**, thu về tổng cộng **49.109 bản ghi thô** trong khung thời gian 93 ngày (từ 17/07 đến 17/10/2026):*
> * *Chiếm tỷ trọng nền tảng 90,90% là **Open-Meteo Archive (tái phân tích ERA5)** với 44.640 dòng quan trắc lịch sử hoàn chỉnh.*
> * *Tiếp đến là **Open-Meteo Forecast** đóng góp 2.880 dòng (5,86%).*
> * * **WeatherAPI.com** đóng góp 1.095 dòng (2,23%) kết hợp giữa dự báo giờ và quan trắc tức thời.*
> * * **Vaisala Xweather** cung cấp 480 dòng (0,98%) quan trắc trạm thực địa độ chính xác cao.*
> * *Và **FreeOpenAPI.dev** đóng góp 14 dòng snapshot hiện tại (0,03%).*
>
> *Đặc biệt, tại **Bảng 2**, mạng lưới quan trắc của nhóm bao phủ **20 thành phố trọng điểm** trải dài trên cả **7 vùng khí hậu đặc trưng của Việt Nam** — từ vùng núi cao Tây Bắc như Sa Pa ở độ cao 1.545 mét, đồng bằng sông Hồng, Bắc Trung Bộ, Duyên hải Nam Trung Bộ, Tây Nguyên lộng gió, Đồng bằng sông Cửu Long, cho đến các vùng đảo tiền tiêu như Phú Quốc và Côn Đảo. Sự phân bổ này đảm bảo bộ dữ liệu mang đầy đủ tính đa dạng sinh thái và địa hình."*

---

### SLIDE 04: 1.2 QUY TRÌNH THU THẬP DỮ LIỆU TỰ ĐỘNG (HOW DATA IS COLLECTED)
* **Diễn giả:** Nguyễn Dạ Giao Đăng
* **Thời lượng dự kiến:** ~50 – 55 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào sơ đồ 4 bước thu thập: **Step 1 (Config & Auth)** -> **Step 2 (HTTP Retry)** -> **Step 3 (Dual Timestamps)** -> **Step 4 (Coverage Log)**.
  - Hướng vào đoạn mã Python minh họa `src/01_collect_weather_data.py` và bảng giải thích trường dữ liệu nguồn gốc (Provenance Metadata).
* **Lời thoại chi tiết:**
> *"Vậy quy trình thu thập dữ liệu tự động được nhóm hiện thực hóa như thế nào?*
>
> *Quy trình thu thập được mô-đun hóa trong tệp `src/01_collect_weather_data.py` theo 4 bước kỹ thuật nghiêm ngặt:*
> * * **Bước 1 (Cấu hình & Xác thực):** Tách biệt toàn bộ tham số tọa độ 20 thành phố, khóa API và tham số thời gian vào tệp `config/config.py`, tuân thủ nguyên tắc mã nguồn an toàn.*
> * * **Bước 2 (Cơ chế phục hồi HTTP Retry):** Trong môi trường mạng thực tế, các cuộc gọi API rất dễ bị ngắt quãng hoặc bị chặn do giới hạn tần suất (Rate Limiting HTTP 429). Nhóm đã cài đặt giải thuật **Exponential Backoff** với tối đa 3 lần thử lại, giúp hệ thống bền bỉ vượt qua các lỗi mạng tạm thời.*
> * * **Bước 3 (Ghi nhận mốc thời gian kép - Dual Timestamps):** Đây là điểm then chốt trong kỹ thuật tiền xử lý: Hệ thống lưu song song mốc `collected_at` (thời điểm gửi yêu cầu HTTP) và mốc `date` (thời điểm quan sát thời tiết thực tế). Cơ chế này giúp chúng em phát hiện chính xác hiện tượng trôi lệch giờ và rò rỉ dữ liệu tương lai.*
> * * **Bước 4 (Nhật ký bao phủ - Coverage Log):** Kiểm toán toàn bộ 100 lượt gọi API (20 trạm × 5 nguồn), tự động xuất ra báo cáo `api_coverage_report.csv` ghi nhận 89 cuộc gọi thành công và 11 cuộc gọi thất bại cục bộ."*

---

### SLIDE 05: 1.3 CẤU TRÚC BỘ DỮ LIỆU & TIẾN HÓA SCHEMA
* **Diễn giả:** Nguyễn Dạ Giao Đăng
* **Thời lượng dự kiến:** ~50 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào 3 thẻ số liệu: **22 Raw -> 31 Clean**, Khóa chính phức hợp **(location_id, time)**, và **13 Cột giám sát chất lượng** (`num_sources`, `spread_*`, `cross_source_conflict`, `is_imputed`).
  - Lướt qua **Bảng 3 (Table 3)** trình bày 6 biến thời tiết chuẩn SI cùng khoảng giá trị vật lý quy chuẩn.
* **Lời thoại chi tiết:**
> *"Tiếp theo, Slide 05 mô tả cấu trúc và sự tiến hóa của schema dữ liệu qua **Bảng 3**:*
>
> *Dữ liệu thô thu về từ 4 nhà cung cấp mang định dạng JSON hoàn toàn không đồng nhất về tên trường và đơn vị đo. Đường ống của nhóm đã chuẩn hóa **22 thuộc tính thô ban đầu thành 31 cột dữ liệu sạch thống nhất theo hệ đo lường quốc tế SI**:*
> * * **Khóa chính phức hợp (Composite Primary Key)** được định nghĩa chuẩn tắc bởi cặp `(location_id, time)`. Với 20 địa điểm và 2.227 giờ quan trắc, bảng dữ liệu đích yêu cầu chính xác 44.540 dòng duy nhất.*
> * * **Sáu biến khí tượng cốt lõi** gồm: Nhiệt độ 2m (`temperature_2m`, khoảng [-10; 50]°C), Độ ẩm tương đối (`relative_humidity_2m`, [0; 100]%), Áp suất mực biển (`pressure_msl`, [850; 1080] hPa), Tốc độ gió 10m (`wind_speed_10m`, [0; 200] km/h), Gió giật (`wind_gusts_10m`, [0; 250] km/h với điều kiện bắt buộc $gust \ge speed$), và Lượng mưa tích lũy (`precipitation`, [0; 300] mm/h).*
> * *Đặc biệt, schema sạch bổ sung **13 cột nguồn gốc và kiểm toán chất lượng**, ghi vết rõ số lượng cảm biến hợp nhất (`num_sources`), độ lệch giữa các nguồn (`spread_*`), cờ xung đột đa nguồn (`cross_source_conflict`) và trạng thái nội suy (`is_imputed`), giúp dữ liệu hoàn toàn minh bạch về xuất xứ."*

---

### SLIDE 06: 1.4 KIỂM TOÁN CÁC BẤT THƯỜNG TRONG DỮ LIỆU THÔ (RAW DATA DEFECTS)
* **Diễn giả:** Nguyễn Dạ Giao Đăng
* **Thời lượng dự kiến:** ~60 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Nhấn mạnh vào 4 khối thông số kiểm toán: **11 Calls & 42 Cells**, **4 Formats & 995 Rows**, **3,574 Duplicates**, **125 Gust & 158k Float**.
  - Trình chiếu **Bảng 4 (Table 4)** liệt kê đầy đủ 9 danh mục khuyết tật thực nghiệm được phát hiện trên 49.109 dòng thô.
  - Thực hiện lời dẫn chuyển giao (handover) sang Diễn giả 2 (Hồ Văn Như Ý).
* **Lời thoại chi tiết:**
> *"Trước khi có thể sử dụng dữ liệu cho bất kỳ bài toán phân tích nào, nhóm đã thực hiện một cuộc kiểm toán toàn diện trên toàn bộ 49.109 dòng thô. Kết quả được lượng hóa chi tiết trong **Bảng 4** với **9 danh mục lỗi bất thường** điển hình:*
>
> 1. * **Thiếu phản hồi API:** 11/100 lượt gọi thất bại (WeatherAPI lỗi 5 trạm, FreeOpenAPI lỗi 6 trạm).*
> 2. * **Ô khuyết thiếu cục bộ:** 14 dòng của FreeOpenAPI bị khuyết 3 biến (độ ẩm, áp suất, gió giật), tạo ra 42 ô NaN.*
> 3. * **Múi giờ và định dạng hỗn tạp:** 49.109 dòng mang 4 kiểu chuỗi thời gian khác nhau (chuỗi có offset khoảng trắng, chuẩn ISO-8601 chữ T, chuỗi ngây thơ chỉ có phút, và chuỗi ngây thơ có giây).*
> 4. * **Bản ghi lệch giờ tròn:** 26 bản ghi quan trắc ở phút lẻ (:30, :45, :29).*
> 5. * **Rò rỉ dự báo tương lai (Data Leakage):** Phát hiện nghiêm trọng với **995 dòng** thời gian tương lai vượt quá mốc thu thập (WeatherAPI đính kèm 795 dòng, Open-Meteo đính kèm 200 dòng).*
> 6. * **Bản ghi trùng lặp tuyệt đối:** 2.780 dòng lặp hoàn toàn do các đợt polling định kỳ của Open-Meteo Forecast.*
> 7. * **Trùng lặp cùng nguồn:** 15 cặp bản ghi của WeatherAPI giữa dữ liệu tức thời và dự báo giờ.*
> 8. * **Chồng lấn đa nguồn:** 779 dòng quan trắc song song tại 514 khung giờ giữa các nhà cung cấp.*
> 9. * **Vi phạm vật lý và nhiễu thập phân:** 125 dòng có gió giật nhỏ hơn gió duy trì, và 158.173 ô mang đuôi nhiễu nhị phân IEEE-754.*
>
> *Chính 9 vấn đề nan giải này là lý do nhóm thiết kế nên đường ống làm sạch 9 bước chuyên sâu. Sau đây, em xin kính mời bạn **Hồ Văn Như Ý** tiếp nối bài thuyết trình với Phần 2: Chi tiết đường ống tiền xử lý."*

---

### SLIDE 07: 2.0 TỔNG QUAN ĐƯỜNG ỐNG TIỀN XỬ LÝ 9 BƯỚC (PIPELINE ARCHITECTURE)
* **Diễn giả:** Hồ Văn Như Ý (MSSV: 245191885)
* **Thời lượng dự kiến:** ~50 – 55 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Cúi đầu chào Thầy Cô và Hội đồng, tiếp nhận lượt nói tự tin.
  - Chỉ vào 3 khối hạch toán cân bằng dòng: **49,109 Raw Input** -> **-4,569 Rows (-9.3%)** -> **44,540 Clean Output**.
  - Lướt qua **Bảng 5 (Table 5)** thể hiện trạng thái dữ liệu giảm dần qua từng bước từ Step 01 đến Step 09.
* **Lời thoại chi tiết:**
> *"Em xin cảm ơn bạn Giao Đăng và kính chào quý Thầy Cô trong Hội đồng! Em là **Hồ Văn Như Ý**. Sau đây em xin đại diện nhóm trình bày **Phần 2: Đường ống Làm sạch và Tiền xử lý Dữ liệu**.*
>
> *Để giải quyết triệt để 9 nhóm khuyết tật mà bạn Giao Đăng vừa trình bày, nhóm đã thiết kế một đường ống tiền xử lý tuần tự gồm **9 bước chuyên biệt** được hiện thực hóa trong tệp `src/02_clean_weather_data.py`.*
>
> *Như quý Thầy Cô thấy trên **Bảng 5**, đường ống tuân thủ nguyên tắc **Hạch toán cân bằng dòng tuyệt đối (Exact Accounting Balance)**:*
> * *Đầu vào ban đầu là **49.109 dòng thô** từ bảng tạm đa nguồn.*
> * *Qua các bước xử lý, hệ thống đã khử bỏ chính xác **4.569 dòng dư thừa** (chiếm tỷ lệ -9,30%), bao gồm: 995 dòng dự báo tương lai, 2.780 dòng lặp tuyệt đối, 15 dòng lặp cùng nguồn, và 779 dòng chồng lấn đa nguồn được hợp nhất thành 514 giờ duy nhất.*
> * *Kết quả đầu ra đạt đúng **44.540 dòng sạch**, khớp chính xác với ma trận hoàn hảo của 20 thành phố nhân với 2.227 giờ quan trắc liên tục, đạt 100% độ đầy đủ, 0 dòng trùng, 0 rò rỉ và 0 vi phạm vật lý.*
>
> *Sau đây, em xin đi sâu vào chi tiết kỹ thuật của từng cụm bước chính."*

---

### SLIDE 08: 2.1 KIỂM TOÁN PHẢN HỒI THIẾU & XỬ LÝ BẢN GHI RỖNG
* **Diễn giả:** Hồ Văn Như Ý
* **Thời lượng dự kiến:** ~45 – 50 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào 3 thẻ: **11 / 100 Missing Calls**, **0 All-Empty Rows**, **42 NaN Cells -> 0**.
  - Hướng vào ma trận bao phủ và bảng đối chiếu các trạm bị thiếu cục bộ: WeatherAPI thiếu 5 trạm (Hà Nội, Phú Lộc, Phú Quốc, Cà Mau, Côn Đảo), FreeOpenAPI thiếu 6 trạm (Vinh, Huế, Phan Thiết, Côn Đảo, Pleiku, Buôn Ma Thuột).
* **Lời thoại chi tiết:**
> *"Tại **Bước 1 và Bước 2**, hệ thống tiến hành kiểm toán độ bao phủ phản hồi và rà soát các bản ghi rỗng:*
>
> * * **Kiểm toán phản hồi thiếu:** Trong 100 lượt gọi API, hệ thống ghi nhận 89 lượt thành công và 11 lượt trả về rỗng do lỗi timeout hoặc chạm trần hạn ngạch. Cụ thể, WeatherAPI bị mất 5 trạm và FreeOpenAPI bị mất 6 trạm. Tuy nhiên, nhờ thiết kế thu hoạch đa nguồn, toàn bộ các thành phố bị khuyết đều được bảo vệ bởi các luồng dữ liệu từ Open-Meteo và Xweather, đảm bảo không một trạm nào bị mất trắng dữ liệu lịch sử.*
> * * **Quy tắc xử lý dòng rỗng:** Đường ống áp dụng tiêu chí loại bỏ nghiêm ngặt: Một dòng chỉ bị coi là dòng rác và bị xóa khi **toàn bộ 6 biến thời tiết đồng thời mang giá trị NaN**. Kết quả rà soát cho thấy có **0 dòng rỗng hoàn toàn**.*
> * *Ngược lại, có **14 dòng bán phần** của FreeOpenAPI bị khuyết 3 biến (độ ẩm, áp suất, gió giật - tạo ra 42 ô NaN). Nhóm quyết định **giữ lại toàn bộ 14 dòng này**, vì chúng vẫn chứa thông tin nhiệt độ và tốc độ gió hợp lệ. Các ô khuyết sẽ được bù đắp thông minh tại bước hợp nhất đa nguồn phía sau."*

---

### SLIDE 09: 2.2 CHUẨN HÓA THỜI GIAN UTC+7 & LOẠI BỎ DỰ BÁO TƯƠNG LAI
* **Diễn giả:** Hồ Văn Như Ý
* **Thời lượng dự kiến:** ~50 – 55 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào 3 thẻ: **49,109 -> UTC+7**, **26 Sub-Hourly Rows (Floored :00)**, **995 Future Rows Cut**.
  - Nhấn mạnh vào **Bảng 6 (Table 6)** thể hiện chi tiết từng định dạng chuỗi thô và số lượng dòng dự báo bị cắt bỏ ở từng nguồn.
* **Lời thoại chi tiết:**
> *"Bước 3 và Bước 4 giải quyết bài toán sống còn về tính đồng bộ của trục thời gian qua **Bảng 6**:*
>
> * * **Chuẩn hóa thời gian về UTC+7:** 49.109 dòng thô ban đầu mang 4 cấu trúc chuỗi thời gian không đồng nhất (từ chuỗi có offset `+07:00`, chuẩn ISO-8601 có chữ `T`, đến chuỗi ngây thơ không múi giờ). Đường ống đã phân tích cú pháp và chuyển đổi 100% về múi giờ chuẩn Việt Nam `Asia/Ho_Chi_Minh`.*
> * * **Làm tròn giờ (Hourly Flooring):** Có **26 bản ghi** quan trắc ở phút lẻ (gồm 12 dòng WeatherAPI ghi lúc :30, :45 và 14 dòng FreeOpenAPI ghi lúc :29:15). Nhóm đã làm tròn sàn (floor) các mốc này về đầu giờ tròn (`:00:00`) để khớp nối chính xác vào lưới chuỗi thời gian đồng nhất.*
> * * **Loại bỏ rò rỉ dữ liệu tương lai (Purging Future Forecasts):** Bằng cách so sánh thời điểm quan sát với thời điểm gửi yêu cầu thực tế `collected_at`, đường ống phát hiện và loại bỏ triệt để **995 dòng dự báo tương lai** (gồm 795 dòng từ WeatherAPI và 200 dòng từ Open-Meteo). Thao tác này đưa số dòng từ 49.109 xuống còn **48.114 dòng**, ngăn chặn hoàn toàn nguy cơ mô hình học máy bị rò rỉ thông tin tương lai."*

---

### SLIDE 10: 2.3 KIỂM ĐỊNH NGƯỠNG VẬT LÝ WMO & BẢO TỒN CỰC ĐOAN
* **Diễn giả:** Hồ Văn Như Ý
* **Thời lượng dự kiến:** ~55 – 60 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào 3 thẻ: **Cell-Level Masking**, **0 Out-of-Range Cells**, **2,163 Extremes Kept**.
  - Trỏ vào **Bảng 7 (Table 7)** để đối chiếu khoảng vật lý WMO với giá trị thực tế quan sát được và số giờ cực đoan được bảo tồn.
* **Lời thoại chi tiết:**
> *"Tại **Bước 5**, nhóm thiết kế cơ chế kiểm định miền tri thức vật lý kết hợp bảo tồn hiện tượng thời tiết cực đoan, thể hiện qua **Bảng 7**:*
>
> * * **Mặt nạ kiểm định cấp độ ô (Cell-Level Masking):** Thay vì xóa cả dòng khi phát hiện một biến sai lệch, thuật toán chỉ chuyển đổi giá trị của riêng ô vi phạm thành NaN, bảo toàn nguyên vẹn các biến khí tượng hợp lệ còn lại trên cùng dòng.*
> * * **Tuân thủ ngưỡng vật lý WMO:** Toàn bộ 267.240 ô giá trị của 6 biến quan trắc đều tuân thủ 100% các ngưỡng khí hậu học của Tổ chức Khí tượng Thế giới (WMO) và Việt Nam: Nhiệt độ nằm trong [-10; 50]°C (thực tế dao động 11,40 đến 39,70°C); Độ ẩm nằm trong [0; 100]%; Áp suất từ 994,7 đến 1025,7 hPa; và Lượng mưa không có giá trị âm.*
> * * **Đóng góp kỹ thuật quan trọng — Bảo tồn 2.163 giá trị cực đoan:** Nếu áp dụng máy móc quy tắc khoảng cách vị phân thống kê $1.5 	imes 	ext{IQR}$, các thuật toán thông thường sẽ tự động xóa bỏ hàng ngàn điểm dữ liệu ngoại lai. Tuy nhiên, nhóm đã chứng minh đây là các hiện tượng khí tượng tự nhiên có thật của mùa mưa bão nhiệt đới Việt Nam. Vì vậy, hệ thống đã **bảo tồn nguyên vẹn 2.163 giờ cực đoan hợp lệ**, bao gồm 479 giờ mưa lớn vượt 5 mm/h (đạt đỉnh 37,40 mm/h tại Hạ Long) và 674 giờ gió giật mạnh, bảo vệ trọn vẹn tín hiệu thời tiết phục vụ cho cảnh báo thiên tai."*

---

### SLIDE 11: 2.4 KHỬ TRÙNG LẶP 3 TẦNG & HỢP NHẤT CẢM BIẾN ĐA NGUỒN
* **Diễn giả:** Hồ Văn Như Ý
* **Thời lượng dự kiến:** ~55 – 60 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào 3 tầng xử lý: **Tier 1 (-2,780 Exact)**, **Tier 2 (-15 Same-Source)**, **Tier 3 (779 -> 514h Mean Fusion)**.
  - Phân tích **Bảng 8 (Table 8)** và công thức tính trung bình đồng thuận $ar{x}_{v,l,t} = rac{1}{n} \sum_{i=1}^n x_{i,v,l,t}$.
* **Lời thoại chi tiết:**
> *"Bước 6 và Bước 7 là trái tim công nghệ của đồ án — giải quyết bài toán xung đột dữ liệu đa nguồn bằng **Mô hình Khử trùng lặp 3 tầng** qua **Bảng 8**:*
>
> * * **Tầng 1 (Khử lặp tuyệt đối):** Loại bỏ **2.780 dòng** trùng lặp 100% trên toàn bộ các cột do cơ chế polling lặp lại của Open-Meteo Forecast, đưa số dòng về 45.334.*
> * * **Tầng 2 (Khử lặp cùng nguồn):** Xử lý **15 cặp bản ghi** của WeatherAPI bị chồng lấn giữa dữ liệu quan trắc tức thời và dự báo giờ trong cùng một trạm. Nhóm áp dụng bảng xếp hạng ưu tiên nguồn `RECORD_TYPE_RANK` (ưu tiên quan trắc thực địa hơn dự báo) kết hợp điền khuyết ngược, loại bỏ tiếp 15 dòng thừa, đưa tập dữ liệu về 45.319 dòng.*
> * * **Tầng 3 (Hợp nhất cảm biến đa nguồn - Sensor Fusion):** Tại 514 khung giờ có từ 2 đến 4 API cùng quan trắc song song (tổng cộng 1.293 dòng thô), thuật toán tính **giá trị trung bình đồng thuận (Consensus Mean)** cho từng biến thời tiết:*
>   $$ar{x}_{v,l,t} = rac{1}{n} \sum_{i=1}^n x_{i,v,l,t}$$
>   *Đồng thời, hệ thống đo lường độ phân tán (`spread`) giữa các trạm và gắn cờ `cross_source_conflict = True` cho **113 giờ có độ lệch lớn** ($|\Delta T| > 3^\circ	ext{C}$ hoặc $|\Delta RH| > 15\%$).*
>
> *Quá trình này hợp nhất 1.293 dòng thành 514 giờ duy nhất, giảm tiếp 779 dòng, đưa bộ dữ liệu về mốc chuẩn xác **44.540 dòng**."*

---

### SLIDE 12: 2.5 TÁI LẬP LƯỚI GIỜ, TÍNH NHẤT QUÁN & ĐỘ CHÍNH XÁC
* **Diễn giả:** Hồ Văn Như Ý
* **Thời lượng dự kiến:** ~50 – 55 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào 3 khối kết quả: **20 × 2,227 = 44,540 Complete Hourly Grid**, **125 Gust Rows Fixed**, **158,173 Float Cells Cleaned**.
  - Trình bày **Bảng 9 (Table 9)** tổng kết các bước tinh chỉnh vật lý và mã nguồn `src/02_clean_weather_data.py`.
  - Thực hiện lời dẫn chuyển giao lượt nói (handover) sang Diễn giả 3 (Ngô Minh Triết).
* **Lời thoại chi tiết:**
> *"Tại **Bước 8 và Bước 9**, nhóm hoàn thiện các khâu tinh chỉnh cuối cùng thể hiện trên **Bảng 9**:*
>
> * * **Tái lập lưới giờ liên tục:** Tái lập chỉ mục toàn diện trên tích Descartes giữa 20 thành phố và 2.227 mốc giờ liên tục, đạt chính xác 44.540 dòng. Các ô khuyết thiếu cục bộ ($\le 6$ giờ liên tiếp) được nội suy tuyến tính có chặn biên, đưa toàn bộ 42 ô NaN ban đầu về mức **0 ô khuyết thiếu (0,00%)**.*
> * * **Thực thi quy luật khí động học gió:** Trong khí tượng, gió giật tức thời luôn phải lớn hơn hoặc bằng tốc độ gió duy trì trung bình. Dữ liệu thô có 125 dòng vi phạm quy luật này do sai khác trong thuật toán làm mịn của cảm biến. Nhóm đã thực thi luật vật lý:*
>   $$wind\_gusts = \max(wind\_gusts, wind\_speed)$$
>   *sửa chữa dứt điểm 100% các vi phạm mà không làm mất bản ghi.*
> * * **Khử nhiễu dấu phẩy động Float32:** Làm tròn 2 chữ số thập phân trên toàn bộ **158.173 ô** mang đuôi nhiễu nhị phân IEEE-754.*
>
> *Sau 9 bước tiền xử lý, chúng ta đã có một bộ dữ liệu hoàn hảo 100%. Để chứng minh điều này bằng các con số thực nghiệm và đồ thị khoa học, em xin kính mời bạn **Ngô Minh Triết** trình bày Phần 3."*

---

### SLIDE 13: 3.1 ĐỐI CHIẾU TRƯỚC VÀ SAU LÀM SẠCH (BEFORE VS. AFTER AUDIT)
* **Diễn giả:** Ngô Minh Triết (MSSV: 245193038)
* **Thời lượng dự kiến:** ~50 – 55 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Tự tin chào Thầy Cô và Hội đồng, tiếp nhận bài nói.
  - Chỉ vào 4 chỉ số kiểm toán lớn: **49,109 -> 44,540 (-4,569 rows, -9.3%)**, **42 NaN -> 0 Cells (100% Completeness)**, **125 Gust -> 0 Errors (100% Physical Consistency)**, và **2,163 Extremes Kept**.
  - Hướng sự chú ý vào **Hình 1 (Figure 1)** minh họa sự biến mất hoàn toàn của các loại lỗi dữ liệu thô.
* **Lời thoại chi tiết:**
> *"Em xin cảm ơn bạn Như Ý và kính chào quý Thầy Cô trong Hội đồng! Em tên là **Ngô Minh Triết**. Sau đây em xin đại diện nhóm trình bày **Phần 3: Kết quả Đánh giá Chất lượng Thực nghiệm và Các Phát hiện Dữ liệu**.*
>
> *Mở đầu Phần 3, Slide 13 và **Hình 1** mang đến bằng chứng định lượng thuyết phục nhất chứng minh toàn bộ các khuyết tật trong dữ liệu thô đã được giải quyết triệt để 100%:*
> * *Về **Quy mô tập dữ liệu**: Từ 49.109 dòng thô ban đầu, đường ống đã bóc tách chính xác 995 dòng dự báo tương lai và 3.574 bản ghi trùng lặp các tầng, đưa bộ dữ liệu về đúng quy chuẩn toán học:*
>   $$N_{total} = 20 	ext{ thành phố} 	imes 2.227 	ext{ giờ} = 44.540 	ext{ dòng sạch}$$
> * *Về **Độ đầy đủ dữ liệu**: Toàn bộ 42 ô khuyết thiếu ban đầu đã được lấp đầy hoàn hảo, đạt tỷ lệ hoàn thiện **100,00% trên toàn bộ 267.240 ô quan trắc** của 6 biến thời tiết.*
> * *Về **Tính nhất quán vật lý**: Toàn bộ 125 dòng vi phạm gió giật đã được chuẩn hóa về mức 0 lỗi, 0 ô lệch múi giờ, và 0 ô nhiễu thập phân.*
> * *Đồng thời, **2.163 giá trị thời tiết cực đoan tự nhiên** (gồm 674 giờ gió lớn, 479 giờ mưa giông và 472 giờ gió giật) được bảo tồn nguyên vẹn, đảm bảo độ chân thực khí hậu tối đa."*

---

### SLIDE 14: 3.2 HỒ SƠ THỐNG KÊ BỘ DỮ LIỆU ĐẦU RA (OUTPUT STATISTICAL PROFILE)
* **Diễn giả:** Ngô Minh Triết
* **Thời lượng dự kiến:** ~50 – 55 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào 3 thẻ thống kê nổi bật: **26.55 ± 3.72 °C** (Nhiệt độ phân phối chuẩn Gauss), **82.32 ± 14.37 %** (Độ ẩm gió mùa nhiệt đới), và **Skew +8.51 | Kurt 142.9** (Lượng mưa đuôi dày cực đoan).
  - Trình bày chi tiết **Bảng 10 (Table 10)** với đầy đủ 9 tham số thống kê mô tả (Mean, SD, Min, Q25, Median, Q75, Max, Skew, Kurt) cho cả 6 biến thời tiết trên N = 44.540 dòng.
* **Lời thoại chi tiết:**
> *"Trên bộ dữ liệu sạch 44.540 dòng, nhóm đã tiến hành phân tích thống kê mô tả toàn diện qua **Bảng 10**:*
>
> * * **Nhiệt độ trung bình toàn quốc** đạt **26,55 ± 3,72°C**, với trung vị là 26,80°C. Đáng chú ý, hệ số bất đối xứng Skewness xấp xỉ bằng 0 (+0,02), chứng minh phân phối nhiệt độ tuân theo quy luật chuẩn (Gaussian) rất đẹp trong khoảng từ 11,40°C đến 39,70°C.*
> * * **Độ ẩm tương đối** có giá trị trung bình **82,32 ± 14,37%** với trung vị 85,00%, phản ánh rõ nét đặc trưng khí hậu nhiệt đới gió mùa ẩm của Việt Nam, với chặn trên vật lý chạm đúng 100,00%.*
> * * **Áp suất mực biển** trung bình đạt **1009,5 ± 3,92 hPa**, biến thiên ổn định từ 994,7 đến 1025,7 hPa.*
> * *Trái lại, **Lượng mưa** mang đặc trưng phân phối đuôi dày lệch phải cực mạnh với Skewness lên tới **+8,51** và Kurtosis lên tới **142,9**. Điều này hoàn toàn phù hợp với thực tế tự nhiên: đại đa số các giờ trong ngày là tạnh ráo (75% số giờ quan trắc có lượng mưa $\le 0,20$ mm/h), nhưng khi mưa rào nhiệt đới xuất hiện, lượng mưa tăng vọt rất nhanh lên đến đỉnh 37,40 mm/h.*
> * *Các chỉ số kiểm toán ở chân slide xác nhận 100% bộ dữ liệu đạt chuẩn PASS trên mọi tiêu chí."*

---

### SLIDE 15: 3.3 PHÂN PHỐI ĐẶC TRƯNG CÁC BIẾN QUAN TRẮC (FIGURE 2)
* **Diễn giả:** Ngô Minh Triết
* **Thời lượng dự kiến:** ~45 – 50 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào **Hình 2 (Figure 2)** — biểu đồ hộp (boxplots) của 6 biến thời tiết.
  - Phân tích sự đối lập giữa nhóm biến đối xứng (Nhiệt độ, Áp suất) và nhóm biến lệch phải (Mưa, Gió); chỉ vào mốc chặn trên 100% của độ ẩm và 2 điểm cực đoan bão được giữ lại (81 km/h ở Pleiku, 37,4 mm/h ở Hạ Long).
* **Lời thoại chi tiết:**
> *"Sang Slide 15, **Hình 2** minh họa trực quan phân phối dạng biểu đồ hộp của cả 6 biến khí tượng, làm nổi bật 3 kết luận vật lý then chốt:*
>
> * * **Sự phân hóa giữa hai nhóm chế độ vật lý:** Nhiệt độ và Áp suất mực biển thể hiện dạng hộp rất cân đối quanh trung vị, phản ánh chu kỳ biến thiên ngày đêm và theo mùa ổn định. Ngược lại, Tốc độ gió, Gió giật và Lượng mưa thể hiện các đuôi ngoại lai dài kéo dài về phía trên bên phải, đặc trưng cho các đợt giông lốc cục bộ.*
> * * **Chặn trên độ ẩm chính xác tuyệt đối:** Hộp tứ phân độ ẩm dao động từ 74% đến 94%, và râu trên chạm đúng mức 100,00%, hoàn toàn không có bất kỳ điểm nhiễu cảm biến vô lý nào vượt quá 100%.*
> * * **Xác thực các cực đoan bão nhiệt đới:** Đồ thị xác nhận việc bảo tồn thành công các trận bão thực tế, tiêu biểu là gió giật đạt đỉnh **81,0 km/h tại Pleiku** và trận mưa giông nhiệt đới dữ dội **37,4 mm/h tại Hạ Long**."*

---

### SLIDE 16: 3.4 PHÁT HIỆN 1: TƯƠNG QUAN NHIỆT ĐỘNG & LƯỢNG MƯA 20 ĐỊA PHƯƠNG
* **Diễn giả:** Ngô Minh Triết
* **Thời lượng dự kiến:** ~50 – 55 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào ma trận tương quan và biểu đồ lượng mưa tích lũy 20 thành phố trên **Hình 3 (Figure 3)**.
  - Nhấn mạnh vào 3 con số then chốt: **r = -0.66** (Nhiệt độ - Độ ẩm), **r = -0.49** (Nhiệt độ - Áp suất), và **tỷ lệ mưa 2,74 lần** giữa Vinh (1.293 mm) và Nha Trang (472 mm).
* **Lời thoại chi tiết:**
> *"Từ tập dữ liệu sạch, nhóm đã rút ra **3 phát hiện khoa học sâu sắc**. Phát hiện đầu tiên liên quan đến tương quan nhiệt động và lượng mưa tích lũy trên **Hình 3**:*
>
> * * **Tương quan nghịch rất mạnh giữa Nhiệt độ và Độ ẩm ($r = -0,66$):** Đây là minh chứng thực nghiệm hoàn hảo cho phương trình nhiệt động lực học Clausius-Clapeyron: Khi bức xạ mặt trời hun nóng không khí vào buổi trưa, khả năng chứa hơi nước bão hòa tăng lên làm độ ẩm tương đối giảm sâu; và ngược lại khi đêm xuống.*
> * * **Tương quan nghịch giữa Nhiệt độ và Áp suất ($r = -0,49$):** Thể hiện rõ hiện tượng hình thành các vùng áp thấp nhiệt lực vào các buổi chiều hè nóng bức trên đất liền.*
> * * **Tương quan gió giật ($r = +0,87$):** Gió giật liên kết mật thiết với tốc độ gió duy trì, tuân thủ chặt chẽ cơ chế nhiễu động tầng biên khí quyển.*
> * * **Sự phân hóa lượng mưa tích lũy 20 thành phố:** Tổng lượng mưa trong 93 ngày ghi nhận sự chênh lệch tới **2,74 lần** giữa các vùng miền: Đứng đầu cả nước là **Vinh (1.293,1 mm)** và **Pleiku (1.235,4 mm)** do đón các đợt gió mùa Tây Nam và bão thu Trung Bộ; trong khi vùng khô hạn nhất là **Nha Trang chỉ đạt 471,6 mm** nhờ nằm ở vùng khuất gió."*

---

### SLIDE 17: 3.5 PHÁT HIỆN 2: HỒ SƠ NHIỆT ĐỘ & PHÂN HÓA ĐỊA HÌNH
* **Diễn giả:** Ngô Minh Triết
* **Thời lượng dự kiến:** ~50 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào **Hình 4 (Figure 4)** thể hiện dải nhiệt độ (Min – Mean – Max) trên 20 thành phố.
  - So sánh Sa Pa (18,95°C) với Đà Nẵng (29,48°C) — độ chênh lệch 10,53°C; chỉ vào độ ổn định nhiệt của Côn Đảo (độ lệch chuẩn 0,88°C, dải nhiệt chỉ 5,3°C).
* **Lời thoại chi tiết:**
> *"Phát hiện thứ hai làm nổi bật sự phân hóa địa hình sâu sắc của khí hậu Việt Nam qua **Hình 4**:*
>
> * * **Độ chênh lệch nhiệt độ trung bình toàn quốc lên tới 10,53°C:** Trạm lạnh nhất cả nước là thị trấn vùng cao **Sa Pa** ở độ cao 1.545m với nhiệt độ trung bình chỉ **18,95°C** (thấp nhất 11,40°C). Ngược lại, trạm nóng nhất là dải đồng bằng ven biển **Đà Nẵng** với nhiệt độ trung bình đạt **29,48°C** (cao nhất lên tới 39,70°C).*
> * * **Xác thực quy luật suy giảm nhiệt theo độ cao (Lapse Rate):** Dữ liệu phản ánh chính xác quy luật vật lý khí quyển $-6,5^\circ	ext{C}$ cho mỗi 1.000m độ cao: Sa Pa (18,95°C), Phú Lộc đỉnh đèo (21,86°C), Pleiku (22,66°C) và Đà Lạt (23,07°C) mát hơn rõ rệt so với các vùng đồng bằng lân cận.*
> * * **Hiệu ứng điều hòa nhiệt đại dương tại Côn Đảo:** Côn Đảo có độ lệch chuẩn nhiệt độ chỉ **0,88°C** với dải biến thiên cực hẹp từ 25,5 đến 30,8°C (biên độ chỉ 5,3°C). Trong khi đó, các trạm nội địa Bắc Trung Bộ như Huế có biên độ nhiệt ngày đêm và thời tiết lên tới 16,6°C."*

---

### SLIDE 18: 3.6 PHÁT HIỆN 3: PHÂN TÍCH ĐỘ LỆCH HỆ THỐNG GIỮA CÁC NHÀ CUNG CẤP API
* **Diễn giả:** Ngô Minh Triết
* **Thời lượng dự kiến:** ~55 – 60 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào **Hình 5 (Figure 5)** và **Bảng 11 (Table 11)** so sánh sai số từng cặp API lấy Open-Meteo làm mốc đối chuẩn.
  - Phân tích 3 con số cốt lõi: **Xweather lệch nóng +1,49°C**, **WeatherAPI lệch lạnh -0,61°C**, và **113 giờ xung đột (22,0%)** được gắn cờ cảnh báo.
* **Lời thoại chi tiết:**
> *"Phát hiện thứ ba mang giá trị thực tiễn cao nhất cho kỹ thuật dữ liệu, được đúc kết trên **Hình 5** và **Bảng 11**: Phân tích độ lệch hệ thống giữa các nhà cung cấp API tại 514 giờ có quan trắc song song:*
>
> * * **Vaisala Xweather có thiên hướng 'Nóng và Khô' hơn:** So với Open-Meteo trên 480 giờ đối chiếu, Xweather báo nhiệt độ cao hơn trung bình **+1,49°C** (sai số tuyệt đối trung bình MAD = 1,72°C) và độ ẩm thấp hơn **-4,05%** (MAD = 7,64%). Điều này là do Xweather lấy dữ liệu từ các cảm biến thực tế đặt tại các sân bay hoặc đô thị chịu hiệu ứng đảo nhiệt.*
> * * **WeatherAPI có thiên hướng 'Mát hơn':** Báo nhiệt độ thấp hơn trung bình **-0,61°C** (MAD = 1,44°C) và áp suất thấp hơn **-0,69 hPa** do sử dụng mô hình nội suy số trị quy mô khu vực.*
> * * **FreeOpenAPI:** Ghi nhận độ lệch nhỏ +0,15°C trên 14 giờ mẫu đối chiếu.*
> * * **Đóng góp về tính minh bạch dữ liệu:** Có tới **113 giờ (chiếm 22,0% số giờ đa nguồn)** xuất hiện xung đột mạnh giữa các API ($|\Delta T| > 3^\circ	ext{C}$ hoặc $|\Delta RH| > 15\%$). Thay vì tùy tiện xóa bỏ dữ liệu của bất kỳ bên nào, đường ống đã tính trung bình đồng thuận và gắn cờ cảnh báo `cross_source_conflict = True`, giúp các nhà khoa học dữ liệu dễ dàng truy xuất nguồn gốc."*

---

### SLIDE 19: 3.7 XÁC MINH TRỰC QUAN TRÊN GIAO DIỆN WEB STREAMLIT
* **Diễn giả:** Ngô Minh Triết
* **Thời lượng dự kiến:** ~45 – 50 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Hướng về màn hình giao diện ứng dụng web Streamlit minh họa trên slide.
  - Nêu bật 3 tính năng tương tác người dùng: **Live 4-API Polling**, **Before vs After Audit View**, và **20-City Stats Explorer**.
* **Lời thoại chi tiết:**
> *"Để chứng minh tính khả thi trong môi trường sản xuất thực tế, nhóm đã đóng gói toàn bộ đường ống thành một ứng dụng web trực quan bằng **Streamlit** tại tệp `app.py`:*
>
> * * **Tính năng 1 — Live 4-API Polling:** Người dùng chỉ cần chọn một thành phố và nhấn nút, hệ thống sẽ gửi yêu cầu HTTP song song tới cả 4 nhà cung cấp, hiển thị dữ liệu thô và đo lường thời gian phản hồi theo thời gian thực.*
> * * **Tính năng 2 — Before vs After Audit:** Cung cấp bảng điều khiển so sánh trực quan từng bước làm sạch, cho phép kiểm tra ngay lập tức sự biến mất của 42 ô NaN và 125 vi phạm vật lý.*
> * * **Tính năng 3 — 20-City Stats Explorer:** Cho phép người dùng tùy chọn khám phá phân phối nhiệt độ, lượng mưa, ma trận tương quan của từng trạm trong số 20 thành phố, và tải về tệp dữ liệu sạch chuẩn CSV.*
>
> *Ứng dụng đã sẵn sàng chạy live để phục vụ phần kiểm chứng của Hội đồng."*

---

### SLIDE 20: 3.8 BẢNG TỔNG KẾT THÀNH QUẢ & ĐÓNG GÓP (SUMMARY SCORECARD)
* **Diễn giả:** Ngô Minh Triết
* **Thời lượng dự kiến:** ~50 – 55 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Chỉ vào 3 trụ cột kết quả: **100% Defect Removal (Certified Gold Dataset)**, **Climatic Fidelity (2,163 Extremes Preserved)**, và **Multi-Source Lineage**.
  - Rà soát **Bảng 12 (Table 12)** đối chiếu 8 chiều chất lượng dữ liệu giữa Trước (Raw) và Sau làm sạch (Cleaned).
* **Lời thoại chi tiết:**
> *"Trước khi kết thúc, Slide 20 và **Bảng 12** tổng kết toàn diện giá trị kỹ thuật mà đồ án đã mang lại qua 8 chiều đánh giá chất lượng:*
>
> 1. * **Quy mô dữ liệu:** Rút gọn từ 49.109 dòng thô xuống đúng **44.540 dòng sạch** (-9,3% dư thừa).*
> 2. * **Độ bao phủ trạm:** Từ 89/100 cuộc gọi thành công, hợp nhất đa nguồn giúp bao phủ trọn vẹn **100% không gian thời gian** của 20 trạm.*
> 3. * **Múi giờ & Dự báo:** Chuẩn hóa 100% về UTC+7, cắt bỏ 995 dòng rò rỉ tương lai.*
> 4. * **Bản ghi trùng lặp:** Loại bỏ hoàn toàn 3.574 bản ghi trùng, đảm bảo cặp khóa `(location_id, time)` duy nhất 100%.*
> 5. * **Ô khuyết thiếu:** 42 ô NaN đưa về đúng **0 ô khuyết (0,00%)**.*
> 6. * **Quy luật vật lý:** 125 vi phạm gió giật được sửa chữa; giữ lại nguyên vẹn **2.163 giờ thời tiết cực đoan tự nhiên**.*
> 7. * **Khí hậu vùng miền:** Phản ánh chân thực độ chênh nhiệt 10,53°C giữa Sa Pa và Đà Nẵng cùng quy luật suy giảm nhiệt theo độ cao.*
> 8. * **Độ lệch API:** Lượng hóa sai số Xweather +1,49°C và gắn cờ minh bạch cho 113 giờ xung đột.*
>
> *Bộ dữ liệu hoàn toàn đạt cấp độ **Gold Standard**, sẵn sàng cho các bài toán phân tích học máy chuyên sâu."*

---

### SLIDE 21: LỜI CẢM ƠN, TỔNG KẾT BÀN GIAO & PHẦN HỎI ĐÁP (Q&A)
* **Diễn giả:** Ngô Minh Triết (cùng Giao Đăng & Như Ý đứng nghiêm trang)
* **Thời lượng dự kiến:** ~40 – 45 giây
* **Điểm nhìn & Hành động trình chiếu (Visual Cues):**
  - Ba thành viên đứng thẳng, hướng về phía Thầy hướng dẫn và Hội đồng phản biện.
  - Chỉ vào Bảng danh mục 7 sản phẩm bàn giao (Deliverables Checklist) đều ở trạng thái **Verified / Certified / Complete**.
* **Lời thoại chi tiết:**
> *"Kính thưa Thầy ThS. Trương Bá Vinh và toàn thể quý Thầy Cô trong Hội đồng!*
>
> *Thay mặt Nhóm 3, em xin được gửi lời cảm ơn chân thành và sâu sắc nhất tới Thầy Trương Bá Vinh đã tận tình hướng dẫn, truyền đạt những kiến thức và nguyên tắc chuẩn mực về Thu thập và Làm sạch Dữ liệu trong suốt học kỳ vừa qua, giúp nhóm em hoàn thành trọn vẹn đồ án này.*
>
> *Nhóm chúng em đã hoàn thiện và đóng gói đầy đủ **7 sản phẩm bàn giao** theo đúng quy định: gồm mã nguồn thu thập `01`, mã nguồn làm sạch `02`, tệp dữ liệu thô, tệp dữ liệu sạch 44.540 dòng, báo cáo kiểm toán chất lượng JSON, ứng dụng Streamlit, cùng toàn bộ cuốn báo cáo tiểu luận định dạng IEEE và slide thuyết trình.*
>
> *Đến đây, phần thuyết trình của Nhóm 3 xin phép được khép lại. Nhóm chúng em rất mong nhận được những nhận xét, góp ý và câu hỏi phản biện từ quý Thầy Cô để đồ án được hoàn thiện hơn nữa. Em xin chân thành cảm ơn!"*

---

# PHẦN 2: ENGLISH PRESENTATION SCRIPT (SLIDES 01 – 21)

---

### SLIDE 01: TITLE, CAPSTONE METADATA & RESEARCH TEAM
* **Speaker:** Nguyen Da Giao Dang (Student ID: 235210195)
* **Estimated Duration:** ~45 – 50 seconds
* **Visual Cues & Actions:**
  - Stand upright, maintain eye contact with the defense committee.
  - Gesture toward the top metrics cards: **4 APIs / 5 Feeds**, **20 Locations**, **49,109 Raw Rows**, **9 Clean Steps**, **44,540 Clean Rows (100% Certified Output)**.
  - Reference supervisor MSc. Truong Ba Vinh and the three team members.
* **Spoken Script:**
> *"Distinguished members of the Defense Committee, and our respected supervisor MSc. Truong Ba Vinh!*
>
> *My name is **Nguyen Da Giao Dang**, and today, together with my teammates **Ho Van Nhu Y** and **Ngo Minh Triet**, I am honored to represent Team 3 to present our Capstone Defense on Topic 6:*
>
> ***'Real-Time Weather Data Collection & Cleaning: End-to-End Multi-API Harvesting, 9-Step Preprocessing & Empirical Quality Evaluation Across 20 Vietnam Cities'***.
>
> *This project addresses a fundamental engineering challenge in applied data science: How to build a fully automated, resilient data pipeline that ingests heterogeneous weather streams from 4 independent API providers, audits 9 distinct categories of raw data defects across 49,109 input rows, and applies a strict 9-step preprocessing architecture to deliver an immaculate, gold-standard dataset of 44,540 hourly records. I will now begin Part 1 of our presentation."*

---

### SLIDE 02: PRESENTATION ROADMAP & STRUCTURED MATRIX
* **Speaker:** Nguyen Da Giao Dang
* **Estimated Duration:** ~35 – 40 seconds
* **Visual Cues & Actions:**
  - Point to the three main parts and the Structured Presentation Matrix.
  - Emphasize the systematic end-to-end flow from collection to empirical evaluation.
* **Spoken Script:**
> *"To facilitate your evaluation, our presentation is structured into three cohesive, rigorous sections:*
>
> * * **Part 1 (Slides 03 to 06): Data Collection & Raw Dataset Description** — Presented by myself, detailing our 4-API architecture, network retry resilience, schema standardization, and the empirical audit of 9 raw defect classes.*
> * * **Part 2 (Slides 07 to 12): Data Cleaning & Preprocessing Pipeline** — Presented by Ho Van Nhu Y, walking through our sequential 9-step pipeline, the exact accounting reduction of 4,569 redundant rows, domain-informed WMO range checks that preserve 2,163 natural extremes, and multi-source sensor fusion.*
> * * **Part 3 (Slides 13 to 20): Empirical Results & Quality Evaluation** — Presented by Ngo Minh Triet, presenting quantitative before-vs-after proof, 6-variable distributions, three climatological insights, and a live Streamlit UI demonstration.*
>
> *Finally, Slide 21 summarizes our deliverable checklist and opens the floor for the Q&A session."*

---

### SLIDE 03: 1.1 WHERE DATA COMES FROM
* **Speaker:** Nguyen Da Giao Dang
* **Estimated Duration:** ~50 – 55 seconds
* **Visual Cues & Actions:**
  - Point to **Table 1** (API provider shares) and **Table 2** (20 monitoring locations across 7 climate zones).
  - Emphasize the elevation gradient from alpine Sa Pa (1,545m) down to offshore Con Dao.
* **Spoken Script:**
> *"Moving to Part 1, the first question is: Where does our weather data originate?*
>
> *As shown in **Table 1**, rather than relying on a single, vulnerable data source, we architected a multi-provider harvesting network comprising **4 global weather providers and 5 endpoint groups**, gathering **49,109 raw records** across a 93-day window from July 17 to October 17, 2026:*
> * * **Open-Meteo Archive (ERA5 Reanalysis)** forms the foundational backbone with 44,640 records, representing 90.90% of the raw data.*
> * * **Open-Meteo Forecast** provides 2,880 records (5.86%).*
> * * **WeatherAPI.com** contributes 1,095 records (2.23%) across hourly forecasts and real-time observations.*
> * * **Vaisala Xweather** adds 480 high-precision station observation records (0.98%).*
> * *And **FreeOpenAPI.dev** provides 14 snapshot records (0.03%).*
>
> *Furthermore, as detailed in **Table 2**, our monitoring network covers **20 key cities across all 7 distinct climatic regimes of Vietnam** — spanning from alpine Northwest peaks like Sa Pa at 1,545 meters elevation, through the Red River Delta, Central coastal plains, the windy Central Highlands, down to the Mekong Delta and offshore islands like Phu Quoc and Con Dao. This ensures rich geographic and climatological heterogeneity."*

---

### SLIDE 04: 1.2 HOW DATA IS COLLECTED
* **Speaker:** Nguyen Da Giao Dang
* **Estimated Duration:** ~50 – 55 seconds
* **Visual Cues & Actions:**
  - Guide attention through the 4 ingestion steps: **Config & Auth**, **HTTP Retry**, **Dual Timestamps**, and **Coverage Log**.
  - Point to the Python ingestion script `src/01_collect_weather_data.py` and the provenance metadata specifications.
* **Spoken Script:**
> *"How is this heterogeneous data automatically harvested?*
>
> *Our ingestion pipeline is implemented in `src/01_collect_weather_data.py` and follows four robust engineering steps:*
> * * **Step 1 (Configuration & Authentication):** All geographic coordinates, API authentication credentials, and query windows are fully decoupled into `config/config.py`.*
> * * **Step 2 (HTTP Retry Resilience):** Real-world public APIs frequently encounter network latency and HTTP 429 rate limits. We implemented **exponential backoff with up to 3 retries**, enabling graceful recovery from transient network drops.*
> * * **Step 3 (Dual Timestamps Recording):** Crucially, our collector records both `collected_at` (the exact UTC+7 HTTP retrieval timestamp) and `date` (the valid meteorological observation hour). This dual-clock mechanism is essential for detecting future forecast leakage.*
> * * **Step 4 (Coverage Auditing):** Every single API request is audited across 100 endpoint calls (20 locations × 5 sources), logging 89 successful calls and 11 silent dropouts into `api_coverage_report.csv`."*

---

### SLIDE 05: 1.3 DATASET STRUCTURE & SCHEMA EVOLUTION
* **Speaker:** Nguyen Da Giao Dang
* **Estimated Duration:** ~50 seconds
* **Visual Cues & Actions:**
  - Point to the schema transformation: **22 Raw -> 31 Clean**, Composite Primary Key `(location_id, time)`, and **13 Quality Lineage Columns**.
  - Review **Table 3** listing the standardized SI meteorological variables and physical bounds.
* **Spoken Script:**
> *"Slide 05 presents the structural schema evolution through **Table 3**:*
>
> *Raw JSON payloads from the 4 providers contained inconsistent key naming conventions and measurement units. Our pipeline unified **22 raw heterogeneous fields into 31 standardized columns adhering to International System of Units (SI)**:*
> * *The dataset is indexed by a **Composite Primary Key** defined by `(location_id, time)`. For 20 stations across 2,227 hours, the target tabular space mandates exactly 44,540 unique records.*
> * * **Six core meteorological variables** are standardized: 2m air temperature (`temperature_2m`, [-10, 50]°C), relative humidity (`relative_humidity_2m`, [0, 100]%), sea-level pressure (`pressure_msl`, [850, 1080] hPa), 10m wind speed (`wind_speed_10m`, [0, 200] km/h), wind gusts (`wind_gusts_10m`, [0, 250] km/h, with the physical constraint $gust \ge speed$), and hourly precipitation (`precipitation`, [0, 300] mm/h).*
> * *In addition, we engineered **13 audit and lineage columns** (`num_sources`, `spread_*`, `cross_source_conflict`, and `is_imputed`), providing complete data provenance and analytical transparency."*

---

### SLIDE 06: 1.4 RAW DATA DEFECTS & EMPIRICAL AUDIT
* **Speaker:** Nguyen Da Giao Dang
* **Estimated Duration:** ~60 seconds
* **Visual Cues & Actions:**
  - Highlight the 4 defect metric callouts: **11 Calls & 42 Cells**, **4 Formats & 995 Rows**, **3,574 Duplicates**, **125 Gust & 158k Float**.
  - Walk through **Table 4** detailing the 9 empirical defect categories.
  - Deliver the handover transition to Speaker 2 (Ho Van Nhu Y).
* **Spoken Script:**
> *"Prior to any analysis, we conducted an exhaustive audit across all 49,109 raw records. As quantified in **Table 4**, we discovered **9 distinct defect categories** in the unprocessed data:*
>
> 1. * **Missing API Responses:** 11 of 100 requests returned empty payloads (5 in WeatherAPI, 6 in FreeOpenAPI).*
> 2. * **Partial Missing Cells:** 14 FreeOpenAPI records omitted 3 key variables, producing 42 NaN values.*
> 3. * **Heterogeneous Timestamps:** 49,109 rows spanned 4 different string formats (space-separated offset, ISO-8601 T-strings, minute-level naive, and second-level naive).*
> 4. * **Sub-Hourly Observations:** 26 off-grid records logged at minutes :30, :45, or :29.*
> 5. * **Future Forecast Leakage:** A critical defect where **995 future forecast hours** were appended beyond the collection cutoff (795 from WeatherAPI, 200 from Open-Meteo).*
> 6. * **Exact Duplicate Records:** 2,780 identical rows caused by overlapping polling batches.*
> 7. * **Same-Source Clashes:** 15 conflicting pairs between WeatherAPI current and forecast feeds.*
> 8. * **Cross-Source Overlaps:** 779 multi-provider records across 514 co-temporal hours.*
> 9. * **Physical Inconsistencies & Float Noise:** 125 records had wind gusts lower than sustained wind speeds, and 158,173 cells exhibited IEEE-754 precision tails.*
>
> *These 9 critical defects necessitated our 9-step cleaning architecture. I now hand over the presentation to **Ho Van Nhu Y** to walk you through Part 2."*

---

### SLIDE 07: 2.0 DATA CLEANING PIPELINE OVERVIEW
* **Speaker:** Ho Van Nhu Y (Student ID: 245191885)
* **Estimated Duration:** ~50 – 55 seconds
* **Visual Cues & Actions:**
  - Acknowledge Giao Dang, greet the defense committee.
  - Point to the exact accounting balance: **49,109 Raw Input** -> **-4,569 Rows (-9.3%)** -> **44,540 Clean Output**.
  - Review **Table 5** demonstrating the step-by-step reduction from Step 01 to Step 09.
* **Spoken Script:**
> *"Thank you, Giao Dang, and good morning, respected Committee members! My name is **Ho Van Nhu Y**. I will now present **Part 2: Data Cleaning & Preprocessing Pipeline**.*
>
> *To eliminate all 9 defect categories systematically, we implemented an automated 9-step preprocessing architecture in `src/02_clean_weather_data.py`.*
>
> *As shown in **Table 5**, the pipeline adheres strictly to an **Exact Accounting Balance** principle:*
> * *We begin with **49,109 raw rows** in multi-source staging.*
> * *Across the 9 steps, the engine filters and consolidates exactly **4,569 redundant and contaminated rows** (a net reduction of 9.30%): removing 995 future forecast rows, 2,780 exact duplicate rows, 15 same-source overlaps, and fusing 779 cross-source rows into 514 unique hours.*
> * *The pipeline terminates at exactly **44,540 certified clean records**, perfectly matching the Cartesian product of 20 locations multiplied by 2,227 contiguous observation hours, achieving 100% completeness, zero duplicates, zero leakage, and zero physical violations.*
>
> *Let us now examine the engineering implementation of each core step."*

---

### SLIDE 08: 2.1 MISSING RESPONSES & EMPTY RECORDS
* **Speaker:** Ho Van Nhu Y
* **Estimated Duration:** ~45 – 50 seconds
* **Visual Cues & Actions:**
  - Point to the three callouts: **11 / 100 Missing Calls**, **0 All-Empty Rows**, **42 NaN Cells -> 0**.
  - Reference the coverage matrix: WeatherAPI failures (Hanoi, Phu Loc, Phu Quoc, Ca Mau, Con Dao) and FreeOpenAPI failures (Vinh, Hue, Phan Thiet, Con Dao, Pleiku, Buon Ma Thuot).
* **Spoken Script:**
> *"In **Steps 1 and 2**, the pipeline audits request coverage and handles empty records:*
>
> * * **Missing Response Auditing:** Out of 100 API queries, 89 succeeded with HTTP 200, while 11 returned empty payloads due to provider timeouts or quota limits. WeatherAPI failed across 5 stations, and FreeOpenAPI dropped 6 stations. However, because of our multi-API architecture, all affected locations were protected by co-temporal streams from Open-Meteo and Xweather, preventing any complete loss of data for any city.*
> * * **Strict Empty-Row Filtering:** The pipeline enforces a conservative deletion rule: A record is dropped if and only if **all 6 weather variables are simultaneously NaN**. The audit revealed **zero all-empty records**.*
> * *Conversely, **14 partial records** from FreeOpenAPI lacked 3 variables (producing 42 NaN cells). Rather than discarding them and losing valid temperature and wind measurements, we retained all 14 rows, which were subsequently reconciled during multi-source sensor fusion."*

---

### SLIDE 09: 2.2 STANDARDIZE TIMESTAMPS & FORECASTS
* **Speaker:** Ho Van Nhu Y
* **Estimated Duration:** ~50 – 55 seconds
* **Visual Cues & Actions:**
  - Point to the three metric cards: **49,109 -> UTC+7**, **26 Sub-Hourly Rows (Floored :00)**, **995 Future Rows Cut**.
  - Walk through **Table 6** detailing timestamp parsing, sub-hourly alignment, and forecast filtering per endpoint group.
* **Spoken Script:**
> *"Steps 3 and 4 enforce temporal consistency, as detailed in **Table 6**:*
>
> * * **UTC+7 Standardization:** All 49,109 raw records across 4 disparate formats were parsed and mapped into the local timezone `Asia/Ho_Chi_Minh` (UTC+7).*
> * * **Sub-Hourly Flooring:** **26 off-grid records** (12 from WeatherAPI at :30/:45 and 14 from FreeOpenAPI at :29:15) were floored to the start of the hour (`:00:00`), successfully aligning them with the hourly grid.*
> * * **Future Forecast Purging (Zero Data Leakage):** By comparing the valid weather timestamp against the retrieval timestamp `collected_at`, the engine detected and purged **995 future forecast records** (795 from WeatherAPI and 200 from Open-Meteo). This reduced the dataset from 49,109 to **48,114 verified historical records**, eliminating any potential target leakage for machine learning models."*

---

### SLIDE 10: 2.3 VALIDATE PHYSICAL RANGES & EXTREMES
* **Speaker:** Ho Van Nhu Y
* **Estimated Duration:** ~55 – 60 seconds
* **Visual Cues & Actions:**
  - Point to the three callouts: **Cell-Level Masking**, **0 Out-of-Range Cells**, **2,163 Extremes Kept**.
  - Detail **Table 7** comparing WMO physical limits with observed ranges and extreme counts.
* **Spoken Script:**
> *"In **Step 5**, we deployed domain-informed physical boundary validation while safeguarding natural meteorological extremes, summarized in **Table 7**:*
>
> * * **Cell-Level Masking:** Instead of discarding an entire row when a single variable fails validation, the algorithm masks only the offending cell with NaN, preserving all remaining valid parameters on that row.*
> * * **WMO Physical Compliance:** All 267,240 observational cells across all 6 variables were validated against World Meteorological Organization thresholds. Exactly **zero out-of-range violations** occurred: air temperature remained bounded within [-10, 50]°C (observed 11.40 to 39.70°C); humidity within [0, 100]%; and precipitation contained zero negative values.*
> * * **Preserving 2,163 Natural Extremes:** Standard statistical outlier removal ($1.5 	imes 	ext{IQR}$) would erroneously discard thousands of data points during tropical storms. By grounding our thresholds in atmospheric physics, our pipeline **preserved all 2,163 genuine extreme hours** — including 479 heavy monsoon rain hours exceeding 5 mm/h (peaking at 37.40 mm/h in Ha Long) and 674 high-wind hours. This ensures that severe weather warning signals remain intact."*

---

### SLIDE 11: 2.4 DEDUPLICATION & SENSOR FUSION
* **Speaker:** Ho Van Nhu Y
* **Estimated Duration:** ~55 – 60 seconds
* **Visual Cues & Actions:**
  - Point to the three-tier hierarchy in **Table 8**: **Tier 1 (-2,780 Exact)**, **Tier 2 (-15 Same-Source)**, **Tier 3 (779 -> 514h Mean Fusion)**.
  - Explain the consensus mean formula $ar{x}_{v,l,t} = rac{1}{n} \sum_{i=1}^n x_{i,v,l,t}$.
* **Spoken Script:**
> *"Steps 6 and 7 represent the core algorithmic innovation of our pipeline: a **Three-Tier Deduplication and Sensor Fusion Hierarchy**, outlined in **Table 8**:*
>
> * * **Tier 1 (Exact Deduplication):** Removed **2,780 exact duplicate rows** generated by repeated polling cycles of Open-Meteo Forecast, reducing the count to 45,334.*
> * * **Tier 2 (Same-Source Overlaps):** Resolved **15 overlapping pairs** within WeatherAPI where live station observations clashed with hourly forecasts. We applied our `RECORD_TYPE_RANK` priority rule (prioritizing ground observations over forecasts) combined with backward filling, eliminating 15 redundant rows down to 45,319.*
> * * **Tier 3 (Multi-Source Consensus Fusion):** Across 514 location-hours where 2 to 4 independent APIs co-existed (comprising 1,293 raw rows), we computed the **consensus mean** for each meteorological variable:*
>   $$ar{x}_{v,l,t} = rac{1}{n} \sum_{i=1}^n x_{i,v,l,t}$$
>   *Simultaneously, the engine tracked provider variance and flagged **113 conflict hours** where inter-API discrepancies exceeded tolerance thresholds ($|\Delta T| > 3^\circ	ext{C}$ or $|\Delta RH| > 15\%$).*
>
> *This fused 1,293 rows into 514 hours, removing 779 rows and bringing the total to exactly **44,540 rows**."*

---

### SLIDE 12: 2.5 HOURLY GRID, CONSISTENCY & PRECISION
* **Speaker:** Ho Van Nhu Y
* **Estimated Duration:** ~50 – 55 seconds
* **Visual Cues & Actions:**
  - Point to the three refinement achievements: **20 × 2,227 = 44,540 Hourly Grid**, **125 Gust Rows Fixed**, **158,173 Float Cells Rounded**.
  - Walk through **Table 9** summarizing grid construction, aerodynamic consistency, and IEEE-754 cleanup.
  - Deliver the handover transition to Speaker 3 (Ngo Minh Triet).
* **Spoken Script:**
> *"In **Steps 8 and 9**, the pipeline completes final grid construction and physical consistency refinements, presented in **Table 9**:*
>
> * * **Continuous Hourly Grid & Bounded Imputation:** We re-indexed the dataset over the full Cartesian product of 20 locations and 2,227 continuous hours. Minor isolated gaps ($\le 6$ consecutive hours) were imputed using bounded linear interpolation, successfully reducing all 42 initial NaN cells to **0 missing values (0.00%)**.*
> * * **Aerodynamic Law Enforcement:** By aerodynamic law, instantaneous wind gusts must equal or exceed sustained wind speeds. Raw data contained 125 records violating this rule due to asynchronous sensor averaging intervals. We applied the physical constraint:*
>   $$wind\_gusts = \max(wind\_gusts, wind\_speed)$$
>   *correcting 100% of aerodynamic violations without losing valid data.*
> * * **Float32 Precision Truncation:** We eliminated IEEE-754 binary floating-point noise across **158,173 cells**, rounding all parameters to 2 decimal places.*
>
> *We now have an immaculate, 100% verified dataset. I invite **Ngo Minh Triet** to present Part 3: Empirical Quality Evaluation and Climatological Insights."*

---

### SLIDE 13: 3.1 RAW PROBLEMS DETECTED & RESOLVED (BEFORE VS. AFTER)
* **Speaker:** Ngo Minh Triet (Student ID: 245193038)
* **Estimated Duration:** ~50 – 55 seconds
* **Visual Cues & Actions:**
  - Greet the Committee and take over the presentation with confidence.
  - Point to the 4 quantitative audit badges: **49,109 -> 44,540 (-4,569 rows, -9.3%)**, **42 NaN -> 0 Cells (100% Completeness)**, **125 Gust -> 0 Errors (100% Consistency)**, and **2,163 Extremes Kept**.
  - Highlight **Figure 1** illustrating the elimination of all raw data defects.
* **Spoken Script:**
> *"Thank you, Nhu Y, and good morning, respected Committee members! My name is **Ngo Minh Triet**. I will now present **Part 3: Results, Empirical Quality Evaluation, and Analytical Insights**.*
>
> *Slide 13 and **Figure 1** provide definitive empirical proof that all raw data defects were completely resolved across the certified 44,540 output records:*
> * * **Data Volume & Integrity:** From 49,109 raw rows, our pipeline stripped out 995 future forecast leakages and 3,574 duplicate records, landing precisely on the exact mathematical grid:*
>   $$N_{total} = 20 	ext{ stations} 	imes 2,227 	ext{ hours} = 44,540 	ext{ clean rows}$$
> * * **Completeness:** All 42 initial missing cells were fully imputed, achieving **100.00% completeness across all 267,240 variable cells**.*
> * * **Physical Validity:** 100% of the 125 wind gust violations were corrected, resulting in 0 physical violations, 0 timezone offsets, and 0 float artifacts.*
> * * **Climatological Signal Preservation:** All **2,163 natural extreme weather hours** were preserved within physical bounds, ensuring high scientific fidelity."*

---

### SLIDE 14: 3.2 OUTPUT DATASET STATISTICAL PROFILE
* **Speaker:** Ngo Minh Triet
* **Estimated Duration:** ~50 – 55 seconds
* **Visual Cues & Actions:**
  - Point to the three parametric summary cards: **26.55 ± 3.72 °C** (Near-Gaussian Temperature), **82.32 ± 14.37 %** (Humid Monsoon Regime), and **Skew +8.51 | Kurt 142.9** (Heavy-Tailed Rain).
  - Walk through **Table 10** detailing all 9 parametric and non-parametric statistics (Mean, SD, Min, Q25, Median, Q75, Max, Skew, Kurt) across all 6 variables for N = 44,540 rows.
* **Spoken Script:**
> *"On the cleaned 44,540-record dataset, we conducted a comprehensive descriptive statistical analysis, presented in **Table 10**:*
>
> * * **National Mean Temperature** settled at **26.55 ± 3.72°C**, with a median of 26.80°C. Skewness was nearly zero (+0.02), indicating a near-perfect Gaussian distribution spanning from 11.40°C to 39.70°C.*
> * * **Relative Humidity** averaged **82.32 ± 14.37%** with an 85.00% median, reflecting Vietnam's tropical monsoonal climate, bounded tightly at 100.00%.*
> * * **Sea-Level Pressure** averaged **1009.5 ± 3.92 hPa**, varying between 994.7 and 1025.7 hPa.*
> * *In stark contrast, **Precipitation** exhibited an intensely right-skewed, heavy-tailed distribution with Skewness of **+8.51** and Kurtosis of **142.9**. This matches physical reality: over 75% of hours experienced little or no precipitation ($\le 0.20$ mm/h), but severe downpours surged up to 37.40 mm/h.*
> * *The bottom status badges confirm 100% compliance across all data quality criteria."*

---

### SLIDE 15: 3.3 OUTPUT VARIABLE DISTRIBUTIONS (FIGURE 2)
* **Speaker:** Ngo Minh Triet
* **Estimated Duration:** ~45 – 50 seconds
* **Visual Cues & Actions:**
  - Point to **Figure 2** showing the boxplots for all 6 meteorological parameters.
  - Highlight the contrast between symmetric parameters (Temperature, Pressure) and skewed parameters (Precipitation, Wind); show the 100% humidity cutoff and preserved storm extremes (81 km/h in Pleiku, 37.4 mm/h in Ha Long).
* **Spoken Script:**
> *"In Slide 15, **Figure 2** illustrates the boxplot distributions across all six weather variables, corroborating three key findings:*
>
> * * **Dual Physical Regimes:** Temperature and pressure exhibit symmetric distributions around their medians, reflecting regular diurnal and synoptic cycles. Conversely, wind speed, gusts, and precipitation display extensive upper outlier tails characteristic of convective storm bursts.*
> * * **Strict Physical Saturation Boundary:** The interquartile range for humidity spans 74% to 94%, with the upper whisker bounded exactly at 100.00%, proving zero sensor overshoot errors.*
> * * **Preserved Tropical Storm Peaks:** Verified severe weather events were retained, notably extreme wind gusts of **81.0 km/h in Pleiku** and intense cloudbursts of **37.4 mm/h in Ha Long**."*

---

### SLIDE 16: 3.4 INSIGHT 1: CORRELATIONS & RAINFALL
* **Speaker:** Ngo Minh Triet
* **Estimated Duration:** ~50 – 55 seconds
* **Visual Cues & Actions:**
  - Point to **Figure 3** and the multivariate correlation table.
  - Highlight the three core findings: **r = -0.66** (Clausius-Clapeyron coupling), **r = -0.49** (Thermal low trough), and the **2.74× rainfall ratio** between Vinh (1,293 mm) and Nha Trang (472 mm).
* **Spoken Script:**
> *"From this pristine dataset, we extracted **three major scientific insights**. Insight 1 examines thermodynamic coupling and cumulative rainfall on **Figure 3**:*
>
> * * **Strong Inverse Temperature–Humidity Coupling ($r = -0.66$):** This provides robust empirical validation of the Clausius-Clapeyron relation: daytime solar heating increases atmospheric water vapor holding capacity, lowering relative humidity, and vice versa at night.*
> * * **Moderate Inverse Temperature–Pressure Coupling ($r = -0.49$):** This reflects the formation of thermal low-pressure troughs over the continental landmass during hot monsoon afternoons.*
> * * **Strong Wind Speed–Gust Coupling ($r = +0.87$):** Confirms expected boundary-layer aerodynamic turbulence.*
> * * **2.74× Regional Precipitation Disparity:** Cumulative 93-day rainfall varied dramatically across stations. Monsoon gateway cities led the nation: **Vinh reached 1,293.1 mm** and **Pleiku reached 1,235.4 mm** due to Southwest monsoon winds and autumn tropical depressions. Conversely, **Nha Trang was the driest station at only 471.6 mm**, shielded by the Truong Son mountain range rain shadow."*

---

### SLIDE 17: 3.5 INSIGHT 2: 20-CITY CLIMATE PROFILE
* **Speaker:** Ngo Minh Triet
* **Estimated Duration:** ~50 seconds
* **Visual Cues & Actions:**
  - Point to **Figure 4** showing the temperature profile (Min – Mean – Max) across the 20 cities.
  - Contrast Sa Pa (mean 18.95°C) with Da Nang (mean 29.48°C) — a 10.53°C spread; highlight Con Dao's thermal stability (SD 0.88°C, 5.3°C span).
* **Spoken Script:**
> *"Insight 2 illustrates the spatial and topographical stratification across Vietnam on **Figure 4**:*
>
> * * **10.53°C National Temperature Spread:** The coolest station in Vietnam was the alpine town of **Sa Pa** at 1,545m, with a mean temperature of **18.95°C** (dropping to 11.40°C). In contrast, the warmest station was the coastal city of **Da Nang** with a mean of **29.48°C** (peaking at 39.70°C).*
> * * **Atmospheric Lapse Rate Validation:** The dataset accurately mirrors the environmental lapse rate of $-6.5^\circ	ext{C}$ per 1,000 meters elevation: Sa Pa (18.95°C), Phu Loc summit (21.86°C), Pleiku (22.66°C), and Da Lat (23.07°C) are significantly cooler than lowland plains.*
> * * **Maritime Buffering at Con Dao:** Offshore island Con Dao exhibited extreme thermal stability, with a standard deviation of only **0.88°C** and an overall range of just 5.3°C (25.5 to 30.8°C). In contrast, inland stations like Hue experienced temperature spans of up to 16.6°C."*

---

### SLIDE 18: 3.6 INSIGHT 3: CROSS-PROVIDER BIAS
* **Speaker:** Ngo Minh Triet
* **Estimated Duration:** ~55 – 60 seconds
* **Visual Cues & Actions:**
  - Point to **Figure 5** and **Table 11** comparing provider deviations against the Open-Meteo baseline.
  - Highlight the core biases: **Xweather +1.49°C warm bias**, **WeatherAPI -0.61°C cool offset**, and the **113 conflict hours (22.0%)** flagged.
* **Spoken Script:**
> *"Insight 3 carries the highest practical value for multi-API data engineering, detailed in **Figure 5** and **Table 11**: An empirical bias analysis across 514 co-temporal hours:*
>
> * * **Vaisala Xweather exhibits a Warm and Dry Bias:** Compared to Open-Meteo across 480 matched hours, Xweather reported higher temperatures by **+1.49°C** on average (Mean Absolute Deviation MAD = 1.72°C) and lower humidity by **-4.05%** (MAD = 7.64%). This reflects its live airport surface station sensors subject to local urban heat island effects.*
> * * **WeatherAPI exhibits a Cooler Model Offset:** Reporting temperatures **-0.61°C** lower (MAD = 1.44°C) and pressure **-0.69 hPa** lower, typical of regional numerical weather prediction interpolation.*
> * * **FreeOpenAPI:** Showed a modest +0.15°C temperature difference across 14 matched hours.*
> * * **Lineage & Conflict Transparency:** In **113 hours (22.0% of multi-source hours)**, inter-API differences exceeded significant thresholds ($|\Delta T| > 3^\circ	ext{C}$ or $|\Delta RH| > 15\%$). Rather than arbitrarily deleting data, our pipeline fused them via consensus mean and preserved the audit flag `cross_source_conflict = True`, providing complete transparency for downstream modelers."*

---

### SLIDE 19: 3.7 LIVE VERIFICATION ON STREAMLIT UI
* **Speaker:** Ngo Minh Triet
* **Estimated Duration:** ~45 – 50 seconds
* **Visual Cues & Actions:**
  - Direct the committee's attention to the web application preview in `app.py`.
  - Highlight three interactive modules: **Live 4-API Polling**, **Before vs After Audit View**, and **20-City Stats Explorer**.
* **Spoken Script:**
> *"To demonstrate production readiness, we packaged the entire collection and cleaning pipeline into an interactive web application built with **Streamlit** in `app.py`:*
>
> * * **Feature 1 — Live 4-API Polling:** Users can select any of the 20 cities and trigger concurrent HTTP calls across all 4 APIs, observing raw JSON payloads and API response times in real time.*
> * * **Feature 2 — Before vs After Quality Audit:** Provides an instant visual comparison of the pipeline, verifying the elimination of all 42 NaN cells and 125 physical violations.*
> * * **Feature 3 — 20-City Stats Explorer:** Allows dynamic filtering of temperature, rainfall, and correlation matrices for each station, with one-click export of clean CSV data.*
>
> *The application is live and ready for interactive demonstration during Q&A."*

---

### SLIDE 20: 3.8 SUMMARY SCORECARD & TAKEAWAYS
* **Speaker:** Ngo Minh Triet
* **Estimated Duration:** ~50 – 55 seconds
* **Visual Cues & Actions:**
  - Point to the three final pillar cards: **100% Defect Removal (Certified Gold Dataset)**, **Climatic Fidelity (2,163 Extremes Preserved)**, and **Multi-Source Lineage**.
  - Walk through **Table 12** benchmarking the raw vs. cleaned dataset across all 8 dimensions.
* **Spoken Script:**
> *"Slide 20 and **Table 12** present our comprehensive capstone scorecard across 8 dimensions of data quality:*
>
> 1. * **Record Volume:** 49,109 raw rows consolidated to **44,540 clean rows** (-9.3% redundancy removed).*
> 2. * **API Coverage:** 89/100 requests covered 100% of the spatio-temporal grid via multi-source fallback.*
> 3. * **Time & Forecasts:** 100% unified to UTC+7; 995 future forecast leakages completely excised.*
> 4. * **Duplicate Integrity:** 3,574 duplicate rows eliminated; 100% uniqueness under `(location_id, time)`.*
> 5. * **Completeness:** 42 missing cells reduced to **0 missing cells (0.00%)** across 267,240 values.*
> 6. * **Physical Laws:** 125 wind gust violations corrected; **2,163 natural storm extremes preserved**.*
> 7. * **Climatological Gradient:** Captured the 10.53°C Sa Pa–Da Nang spread and environmental lapse rates.*
> 8. * **Cross-Provider Bias:** Inter-API biases quantified and 113 conflict hours transparently flagged.*
>
> *The resulting output fully qualifies as an enterprise-grade **Gold Standard dataset**, ready for immediate analytical deployment."*

---

### SLIDE 21: CONCLUSION, DELIVERABLES CHECKLIST & Q&A
* **Speaker:** Ngo Minh Triet (joined by Giao Dang and Nhu Y)
* **Estimated Duration:** ~40 – 45 seconds
* **Visual Cues & Actions:**
  - All three members stand together, facing the Committee and Supervisor.
  - Point to the Capstone Deliverables Checklist with all 7 artifacts verified and complete.
* **Spoken Script:**
> *"Distinguished Committee members and Supervisor MSc. Truong Ba Vinh!*
>
> *On behalf of Team 3, we would like to express our deepest gratitude to MSc. Truong Ba Vinh for his expert mentorship, rigorous academic standards, and guidance throughout the Getting and Cleaning Data course.*
>
> *We have submitted a complete and fully reproducible package comprising **all 7 capstone deliverables**: including the automated collector `01`, the 9-step cleaning engine `02`, the raw staging data, the certified 44,540-record clean dataset, the automated quality report, the interactive Streamlit dashboard, and our comprehensive IEEE-formatted capstone report along with these presentation slides.*
>
> *This concludes our presentation. We warmly welcome your feedback, comments, and questions. Thank you very much!"*

---

# PHẦN 3: CÂU HỎI PHẢN BIỆN DỰ PHÒNG & HƯỚNG DẪN TRẢ LỜI (DEFENSE Q&A CHEAT SHEET)

Dưới đây là 5 câu hỏi trọng tâm mà Hội đồng phản biện thường đặt ra cho các đồ án thu thập và làm sạch dữ liệu chuỗi thời gian khí tượng, kèm theo hướng dẫn trả lời chi tiết và các con số thực nghiệm cụ thể từ đề tài:

---

### CÂU HỎI 1: TẠI SAO PHẢI CẮT BỎ 995 DÒNG DỰ BÁO TƯƠNG LAI? ĐIỀU GÌ XẢY RA NẾU KHÔNG CẮT? (DATA LEAKAGE)
* **Thành viên trả lời tốt nhất:** Hồ Văn Như Ý hoặc Nguyễn Dạ Giao Đăng.
* **Hướng dẫn trả lời:**
> *"Dạ kính thưa Thầy Cô, việc loại bỏ 995 dòng dự báo tương lai là một bước bắt buộc để ngăn chặn **Hiểm họa rò rỉ dữ liệu (Data Leakage)**.*
>
> *Trong quá trình thu thập thực tế, các API như WeatherAPI (gửi kèm 795 dòng) và Open-Meteo (gửi kèm 200 dòng) không chỉ trả về dữ liệu lịch sử mà còn tự động đính kèm dự báo thời tiết của 24 đến 72 giờ tiếp theo. Nếu nhóm không kiểm tra và để lẫn các dòng này vào tập dữ liệu quan trắc, chúng ta sẽ phạm phải sai lầm nghiêm trọng là **coi dữ liệu ước tính trong tương lai như dữ liệu thực tế trong quá khứ**.*
>
> *Khi đưa bộ dữ liệu này vào huấn luyện các mô hình Machine Learning hoặc phân tích thống kê, mô hình sẽ bị thiên lệch giả tạo (artificially high accuracy) do đã 'nhìn thấy trước tương lai'. Bằng cách đối chiếu mốc quan trắc với mốc thời gian gửi yêu cầu HTTP `collected_at` (Step 4), đường ống đã cắt bỏ chính xác 995 dòng rò rỉ này, đảm bảo 100% dữ liệu sạch đều là dữ liệu quan trắc quá khứ có thật."*

---

### CÂU HỎI 2: TẠI SAO NHÓM LẠI GIỮ LẠI 2.163 ĐIỂM CỰC ĐOAN MÀ KHÔNG DÙNG $1.5 	imes 	ext{IQR}$ ĐỂ XÓA OUTLIER?
* **Thành viên trả lời tốt nhất:** Hồ Văn Như Ý hoặc Ngô Minh Triết.
* **Hướng dẫn trả lời:**
> *"Dạ kính thưa Thầy Cô, đây là một điểm nhấn kỹ thuật quan trọng của đồ án về sự khác biệt giữa **Kiểm định miền tri thức chuyên ngành (Domain-Informed Validation)** và **Lọc thống kê mù quáng (Blind Statistical Trimming)**.*
>
> *Trong khí tượng học, các hiện tượng thời tiết nguy hiểm như mưa giông nhiệt đới hay gió lốc bản chất là các sự kiện hiếm (extreme tail events). Nếu chúng ta áp dụng máy móc quy tắc thống kê $1.5 	imes 	ext{IQR}$, toàn bộ các trận mưa lớn vượt 5 mm/h (chiếm 479 giờ, với đỉnh 37,4 mm/h tại Hạ Long) và 674 giờ gió mạnh sẽ bị gán nhãn là 'ngoại lai' và bị xóa bỏ hoặc bị cắt ngọn.*
>
> *Nếu làm như vậy, bộ dữ liệu sẽ bị 'làm mịn nhân tạo' (over-smoothed), làm mất hoàn toàn tín hiệu thiên tai và trở nên vô dụng cho các bài toán cảnh báo bão lũ. Vì vậy, nhóm đã đối chiếu từng điểm dữ liệu với **Ngưỡng giới hạn khí hậu thực tế của WMO và Việt Nam** (ví dụ nhiệt độ [-10; 50]°C, lượng mưa [0; 300] mm/h). Kết quả xác nhận 2.163 giá trị này hoàn toàn nằm trong biên vật lý tự nhiên nên nhóm đã bảo tồn nguyên vẹn 100%."*

---

### CÂU HỎI 3: KHI NHIỀU API CÙNG QUAN TRẮC MỘT GIỜ, TẠI SAO LẠI DÙNG TRUNG BÌNH CỘNG? NẾU CÓ MỘT NGUỒN SAI LỆCH THÌ SAO?
* **Thành viên trả lời tốt nhất:** Hồ Văn Như Ý hoặc Ngô Minh Triết.
* **Hướng dẫn trả lời:**
> *"Dạ kính thưa Thầy Cô, khi có từ 2 đến 4 nhà cung cấp cùng đưa ra số liệu cho một giờ tại cùng một địa điểm (514 giờ chồng lấn), việc áp dụng **Giá trị trung bình đồng thuận (Consensus Mean)** dựa trên lý thuyết tổng hợp cảm biến (Sensor Fusion) giúp giảm phương sai đo đạc ngẫu nhiên.*
>
> *Tuy nhiên, để xử lý rủi ro một nguồn bị sai lệch hệ thống, nhóm không làm trung bình đơn thuần mà bổ sung 2 cơ chế giám sát:*
> 1. * **Kiểm tra độ phân tán (`spread`):** Tính khoảng chênh lệch giữa giá trị cao nhất và thấp nhất của các nguồn cho từng biến.*
> 2. * **Gắn cờ xung đột (`cross_source_conflict`):** Nếu độ lệch nhiệt độ vượt quá 3°C hoặc độ ẩm vượt quá 15%, hệ thống sẽ tự động bật cờ cảnh báo `True` (ghi nhận trên 113 giờ). Nhờ đó, người dùng phía sau hoàn toàn có thể lọc riêng các giờ xung đột này ra để thẩm định nâng cao hoặc áp dụng trọng số chuyên gia."*

---

### CÂU HỎI 4: TẠI SAO DỮ LIỆU THÔ LẠI CÓ 125 DÒNG CÓ GIÓ GIẬT BÉ HƠN GIÓ DUY TRÌ? NHÓM ĐÃ XỬ LÝ NHƯ THẾ NÀO?
* **Thành viên trả lời tốt nhất:** Hồ Văn Như Ý hoặc Nguyễn Dạ Giao Đăng.
* **Hướng dẫn trả lời:**
> *"Dạ kính thưa Thầy Cô, theo định nghĩa khí động học WMO, **tốc độ gió duy trì (wind speed)** là vận tốc trung bình đo trong khoảng thời gian 10 phút, còn **gió giật (wind gust)** là vận tốc tức thời cực đại đo trong 3 giây của cùng khoảng thời gian đó. Do đó, về mặt vật lý, gió giật luôn luôn phải lớn hơn hoặc bằng tốc độ gió duy trì ($wind\_gusts \ge wind\_speed$).*
>
> *Hiện tượng 125 dòng thô có gió giật nhỏ hơn gió duy trì xuất hiện cục bộ từ WeatherAPI, nguyên nhân do sự không đồng bộ giữa cửa sổ lấy mẫu của thuật toán nội suy số trị.*
>
> *Để xử lý, thay vì xóa bỏ các dòng này làm đứt gãy chuỗi thời gian, nhóm áp dụng toán tử vật lý:*
> $$wind\_gusts = \max(wind\_gusts, wind\_speed)$$
> *Điều này đảm bảo tính nhất quán khí động học mà không làm sai lệch thông tin của các biến quan trắc khác trên cùng dòng."*

---

### CÂU HỎI 5: ĐƯỜNG ỐNG NÀY CÓ KHẢ NĂNG MỞ RỘNG VÀ TRIỂN KHAI THỜI GIAN THỰC HÀNG NGÀY ĐƯỢC KHÔNG?
* **Thành viên trả lời tốt nhất:** Ngô Minh Triết hoặc Nguyễn Dạ Giao Đăng.
* **Hướng dẫn trả lời:**
> *"Dạ kính thưa Thầy Cô, đồ án của nhóm được thiết kế ngay từ đầu theo **kiến trúc mô-đun hóa cao (High Modularity)** để sẵn sàng triển khai thực tế:*
>
> * * **Khả năng lập lịch tự động (Orchestration):** Hai tệp xử lý cốt lõi `01_collect_weather_data.py` và `02_clean_weather_data.py` hoàn toàn độc lập và nhận tham số từ `config/config.py`. Chúng em có thể dễ dàng gắn lịch chạy định kỳ (cron job hoặc Apache Airflow DAG) mỗi giờ một lần để tự động thu thập và tiền xử lý.*
> * * **Khả năng mở rộng địa lý:** Để thêm một thành phố mới, kỹ sư chỉ cần bổ sung tên và tọa độ vào tệp cấu hình mà không cần viết lại một dòng mã tiền xử lý nào.*
> * * **Hiển thị trực quan:** Ứng dụng Streamlit `app.py` đã chứng minh đường ống có thể nhận dữ liệu live, thực thi làm sạch ngay lập tức và phục vụ người dùng cuối thông qua giao diện tương tác trực quan."*
