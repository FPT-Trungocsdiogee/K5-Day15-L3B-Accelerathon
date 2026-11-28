# Tóm tắt mô phỏng simulate-2@20261128-143924

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 16 | 1 | 378 | 56 | 0.6 | 2.5 |
| dung_vua | 19 | 3 | 953 | 138 | 1.6 | 7.9 |
| dung_nhieu | 11 | 5 | 1609 | 231 | 2.6 | 11.3 |

Tỉ lệ đạt dùng để tính: 32/32 (100%) — lượt run-2@20261128-120915

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (300 người) | Chi phí / tháng — cơ sở (700 người) | Chi phí / tháng — cao (800 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00043 | $0.00043 | $0.00015 | $1.52 | $3.55 | $4.05 | $0.0051 |
| gemini-3.5-flash-lite (vào 0.3 · ra 2.5 $/1M) | $0.00060 | $0.00060 | $0.00022 | $2.15 | $5.02 | $5.74 | $0.0072 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.8) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.5-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 4/50.
