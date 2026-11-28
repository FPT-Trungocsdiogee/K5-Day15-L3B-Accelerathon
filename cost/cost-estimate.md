# Chi phí khi dùng thật

> Số lấy từ `cost/simulate-1-summary.md` (lượt `simulate-1@20261128-125920`, `cost/simulate-1.csv`). Các số được tính lại từ bảng persona và giá bên dưới, khớp với bản tóm tắt.
> Lúc build dùng model đo token là `claude-haiku-5-5`, nhưng chi phí dưới đây tính theo giá gói trả phí của model khác (xem mục 1). Đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu, share cộng lại = 1.

| Persona | Tỉ lệ | Phiên / người / tháng | Lượt hỏi / phiên | Ghi chú nguồn |
|---|---|---|---|---|
| dung_it | 40% | 4 | 1 | Ghi trong yaml: khảo sát Trải nghiệm xem TKB & Tra phòng học AI20K (Responses) |
| dung_vua | 40% | 10 | 3 | như trên |
| dung_nhieu | 20% | 20 | 5 | như trên |

  Lưu ý nguồn: `spec.md` §2 ghi khảo sát **không hỏi** số lần/tháng cho phòng lý thuyết. Vì vậy cột "phiên / người / tháng" và "lượt hỏi / phiên" chưa có bằng chứng xác nhận từ khảo sát. Cần kiểm lại trước khi nộp.

- **Số người dùng thật** (3 kịch bản):
  - thấp **300** — (tự ước tính)
  - cơ sở **700** — quy mô lớp L3 hơn 700 học viên (ghi trong yaml; chưa có link)
  - cao **800** — (tự ước tính)

- **Giá** (USD / 1 triệu token, model đo token nằm ở mục sau):
  - gemini-3.1-flash-lite: vào 0.25 · ra 1.50
  - gemini-4-hydrogen: vào 1.50 · ra 7.50


- **Tỉ lệ đạt** để tính chi phí / task thành công: gemini-3.1-flash-lite,32/32

- **Đo token trên** `claude-haiku-5-5`, **tính giá** cho gemini-3.1-flash-lite và gemini-4-hydrogen. Mỗi hãng tách token khác nhau, nên số token thật khi dùng model khác có thể lệch.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-125920` · 50 phiên · seed 42 · lỗi 0/50.

Token đo được theo persona (trên `claude-haiku-5-5`):

| Persona | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|
| dung_it | 569 | 186 | 0.7 | 2.6 |
| dung_vua | 1326 | 458 | 1.6 | 7.7 |
| dung_nhieu | 2368 | 869 | 2.8 | 11.3 |

Chi phí (tính theo giá chưa xác minh ở mục 1):

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (300) | / tháng — cơ sở (700) | / tháng — cao (800) | / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.50 $/1M) | $0.0010 | — | $3.70 | $8.63 | $9.87 | $0.0123 |
| gemini-4-hydrogen (vào 1.50 · ra 7.50 $/1M) | $0.0054 | — | $19.68 | $45.91 | $52.47 | $0.0656 |
| claude-haiku-5-5 (đo token) | — | — | — | — | — | — |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. **Chưa tính được** vì chưa có tỉ lệ đạt trên model nào khớp với model đo token. Không coi như đạt 100%.
- Hàng `claude-haiku-5-5` để trống vì chưa có giá trong `prices`. Không ước giá.
- Người dùng trung bình: 0.4×4 + 0.4×10 + 0.2×20 = **9.6 phiên / người / tháng**.
- Phân bổ chi phí theo persona (cả hai model cho kết quả gần giống): dung_nhieu chiếm khoảng **61%** chi phí / người, dung_vua khoảng **33%**, dung_it khoảng **6%**. Vì vậy số phiên và lượt hỏi của nhóm nhiều nhất là yếu tố quyết định.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): **chưa tính được.** `spec.md` §2 ghi khảo sát chưa đủ dữ liệu về số lần / tháng và thời gian dò phòng.
- Chi phí / người / tháng (cơ sở): $0.0123 (gemini-3.1-flash-lite) · $0.0656 (gemini-4-hydrogen) — theo giá chưa xác minh.
- Chi phí / tháng toàn lớp (cơ sở, 700 người): khoảng $8.6 – $46 tuỳ model.
- **Kết luận một dòng — đáng làm không:** **chưa kết luận được.** Chi phí model ở mức rất thấp so với quy mô lớp, nhưng để so với impact cần (1) số người × số lần/tháng × phút tiết kiệm có nguồn trong `spec.md` §2, và (2) tỉ lệ đạt trên model thật sẽ dùng.
