# Thiết kế Interface cho Dịch vụ AI / LLM (AI Service Interface Specification)

Tài liệu này xác định đặc tả giao diện (Interface Contract) cho dịch vụ AI / LLM trong kiến trúc của **Smart Virtual Assistant** (Nhóm 07 - FIT HCMUS).

Mục tiêu: Cung cấp bản thiết kế trừu tượng độc lập với nhà cung cấp LLM cụ thể (OpenAI, Anthropic, Gemini, hay mô hình cục bộ). Giao diện này chuẩn hóa cách giao tiếp giữa bộ điều phối chính (Assistant Core / Dispatcher) và tầng xử lý AI ngữ nghĩa trong tương lai (Tuần 4+).

---

## 1. Vị trí trong kiến trúc hệ thống

```
User Query ---> Dispatcher / Rule Engine
                     │
                     ├── [Query xác định / Tra cứu CSV] ---> Trả lời ngay (rules.py)
                     │
                     └── [Query ngữ nghĩa / Cần AI]     ---> AIService Interface (ai_interface)
                                                                    │
                                                                    └── Future LLM Provider / Mock
```

- Các câu hỏi dạng tra cứu thông tin tĩnh (`Where is Library?`, `help`, `quit`) tiếp tục được xử lý bởi `rules.py`.
- Các câu hỏi ngữ nghĩa phức tạp (đã được phân loại trong [ai-or-not.md](ai-or-not.md)) sẽ được chuyển tiếp qua `AIService`.

---

## 2. Kiểu dữ liệu & Chữ ký hàm (Data Types & Function Signature)

### 2.1 Định nghĩa kiểu dữ liệu (Python Type Definitions)

Sử dụng `dataclasses` hoặc `typing.TypedDict` chuẩn của Python để đảm bảo tính chặt chẽ:

```python
from dataclasses import dataclass, field
from typing import List, Optional, Protocol


@dataclass(frozen=True)
class AIRequest:
    """Đầu vào gửi đến dịch vụ AI."""

    query: str
    context: List[str] = field(default_factory=list)
    session_id: Optional[str] = None
    temperature: float = 0.3
    max_tokens: int = 500
    timeout_seconds: float = 10.0


@dataclass(frozen=True)
class AIResponse:
    """Đầu ra chuẩn hóa nhận từ dịch vụ AI."""

    answer: str
    sources: List[str] = field(default_factory=list)
    model_name: str = "mock-ai-v1"
    tokens_used: int = 0
    latency_seconds: float = 0.0
    is_fallback: bool = False
    finish_reason: str = "stop"  # "stop" | "length" | "error" | "fallback"
```

### 2.2 Chữ ký hàm (Function Signatures & Protocol)

Giao diện được trừu tượng hóa dưới dạng một `Protocol` (Interface):

```python
class AIService(Protocol):
    """Giao diện chuẩn của dịch vụ AI."""

    def query(self, request: AIRequest) -> AIResponse:
        """Xử lý câu hỏi của người dùng và trả về phản hồi chuẩn hóa.

        Args:
            request: Đối tượng AIRequest chứa câu hỏi và ngữ cảnh.

        Returns:
            AIResponse: Kết quả sinh câu trả lời hoặc phản hồi fallback.

        Raises:
            AIServiceError: Các lỗi nghiêm trọng nếu không thể tự fallback.
        """
        ...
```

---

## 3. Đặc tả đầu vào (Inputs Specification)

| Trường dữ liệu | Kiểu dữ liệu | Bắt buộc | Mặc định | Mô tả & Ràng buộc |
| :--- | :--- | :---: | :--- | :--- |
| `query` | `str` | **Có** | - | Câu hỏi ngôn ngữ tự nhiên của người dùng. Không được rỗng hoặc chỉ chứa khoảng trắng. Tối đa 1.000 ký tự. |
| `context` | `List[str]` | Không | `[]` | Danh sách các đoạn văn bản trích xuất từ tài liệu/CSV liên quan (hỗ trợ mô hình RAG). |
| `session_id` | `Optional[str]` | Không | `None` | Mã định danh phiên hội thoại để theo dõi ngữ cảnh đối thoại nhiều lượt. |
| `temperature` | `float` | Không | `0.3` | Độ sáng tạo của mô hình (từ `0.0` đến `1.0`). Khuyến nghị mức thấp (`0.2` - `0.3`) để hạn chế ảo giác trong môi trường học thuật/thư viện. |
| `max_tokens` | `int` | Không | `500` | Giới hạn độ dài token sinh ra (1 - 2.000 tokens) để kiểm soát chi phí và độ trễ. |
| `timeout_seconds` | `float` | Không | `10.0` | Thời gian chờ phản hồi tối đa trước khi kích hoạt cơ chế fallback. |

---

## 4. Đặc tả đầu ra (Outputs Specification)

| Trường dữ liệu | Kiểu dữ liệu | Ý nghĩa | Ví dụ |
| :--- | :--- | :--- | :--- |
| `answer` | `str` | Câu trả lời ngôn ngữ tự nhiên gửi tới người dùng. | `"Bạn có thể tham khảo cuốn 'Clean Code' tại kệ B.201..."` |
| `sources` | `List[str]` | Nguồn tham chiếu/trích dẫn dùng để tạo câu trả lời. | `["data/offices.csv", "docs/library-handbook.md"]` |
| `model_name` | `str` | Tên mô hình hoặc backend đã xử lý yêu cầu. | `"gpt-4o-mini"`, `"claude-3-haiku"`, `"mock-v1"` |
| `tokens_used` | `int` | Tổng số token đã tiêu thụ (prompt + completion). | `142` |
| `latency_seconds` | `float` | Thời gian thực thi phản hồi (tính bằng giây). | `0.85` |
| `is_fallback` | `bool` | Cờ đánh dấu câu trả lời có phải được sinh từ bộ dự phòng hay không. | `False` (bình thường) hoặc `True` (khi gặp sự cố) |
| `finish_reason` | `str` | Lý do kết thúc sinh văn bản. | `"stop"`, `"length"`, `"fallback"` |

### Ví dụ dữ liệu đầu ra dạng JSON:

```json
{
  "answer": "Để bắt đầu học Python cho người mới, bạn nên mượn cuốn 'Automate the Boring Stuff with Python' tại khu B.201 hoặc sách giáo trình cơ sở lập trình tại Thư viện.",
  "sources": ["data/books.csv", "Library Policy"],
  "model_name": "mock-ai-v1",
  "tokens_used": 95,
  "latency_seconds": 0.42,
  "is_fallback": false,
  "finish_reason": "stop"
}
```

---

## 5. Xử lý lỗi (Error Handling & Exceptions)

Cây phân cấp ngoại lệ được thiết kế kế thừa từ `AIServiceError`:

```
AIServiceError (Base)
├── AIServiceConfigurationError  (Thiếu API key, URL cấu hình sai)
├── AIServiceTimeoutError        (Quá thời gian timeout chờ phản hồi)
├── AIServiceRateLimitError      (Hết hạn mức API hoặc bị chặn tần suất gọi)
├── AIServiceInvalidInputError   (Input vượt quá token limit hoặc sai format)
└── AIServiceUpstreamError       (Lỗi 5xx từ phía máy chủ nhà cung cấp AI)
```

### Nguyên tắc xử lý lỗi an toàn:
1. **Bảo mật tuyệt đối:** Không bao giờ in trực tiếp API Key, token hoặc thông tin nhạy cảm vào thông báo ngoại lệ hay log công khai.
2. **Không crash ứng dụng:** Các ngoại lệ từ phía AI upstream sẽ được bắt ở tầng service và chuyển đổi thành phản hồi dự phòng (Fallback Response).

---

## 6. Chiến lược dự phòng (Fallback Strategy)

Khi dịch vụ AI bên ngoài gặp sự cố (mất mạng, hết token, quá tải, lỗi phản hồi), hệ thống tuân thủ quy trình dự phòng 3 bước:

```
[Call AI Provider]
        │
        ├── Thành công  ───────────────────────────────> Trả về AIResponse (is_fallback=False)
        │
        └── Thất bại (Timeout / RateLimit / Network)
                │
                ├── Retry (tối đa 1 lần, backoff 1s)
                │      │
                │      └── Thành công ─────────────────> Trả về AIResponse (is_fallback=False)
                │
                └── Thất bại hoàn toàn
                       │
                       └── Kích hoạt Fallback Routine
                              │
                              └── Trả về AIResponse dự phòng (is_fallback=True, finish_reason="fallback")
```

### Nội dung phản hồi dự phòng mẫu:

```python
FALLBACK_MESSAGE = (
    "Hiện tại dịch vụ trợ lý AI đang bận hoặc gián đoạn kết nối. "
    "Bạn có thể tra cứu nhanh thông tin phòng ban bằng cách hỏi trực tiếp "
    "(ví dụ: 'Where is the Library?') hoặc nhập 'help' để xem danh sách lệnh."
)


def create_fallback_response(query: str, reason: str) -> AIResponse:
    return AIResponse(
        answer=FALLBACK_MESSAGE,
        sources=["system/fallback"],
        model_name="rule-fallback",
        tokens_used=0,
        latency_seconds=0.0,
        is_fallback=True,
        finish_reason="fallback",
    )
```

---

## 7. Triển khai Mock phục vụ kiểm thử (Mock Implementation)

Để phục vụ kiểm thử tự động `pytest` trong Lab 2 và Lab 3 khi chưa tích hợp API thật, lớp `MockAIService` được đề xuất như sau:

```python
class MockAIService:
    """Mock AI Service phục vụ kiểm thử đơn vị độc lập với API ngoài."""

    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail

    def query(self, request: AIRequest) -> AIResponse:
        if not request.query or not request.query.strip():
            raise ValueError("Query cannot be empty.")

        if self.should_fail:
            return create_fallback_response(request.query, reason="simulated error")

        return AIResponse(
            answer=f"[Mock AI] Phản hồi giả lập cho câu hỏi: '{request.query}'",
            sources=["mock-knowledge-base"],
            model_name="mock-ai-v1",
            tokens_used=42,
            latency_seconds=0.01,
            is_fallback=False,
            finish_reason="stop",
        )
```

---

## 8. Tuân thủ Definition of Done

- [x] Đầy đủ chữ ký hàm (`function signature`), kiểu dữ liệu đầu vào (`inputs`), đầu ra (`outputs`).
- [x] Phân cấp lỗi chi tiết (`errors`) và chiến lược dự phòng rõ ràng (`fallback`).
- [x] Không gọi API thật, không chứa secret/API key.
- [x] Tương thích với kiến trúc hiện tại của dự án và kết quả nghiên cứu của Issue #18.
