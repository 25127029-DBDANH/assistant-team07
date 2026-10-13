# Bảng phân loại câu hỏi: Cần AI vs Không cần AI (AI vs Non-AI Queries)

Tài liệu này phục vụ cho việc thiết kế kiến trúc xử lý của **Smart Virtual Assistant** (Trợ lý ảo hỗ trợ học tập & thư viện trường ĐH Khoa học Tự nhiên, ĐHQG-HCM). 

Mục tiêu là phân định rõ ràng giữa các yêu cầu có thể giải quyết bằng **quy tắc / tra cứu dữ liệu (Rule-based / Database Lookup)** và các yêu cầu thực sự cần đến **trí tuệ nhân tạo (AI / LLM Service)** nhằm tối ưu hóa chi phí tính toán, độ trễ và tránh hiện tượng ảo giác (hallucination).

---

## 1. 10 câu hỏi KHÔNG cần AI (Non-AI / Rule-based / Database Lookup)

Các câu hỏi này có dữ liệu nguồn dạng bảng cấu trúc (CSV, database), câu trả lời là sự thật xác định (deterministic) hoặc là các lệnh điều khiển hệ thống cố định.

| STT | Câu hỏi người dùng (Query) | Phân loại xử lý | Lý do không cần AI (One-line Reason) |
|:---:|:---|:---|:---|
| 1 | "Phòng đào tạo ở đâu?" | Tra cứu vị trí phòng ban | Dữ liệu phòng ban và vị trí là thông tin tĩnh, tra cứu trực tiếp từ file `data/offices.csv` bằng so khớp từ khóa. |
| 2 | "Thư viện mở cửa lúc mấy giờ?" | Tra cứu thời gian làm việc | Giờ hoạt động của thư viện là thông tin cấu trúc cố định, lấy trực tiếp từ database/CSV không cần suy luận. |
| 3 | "Cho tôi số điện thoại / email của IT Helpdesk." | Tra cứu liên hệ | Dữ liệu thông tin liên lạc là các trường dữ liệu cố định trong danh bạ nội bộ. |
| 4 | "Kiểm tra sách mã ISBN 978-0132350884 còn trong kho không?" | Tra cứu trạng thái sách theo mã | Truy vấn chính xác (exact lookup) theo khóa chính trên cơ sở dữ liệu quản lý thư viện. |
| 5 | "Sinh viên được mượn tối đa bao nhiêu cuốn sách cùng lúc?" | Tra cứu quy định định lượng | Định mức mượn sách là con số quy định bất biến trong sổ tay sinh viên, lưu trong bảng thông số chính sách. |
| 6 | "Phí phạt trễ hạn mượn sách 1 ngày là bao nhiêu tiền?" | Tra cứu bảng giá / quy chế phạt | Mức phí phạt được quy định rõ ràng bằng một hằng số cụ thể trong quy chế thư viện. |
| 7 | "Hạn trả sách của sinh viên mã số 25127345 là ngày nào?" | Tra cứu thông tin cá nhân theo ID | Truy vấn bảng giao dịch mượn/trả trong database theo MSSV, trả về ngày tháng chính xác 100%. |
| 8 | "Hôm nay phòng tự học B.201 có mở cửa không?" | Kiểm tra lịch hoạt động theo ngày | So sánh ngày giờ hiện tại của hệ thống với lịch trực cố định mà không cần xử lý ngôn ngữ phức tạp. |
| 9 | "help" (hoặc "bot có thể làm được những gì?") | Lệnh điều hướng hệ thống | Lệnh hệ thống trả về danh sách các chức năng có sẵn thông qua một hàm cố định. |
| 10 | "quit" / "exit" / "tạm biệt" | Lệnh kết thúc phiên làm việc | Lệnh điều khiển luồng chương trình (flow control) được xử lý ngay lập tức bằng điều kiện `if/else`. |

---

## 2. 10 câu hỏi CẦN dùng AI (AI / LLM-powered / Semantic Reasoning)

Các câu hỏi này đòi hỏi hiểu ngữ nghĩa tự nhiên, xử lý thông tin mơ hồ, suy luận đa bước, tóm tắt hoặc sinh nội dung mới mà hệ thống quy tắc (rule-based) không thể giải quyết được.

| STT | Câu hỏi người dùng (Query) | Năng lực AI cần dùng | Lý do cần AI (One-line Reason) |
|:---:|:---|:---|:---|
| 1 | "Tôi là sinh viên năm nhất mất gốc lập trình, gợi ý cho tôi 3 cuốn sách phù hợp để bắt đầu học Python." | Gợi ý cá nhân hóa (Recommendation) | Đòi hỏi hiểu trình độ, mục tiêu của người học và suy luận độ khó của tài liệu thay vì chỉ tìm từ khóa "Python". |
| 2 | "Tóm tắt ngắn gọn các luận điểm chính trong chương 3 của cuốn Clean Code." | Tóm tắt văn bản (Summarization) | Cần đọc hiểu nội dung văn bản phi cấu trúc dài và cô đọng ý chính bằng ngôn ngữ tự nhiên. |
| 3 | "So sánh ưu nhược điểm giữa cơ sở dữ liệu SQL và NoSQL dựa trên tài liệu trong thư viện." | Phân tích & tổng hợp thông tin | Cần tổng hợp tri thức từ nhiều nguồn tài liệu và trình bày lập luận so sánh có cấu trúc logic. |
| 4 | "Tìm sách nói về trí tuệ nhân tạo nhưng viết dễ hiểu, có nhiều ví dụ thực tế cho người mới." | Tìm kiếm ngữ nghĩa (Semantic Search) | Người dùng tìm kiếm bằng cảm xúc và tiêu chí trừu tượng ("dễ hiểu", "nhiều ví dụ"), không thể khớp chuỗi chính xác. |
| 5 | "Tôi muốn làm đồ án chatbot tư vấn học tập thì nên mượn những tài liệu nào và cần lộ trình kiến thức gì?" | Lập luận & tư vấn lộ trình học tập | Đòi hỏi AI phân tích bài toán lớn thành các mảng kiến thức nhỏ và đề xuất tài liệu tương ứng. |
| 6 | "Giải thích khái niệm Dependency Injection bằng một ví dụ đời sống thực tế cho người mới học." | Sáng tạo & giải thích thích ứng | Cần khả năng sư phạm sáng tạo, dùng phép ẩn dụ đời thường để diễn đạt một khái niệm kỹ thuật trừu tượng. |
| 7 | "Cuốn sách 'Designing Data-Intensive Applications' có phù hợp cho sinh viên ôn thi chứng chỉ AWS không, tại sao?" | Đánh giá độ tương quan ngữ cảnh | Cần hiểu nội dung sách và so sánh với phạm vi kiến thức của kỳ thi chứng chỉ để đưa ra nhận định khách quan. |
| 8 | "Dịch đoạn trích dẫn này sang tiếng Việt chuyên ngành Khoa học Máy tính giúp tôi." | Dịch thuật chuyên ngành | Yêu cầu hiểu sâu thuật ngữ chuyên ngành công nghệ thông tin trong ngữ cảnh học thuật để dịch chính xác. |
| 9 | "Tạo định dạng trích dẫn chuẩn APA 7 cho cuốn sách X của tác giả Y xuất bản năm Z." | Trích xuất và định dạng văn bản | Cần trích xuất thông tin thư tịch và sinh chuỗi văn bản theo đúng chuẩn quy tắc trích dẫn học thuật. |
| 10 | "Tôi nhớ có một cuốn sách bìa màu xanh dương về toán rời rạc thầy từng nhắc trên lớp, đó là cuốn nào?" | Suy luận từ miêu tả mơ hồ | Phải suy luận từ các manh mối mờ nhạt và ngữ cảnh bài giảng để đưa ra dự đoán hợp lý nhất. |

---

## 3. Tiêu chí tổng kết (Decision Criteria)

| Tiêu chí | Giải pháp Rule-based / Database (Non-AI) | Giải pháp AI / LLM Service |
|:---|:---|:---|
| **Bản chất dữ liệu** | Dữ liệu có cấu trúc (bảng, CSV, database), hằng số, quy chế. | Dữ liệu văn bản phi cấu trúc, tài liệu dài, ngữ cảnh mở. |
| **Tính chất câu trả lời** | 100% xác định, chính xác tuyệt đối, không được sai lệch. | Mang tính giải thích, tổng hợp, sáng tạo, tư vấn. |
| **Độ trễ & Chi phí** | Cực thấp (< 5ms), chạy trên CPU máy cục bộ, chi phí 0đ. | Cao hơn (500ms - vài giây), cần API token hoặc GPU. |
| **Rủi ro ảo giác (Hallucination)** | 0% (dữ liệu có sao trả lời vậy, không bị bịa đặt). | Có thể xảy ra, cần kỹ thuật Prompt Engineering hoặc RAG để kiểm soát. |
