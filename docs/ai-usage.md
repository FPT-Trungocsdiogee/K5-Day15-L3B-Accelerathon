# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.
>
> Ô ghi `__` là chỗ nhóm chưa xác nhận được từ repo — người phụ trách điền trước CP4. Không suy đoán thay nhóm.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử (`codebase/tools.py`, `agent.py`, `ai.py`) | `ai.py`: Claude Code (coding agent, theo `AGENTS.md`). `tools.py`, `agent.py`: __ | `ai.py`: viết lời gọi Gemini REST theo `docs/connect-model.md`, đọc token từ `usageMetadata`. `tools.py`, `agent.py`: __ | `ai.py`: chọn mã model từ danh sách model thật của key, không lấy theo tên AI đoán; chạy `eval --try` kiểm token > 0. Lượt 1 và 2 kiểm lại bằng `score` và đọc output (32/32 mỗi lượt) | Nguyễn Văn Anh Trung (`tools.py`, `agent.py`); Triệu Tuấn Minh (`ai.py`) |
| Prompt / thiết kế lời gọi mô hình | __ | Prompt `SYSTEM` trong `codebase/agent.py`: trả JSON, `temperature` 0. Ranh giới "model quyết / code quyết" do nhóm đặt trong `spec.md` §4 | Đọc lại output từng câu trong `traces/run-1.jsonl`; 18/32 câu không qua model (luật code); lớp `guard()` chặn trước khi hiện | Nguyễn Văn Anh Trung |
| Model chạy trong bản chạy thử (runtime, không phải dùng để viết code) | Gemini: `gemini-3.1-flash-lite` (lượt 1), `gemini-3.5-flash-lite` (lượt 2) | Quyết định *đổi / giữ / chưa chắc* cho buổi lý thuyết có căn cứ; không tự chọn công cụ, không tự xếp phòng mới | Code kiểm mã căn cứ, phòng đích, khoảng ngày trước khi hiện; nhóm chấm tay 32/32 mỗi lượt | Triệu Tuấn Minh (`ai.py`); Nguyễn Văn Anh Trung (thiết kế luồng) |
| Đào data (đếm phản hồi khảo sát, đếm buổi lệch phòng — `evidence/data-mining.md`) | Google Sheets (công thức `COUNTIFS` ghi trong file). Có dùng AI để đọc bảng: __ | Đếm bằng công thức. Tần suất phòng lý thuyết đếm từ TKB đã lưu (`evidence/data-mining.md` mục 6) | Kiểm tay __ dòng, khớp __ | Triệu Tuấn Minh |
| Rà câu hỏi phỏng vấn / khảo sát | __ | __ | __ | Triệu Tuấn Minh |
| Viết câu thử (`eval/benchmark.csv`, `eval/metric_spec.yaml`) | __ | __ | Mỗi câu thử có `source`: 23/32 câu có nguồn `data_that` (TKB `Thoi_khoa_bieu_AI20K_Cohort_V_05-29.11.html`), 9 câu `tu_viet`. Câu thử AI viết: __ | Trần Văn Tuấn |
| Sinh data `synthetic` (nếu có) | __ *(ghi "Không dùng" nếu không có; `run.py check` ghi `sinh_seed` 0 trong bộ câu thử)* | __ | Seed __ · kiểm tay __ dòng | __ |
| Chấm cột `pass` bằng LLM (nếu có) | Không dùng | — | Chấm tay theo `pass_criterion` (`eval/report.md`, lượt 1 và lượt 2). Người thứ hai chấm thử 5 output: chưa làm | Trần Văn Tuấn |
| Slide, văn bản (spec, canvas, reflection, slides) | __ *(AI soạn nháp `spec.md` §5, §6, §10 từ `eval/run-1.csv` và `traces/run-1.jsonl`)* | Soạn nháp các mục trên; phần còn lại do người viết | Người phụ trách mục đó đọc lại và sửa; Trung rà §5–§7, §10 | Triệu Tuấn Minh (slides, reflection, spec §0–§2); Đỗ Quang Vinh (spec §3, §9); Nguyễn Văn Anh Trung (canvas, spec §4–§7, §10) |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
