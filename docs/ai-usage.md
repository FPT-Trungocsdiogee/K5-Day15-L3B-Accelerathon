# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử (`codebase/tools.py`, `agent.py`, `ai.py`) | __ *(nhóm điền tên công cụ)* | __ | __ | Nguyễn Văn Anh Trung (`tools.py`, `agent.py`); Triệu Tuấn Minh (`ai.py`) |
| Prompt / thiết kế lời gọi mô hình | __ | __ | __ | Nguyễn Văn Anh Trung |
| Đào data (đếm phản hồi khảo sát, đếm buổi lệch phòng — `evidence/data-mining.md`) | __ | __ (số liệu đếm bằng công thức Google Sheets ghi trong file) | Kiểm tay __ dòng, khớp __ | Triệu Tuấn Minh |
| Rà câu hỏi phỏng vấn / khảo sát | __ | Chỉ rà câu dẫn dắt | __ | Triệu Tuấn Minh |
| Viết câu thử (`eval/benchmark.csv`, `eval/metric_spec.yaml`) | __ | __ | Mỗi câu thử có `source` (hiện 23 câu có nguồn `data_that`: Thoi_khoa_bieu_AI20K_Cohort_V_05-29.11.html); câu thử AI viết: __ | Trần Văn Tuấn |
| Sinh data `synthetic` (nếu có) | __ *(ghi "Không dùng" nếu không có)* | __ | Seed __ · kiểm tay __ dòng | __ |
| Chấm cột `pass` bằng LLM (nếu có) | __ *(ghi "Không dùng" nếu chấm tay)* | __ | Kiểm tra thủ công __ câu thử, khớp __/__ | Trần Văn Tuấn |
| Slide, văn bản (spec, canvas, reflection, slides) | __ | __ | __ | Triệu Tuấn Minh (slides, reflection, spec §0–§2); Đỗ Quang Vinh (spec §3, §9); Nguyễn Văn Anh Trung (canvas, spec §4–§7, §10) |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
