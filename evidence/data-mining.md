# Đào data — phân tích bảng phản hồi khảo sát

> Cập nhật 27/11/2026. Đây là phân tích định lượng lại cùng bảng khảo sát ở `evidence/summary.md`, không phải một nguồn người dùng độc lập thứ hai. Số liệu là snapshot 23 phản hồi hiện có; nhóm xác nhận 20 người ngoài nhóm.

## 1. Cách đếm

- Data dùng: sheet [KHẢO SÁT: Trải nghiệm xem TKB & Tra phòng học AI20K (Responses)](https://docs.google.com/spreadsheets/d/1dApQ_w1yJO1uYv9lI0sfnH20Y81m5FpseFmizW6vD2Q/edit?resourcekey=&gid=950983541#gid=950983541), tab `Form Responses 1`; 23 phản hồi ghi ngày 27/11/2026.
- Đếm gì: cột C ghi tình huống khi xem TKB lý thuyết; cột D ghi trải nghiệm tra phòng thực hành; cột E ghi số lần gặp khó tra phòng thực hành trong tuần. Phân tích trên 22 phản hồi tự khai vai trò `Học viên L3A/L3B`; không tính phản hồi `Lab Coach` vào mẫu số phân tích học viên.
- Mẫu số: 22 học viên trong toàn bộ sheet. Nhóm xác nhận 20/23 người ngoài nhóm, nhưng sheet không cho biết chính xác từng dòng nào là 20 người đó; vì vậy không gán các tỷ lệ dưới đây riêng cho nhóm 20 người ngoài nhóm.
- Cách làm: đọc tiêu đề cột và 23 dòng phản hồi, sau đó phân loại theo các đáp án có sẵn; đây là phép đếm mô tả sau khi xem dữ liệu, không phải giả thuyết/tiêu chí đăng ký trước.
- Công thức Google Sheets để chạy lại trên cùng tab (cột B = vai trò, C = tình huống, D = trải nghiệm, E = tần suất; phạm vi phản hồi hiện tại là hàng 2–24):
  - Mẫu số học viên: `=COUNTIF(B2:B24,"Học viên L3A/L3B")`
  - Dễ nhầm / cập nhật không rõ: `=COUNTIFS(B2:B24,"Học viên L3A/L3B",D2:D24,"Dễ bị nhầm phòng hoặc không rõ cập nhật mới nhất")`
  - Phải dò nhiều bước: `=COUNTIFS(B2:B24,"Học viên L3A/L3B",D2:D24,"Phải dò danh sách / bảng / tin nhắn nhiều bước mới ra đúng phòng của mình")`
  - Tần suất 1–2 lần: `=COUNTIFS(B2:B24,"Học viên L3A/L3B",E2:E24,"1-2 lần")`
  - Tần suất 3 lần trở lên: `=COUNTIFS(B2:B24,"Học viên L3A/L3B",E2:E24,"3 lần trở lên")`
  - Tình huống nhầm phòng/dò lại (câu chọn nhiều): `=COUNTIFS(B2:B24,"Học viên L3A/L3B",C2:C24,"*Bị nhầm phòng hoặc mất thời gian dò lại xem hôm nay gộp/đổi phòng chưa*")`
- Nếu sheet có thêm phản hồi, mở rộng các phạm vi hàng tương ứng trước khi chạy lại. Nếu locale của Google Sheets dùng dấu chấm phẩy, thay dấu phẩy phân cách đối số bằng `;`.

## 2. Đọc trước, đếm sau

Đã đọc tiêu đề cột và toàn bộ 23 dòng phản hồi. Tách riêng tình huống TKB lý thuyết (cột C) khỏi trải nghiệm và tần suất tra phòng thực hành (cột D–E); không dùng tần suất thực hành để suy ra tần suất lý thuyết. Câu trả lời tự do về tính năng được dùng làm ví dụ định tính, không gộp thành nhóm số nếu nội dung khác nhau.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---:|---:|---|
| Học viên L3A/L3B trong toàn bộ phản hồi | 22 / 23 | 96% | Còn 1/23 là Lab Coach. |
| Thực hành — trải nghiệm: dễ nhầm phòng / cập nhật không rõ | 6 / 22 | 27% | Đáp án hiện trạng; không đại diện cho phòng lý thuyết. |
| Thực hành — trải nghiệm: phải dò danh sách / bảng / tin nhắn nhiều bước | 5 / 22 | 23% | Đáp án hiện trạng; không đại diện cho phòng lý thuyết. |
| Thực hành — chọn một trong hai trải nghiệm trên | 11 / 22 | 50% | Hai đáp án hiện trạng loại trừ nhau trong câu hỏi này. |
| Thực hành — gặp khó ít nhất một lần trong tuần qua | 11 / 22 | 50% | 9 chọn 1–2 lần; 2 chọn 3 lần trở lên. |
| Thực hành — chọn “Chưa lần nào” trong tuần qua | 11 / 22 | 50% | Tần suất tự báo cáo. |
| Lý thuyết — chọn bị nhầm phòng / mất thời gian dò lại | 8 / 22 | 36% | Câu chọn tối đa 2 về tình huống khi xem TKB. |
| Lý thuyết — chọn lịch ghi H2xx nhưng thực tế gộp sang H209/H210 | 6 / 22 | 27% | Câu chọn tối đa 2; không phải tần suất. |
| Lý thuyết — chọn thông tin phòng nằm rải rác | 4 / 22 | 18% | Câu chọn tối đa 2. |
| Lý thuyết — chọn “Ít gặp / Không bị ảnh hưởng nhiều” | 10 / 22 | 45% | Câu chọn tối đa 2; có thể đi cùng lựa chọn khác. |

## 4. 5 ví dụ cụ thể (mã theo thứ tự phản hồi trong sheet)

1. R01: chọn cả tình huống lịch ghi H2xx nhưng thực tế gộp H209/H210 và tình huống bị nhầm phòng / mất thời gian dò lại khi xem TKB lý thuyết.
2. R02: chọn tình huống lịch ghi H2xx nhưng thực tế gộp H209/H210.
3. R08: chọn cả tình huống gộp H2xx sang H209/H210 và bị nhầm phòng / mất thời gian dò lại.
4. R21: chọn tình huống bị nhầm phòng / mất thời gian dò lại và thông tin phòng nằm rải rác.
5. R22: chọn tình huống bị nhầm phòng / mất thời gian dò lại và thông tin phòng nằm rải rác; câu trả lời tự do đề nghị hiển thị rõ phòng cũ và phòng mới khi đổi/gộp.

## 5. Giới hạn của data

Data cho biết người trả lời tự báo cáo điều gì, không cho biết nguyên nhân hoặc xác minh hành vi thực tế. Mẫu nhỏ, chỉ có vai trò tự khai; nhóm không thể tách riêng 20 người ngoài nhóm theo từng dòng. Một nửa học viên báo có gặp khó trong tuần qua, một nửa báo không gặp; kết quả không đồng nhất. Không có số phút bị mất. Phân tích này dùng chính dữ liệu khảo sát nên không phải kiểm chứng độc lập với khảo sát.

→ Nhóm không thực hiện phỏng vấn; hiện chưa có nguồn độc lập khác để đối chiếu.

## 6. Tần suất phòng lý thuyết — đếm từ TKB, không từ khảo sát

> Thêm 28/11/2026. Khảo sát **không có câu hỏi tần suất cho phòng lý thuyết** (cột E chỉ hỏi phòng thực hành, mục 3). Vì vậy số lần được đếm từ TKB đã lưu: `data/ai20k_student_schedule_long.csv`, giai đoạn 1 từ 05/11 đến 28/11 (24 ngày, coi như 1 tháng).

- Đếm gì: số buổi `kind=LEC` mà TKB ghi phòng lẻ H2xx (khác H209/H210) cho từng học viên L3A/L3B. Đây là **số lần học viên gặp tình huống cần xác nhận phòng** (độ phơi nhiễm), không phải số lần đi nhầm phòng.
- Cách chạy lại: lọc `group ∈ {L3A, L3B}`, `kind = LEC`, `room` khớp `H2\d\d` và khác `H209`, `H210`; đếm theo `student_id`.

| Đếm gì | Số | Ghi chú |
|---|---:|---|
| Học viên L3A/L3B trong TKB | 721 | L3A 360 · L3B 361 |
| Học viên có ≥1 buổi lý thuyết ghi phòng lẻ H2xx | 231 / 721 (32%) | L3A 60/360 · L3B 171/361 |
| Tổng lượt buổi lý thuyết ghi phòng lẻ H2xx / tháng | 855 | L3A 328 · L3B 527; 7.931 lượt LEC của L3, 6.650 lượt đã ở H209/H210 |
| Trung bình mỗi học viên bị ảnh hưởng | 3,7 lần / tháng | 855 / 231; phân bố lệch: 110 người chỉ 1 lần, 81 người ≥ 6 lần |
| Số buổi (lớp × ngày × buổi) có ít nhất 1 học viên ở phòng lẻ | 20 | Phòng lẻ hay gặp nhất: H203 (432 lượt), H207 (172), H201 (92) |
| Tham khảo: L2A (ngoài lát cắt) | 73 học viên · 365 lượt | L2B: 0 |

**Đối chiếu với khảo sát:** 32% học viên L3 có buổi lý thuyết ghi phòng lẻ theo TKB, gần với 8/22 (36%) học viên tự chọn "bị nhầm phòng / mất thời gian dò lại" và 6/22 (27%) chọn "lịch ghi H2xx nhưng thực tế gộp H209/H210". Hai nguồn đo khác nhau (TKB đo số lần gặp, khảo sát đo tình huống tự báo cáo), nên chỉ là khớp về độ lớn, không phải kiểm chứng.

**Vẫn chưa có:** số phút mất mỗi lần dò lại (khảo sát không hỏi) và tỉ lệ lần thực sự đi nhầm phòng. Impact / tháng = 855 lượt × __ phút: thừa số phút phải ghi *(tự ước tính)* nếu không đo thêm.
