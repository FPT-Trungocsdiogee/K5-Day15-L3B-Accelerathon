# Data card — dữ liệu bản chạy thử dùng

> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · Thời khoá biểu AI20K Cohort V — Phase 1 (3 bản cùng nội dung)

Ba file cùng một nguồn, ba cách trình bày: `ai20k_schedule.json` (đầy đủ: meta + nhóm + học viên), `ai20k_group_schedules.md` (bảng buổi học theo nhóm), `ai20k_student_schedule_long.csv` (mỗi dòng = một học viên × một buổi).

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ `parse_timetable` / `lookup_merged_room` · đối chiếu đáp án bộ câu thử `eval/benchmark.csv` · đào bằng chứng (`evidence/data-mining.md`) |
| Từ đâu | data BTC cấp — thời khoá biểu AI20K Cohort V (05/11–28/11/2026), đã chuyển sang JSON / MD / CSV. Bộ câu thử (`eval/benchmark.csv`) ghi nguồn gốc là file HTML `Thoi_khoa_bieu_AI20K_Cohort_V_05-29_11.html`, file này **không** nằm trong `data/` |
| Xử lý những bước gì | chuẩn hoá về 3 định dạng · mã phòng viết tắt (`H209` = H2-209) · phòng dự phòng đánh `*` / `backup:true` · phòng chưa xếp ghi `?`, buổi online / khai giảng không có phòng (`null`) · tên học viên chỉ còn dạng viết tắt (`short_name`), tên đầy đủ không có trong nguồn · lọc / ẩn danh thêm: chưa làm *(xem Giới hạn)* |
| Số dòng / số đoạn | 4 nhóm (L3A 360, L3B 361, L2A 220, L2B 142 = **1.083 học viên**) × 31 buổi/nhóm = 124 buổi (MD: 124 dòng bảng) · CSV: **33.573** dòng, 1.083 `student_id` (LAB 15.162 · LEC 11.913 · ONL 4.332 · KG 1.083 · HACK 1.083) · JSON ≈ 44 nghìn dòng |
| Phiên bản / ngày lấy | TKB Phase 1 (05/11–28/11/2026; nghỉ 23–24/11; Phase 2 từ 30/11/2026) · ngày lấy chính xác: *chưa ghi — nhóm điền* |
| Nhãn | thật (không `synthetic`) |
| Giới hạn | chỉ là TKB **đã công bố**, không chứa thông báo đổi phòng — thông tin gộp lớp về H209/H210 phải lấy từ nguồn khác · TKB có thể đổi sau ngày lấy (BTC báo qua email / Discord) · có buổi phòng `?` (chưa xếp) → không đủ căn cứ để kết luận · `student_id` + `short_name` là dữ liệu cá nhân thật → chỉ dùng để tra cứu nội bộ, không đưa vào slide / báo cáo / trace công khai, không in nguyên danh sách · chỉ 1 cohort, 1 giai đoạn nên không đại diện cho các đợt sau |

**Lưu ý commit:** file CSV / JSON có mã học viên thật; trước khi nộp / công khai repo, nhóm xác nhận với BTC được phép giữ trong repo, hoặc thay bằng bản cắt ngắn / mã giả.
