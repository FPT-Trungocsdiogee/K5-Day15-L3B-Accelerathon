# codebase/ — lệnh kiểm tra từng module

Lát cắt (spec.md §4): **học viên L3A/L3B** nhập mã học viên + **một ngày học lý thuyết** → luồng đánh dấu từng buổi
lý thuyết ở phòng lẻ H2xx là *đổi phòng → H209/H210* · *giữ nguyên* · *chưa chắc* → TKB ngày đó của học viên,
~~phòng cũ~~ → phòng mới, kèm mã căn cứ để tự kiểm.

Chạy mọi lệnh từ **thư mục gốc repo** (macOS/Linux có thể là `python3`, Windows có thể là `py`).

## Từng module

| Module | Lệnh | Kiểm gì |
|---|---|---|
| `tools.py` | `python codebase/tools.py` | chuẩn hoá ngày / mã học viên (`2a…` → `2A…`) · `find_student` (mã không tồn tại) · `parse_timetable` (chỉ buổi của học viên đó, ngày nghỉ, phòng dự phòng) · `lookup_merged_room` (trong khoảng, ngoài khoảng, mâu thuẫn, dự kiến, không căn cứ) · `render_marked_timetable` (gạch phòng cũ → phòng mới, escape HTML) |
| `agent.py` (tự kiểm) | `python codebase/agent.py --selftest` | chạy **cả 32 câu** của `eval/benchmark.csv` với model **stub** (làm đúng luật, không phải model thật): so trạng thái + phòng mới với `expected`, câu từ chối / hỏi lại không chứa mã phòng. Sau đó stub **cố tình sai** để kiểm lớp chặn (sai phòng · mâu thuẫn · dự kiến → chưa chắc). Không tốn token |
| `agent.py` (một câu) | `python codebase/agent.py "Mình là 2A202603520, ngày 09/11 mình có buổi lý thuyết nào đổi phòng không?"` | chạy `answer()` một lần với model theo `.env`, in kết quả + số lần gọi model / công cụ / token |
| `ai.py` | xem `docs/connect-model.md` | nối model; chưa có `.env` thì chạy chế độ giả → buổi cần model quyết thành "chưa chắc" |
| cả bản chạy thử | `python run.py` | giao diện dòng lệnh của khung (`app.py` → `agent.answer`) |

Trang TKB đánh dấu được lưu ở `drafts/tkb-<ngày>-<mã>.html` (đã gitignore) — mở bằng trình duyệt để xem 3 màu.

**Selftest qua ≠ đạt chuẩn.** Stub chỉ kiểm phần quanh model (đọc TKB, tra căn cứ, chặn, hiển thị). Kết quả tính điểm
phải lấy từ `python run.py eval` với model thật.

## Dữ liệu và biến môi trường

| Biến | Mặc định | Ghi chú |
|---|---|---|
| `STUDENT_SCHEDULE_FILE` | `data/ai20k_student_schedule_long.csv` | phòng của từng học viên từng buổi |
| `TIMETABLE_FILE` | `data/ai20k_schedule.json` | để biết phòng dự phòng (`backup`) và ngày nghỉ lễ |
| `MERGED_ROOMS_FILE` | `eval/merged_room_fixture.csv` | thông tin gộp phòng GOP-xx: `code, lop, tu_ngay, den_ngay, do_chac (xac_nhan/du_kien), phong_cu, phong_moi (H209/H210/GIU), text`. Nguồn ghi `tu_viet` trong `eval/benchmark.csv` — xem `data/DATA_CARD.md` |

## Cả bộ (lệnh của khung)

```
python run.py check              # kiểm eval/benchmark.csv + eval/metric_spec.yaml
python run.py eval --try         # thử 3 câu đầu
python run.py eval               # cả bộ → eval/run-N.csv + traces/run-N.jsonl
python run.py score eval/run-N.csv
python run.py simulate --try     # thử mô phỏng chi phí 10 phiên
python run.py simulate           # → cost/simulate-N.csv
```
