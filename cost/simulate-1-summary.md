# Tóm tắt mô phỏng simulate-1@20261128-125920

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 18 | 1 | 569 | 186 | 0.7 | 2.6 |
| dung_vua | 20 | 3 | 1326 | 458 | 1.6 | 7.7 |
| dung_nhieu | 12 | 5 | 2368 | 869 | 2.8 | 11.3 |

Tỉ lệ đạt dùng để tính: **chưa có** lượt eval chấm xong chạy bằng claude-haiku-5-5. Lượt chấm gần nhất (run-1@20261128-081816) chạy bằng gemini-3.1-flash-lite — model khác, nên KHÔNG dùng tỉ lệ đạt đó → chưa tính chi phí / task thành công. Chạy `python run.py eval` bằng đúng model này, chấm xong (`python run.py score …`) rồi chạy lại simulate.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (300 người) | Chi phí / tháng — cơ sở (700 người) | Chi phí / tháng — cao (800 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0010 | — | — | $3.70 | $8.63 | $9.87 | $0.0123 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0054 | — | — | $19.68 | $45.91 | $52.47 | $0.0656 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.8) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: claude-haiku-5-5. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
