# codebase/ — lệnh kiểm tra từng module

Lát cắt (spec.md §4): người vận hành lớp đưa **một ngày** → luồng đánh dấu buổi lý thuyết ở phòng lẻ H2xx là
*đổi phòng → H209/H210* · *giữ nguyên* · *chưa chắc* → bản nháp TKB HTML chờ duyệt.

Chạy mọi lệnh từ **thư mục gốc repo** (macOS/Linux có thể là `python3`, Windows có thể là `py`).

## Từng module

| Module | Lệnh | Kiểm gì |
|---|---|---|
| `tools.py` | `python codebase/tools.py` | `normalize_date` · `parse_timetable` (13/11, ngày nghỉ 23/11, input sai) · `lookup_merged_room` (file mẫu, file thiếu) · `render_marked_timetable` (nhãn bản nháp, escape HTML) |
| `agent.py` (tự kiểm) | `python codebase/agent.py --selftest` | luồng chính với model giả có kịch bản: đổi phòng đúng · chặn sai phòng · chặn mã căn cứ bịa · chặn căn cứ mâu thuẫn · không căn cứ → chưa chắc · từ chối ngoài phạm vi · hỏi lại khi thiếu ngày · ngày nghỉ. Không tốn token |
| `agent.py` (một yêu cầu) | `python codebase/agent.py "13/11 lớp L3A"` | chạy `answer()` một lần với model theo `.env`, in kết quả + số lần gọi model / công cụ / token |
| `ai.py` | xem `docs/connect-model.md` | nối model; chưa có `.env` thì chạy chế độ giả |
| cả bản chạy thử | `python run.py` | giao diện dòng lệnh của khung (`app.py` → `agent.answer`) |

Bản nháp HTML được lưu ở `drafts/tkb-<ngày>[-<lớp>].html` (đã gitignore) — mở bằng trình duyệt để xem 3 màu.

## Dữ liệu và biến môi trường

| Biến | Mặc định | Ghi chú |
|---|---|---|
| `TIMETABLE_FILE` | `data/ai20k_schedule.json` | TKB đã công bố. spec ghi "TKB HTML" nhưng file HTML không có trong `data/` nên đọc bản JSON cùng nội dung |
| `MERGED_ROOMS_FILE` | `data/merged_rooms.json` | thông tin gộp lớp về H209/H210 — **nhóm tự điền từ thông báo thật**, kèm nguồn. Chưa có file → mọi buổi phòng lẻ H2xx thành "chưa chắc" |

`data/merged_rooms.sample.json` là **dữ liệu giả** (ghi `"synthetic": true`), chỉ để tự kiểm / demo. Dùng thử:

```
# PowerShell
$env:MERGED_ROOMS_FILE="data/merged_rooms.sample.json"; python codebase/agent.py "13/11"
# bash
MERGED_ROOMS_FILE=data/merged_rooms.sample.json python codebase/agent.py "13/11"
```

Không đặt biến này khi chạy `python run.py eval` / `simulate` — lượt tính điểm không được dùng dữ liệu giả.

## Cả bộ (lệnh của khung)

```
python run.py check              # kiểm eval/benchmark.csv + eval/metric_spec.yaml
python run.py eval --try         # thử 3 câu đầu
python run.py eval               # cả bộ → eval/run-N.csv + traces/run-N.jsonl
python run.py score eval/run-N.csv
python run.py simulate --try     # thử mô phỏng chi phí 10 phiên
python run.py simulate           # → cost/simulate-N.csv
```
