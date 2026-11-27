# Đào data — phân tích bảng phản hồi khảo sát

> Cập nhật 27/11/2026. Đây là phân tích định lượng lại cùng bảng khảo sát ở `evidence/summary.md`, không phải một nguồn người dùng độc lập thứ hai. Số liệu là snapshot 23 phản hồi hiện có; nhóm xác nhận 20 người ngoài nhóm.

## 1. Cách đếm

- Data dùng: sheet [KHẢO SÁT: Trải nghiệm xem TKB & Tra phòng học AI20K (Responses)](https://docs.google.com/spreadsheets/d/1dApQ_w1yJO1uYv9lI0sfnH20Y81m5FpseFmizW6vD2Q/edit?resourcekey=&gid=950983541#gid=950983541), tab `Form Responses 1`; 23 phản hồi ghi ngày 27/11/2026.
- Đếm gì: trải nghiệm tra phòng và số lần gặp khó trong tuần; trên 22 phản hồi tự khai vai trò `Học viên L3A/L3B`; không tính phản hồi `Lab Coach` vào mẫu số phân tích học viên.
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

Đã đọc tiêu đề cột và toàn bộ 23 dòng phản hồi. Các trường có thể đếm nhất quán gồm vai trò, trải nghiệm hiện tại, tần suất gặp khó trong tuần, và lựa chọn tình huống khi xem lịch. Câu trả lời tự do về tính năng được dùng làm ví dụ định tính, không gộp thành nhóm số nếu nội dung khác nhau.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---:|---:|---|
| Học viên L3A/L3B trong toàn bộ phản hồi | 22 / 23 | 96% | Còn 1/23 là Lab Coach. |
| Trải nghiệm: dễ nhầm phòng / cập nhật không rõ | 6 / 22 | 27% | Đáp án hiện trạng. |
| Trải nghiệm: phải dò danh sách / bảng / tin nhắn nhiều bước | 5 / 22 | 23% | Đáp án hiện trạng. |
| Chọn một trong hai trải nghiệm trên | 11 / 22 | 50% | Hai đáp án hiện trạng loại trừ nhau trong câu hỏi này. |
| Gặp khó ít nhất một lần trong tuần qua | 11 / 22 | 50% | 9 chọn 1–2 lần; 2 chọn 3 lần trở lên. |
| Chọn “Chưa lần nào” trong tuần qua | 11 / 22 | 50% | Tần suất tự báo cáo. |
| Chọn bị nhầm phòng / mất thời gian dò lại trong câu chọn tối đa 2 | 9 / 22 | 41% | Đáp án nhiều lựa chọn. |
| Chọn lịch phòng lẻ H2xx nhưng thực tế gộp sang H209/H210 | 6 / 22 | 27% | Đáp án nhiều lựa chọn. |
| Chọn “Ít gặp / Không bị ảnh hưởng nhiều” | 9 / 22 | 41% | Đáp án nhiều lựa chọn; có thể đi cùng một lựa chọn khác. |

## 4. 5 ví dụ cụ thể (mã theo thứ tự phản hồi trong sheet)

1. R01: chọn lịch ghi phòng lẻ H2xx nhưng thực tế gộp H209/H210 và bị nhầm phòng/mất thời gian dò lại; tuần qua chọn “Chưa lần nào”.
2. R04: chọn thông tin phòng nằm rải rác; trải nghiệm là phải dò nhiều bước; tuần qua chọn 1–2 lần.
3. R07: chọn tình huống phòng H2xx gộp sang H209/H210; trải nghiệm dễ nhầm/cập nhật không rõ; tuần qua chọn 3 lần trở lên.
4. R08: chọn cả tình huống H2xx gộp phòng và bị nhầm/mất thời gian dò lại; trải nghiệm phải dò nhiều bước; tuần qua chọn 3 lần trở lên.
5. R22: chọn bị nhầm phòng/mất thời gian dò lại và thông tin nằm rải rác; trải nghiệm dễ nhầm/cập nhật không rõ; tuần qua chọn 1–2 lần.

## 5. Giới hạn của data

Data cho biết người trả lời tự báo cáo điều gì, không cho biết nguyên nhân hoặc xác minh hành vi thực tế. Mẫu nhỏ, chỉ có vai trò tự khai; nhóm không thể tách riêng 20 người ngoài nhóm theo từng dòng. Một nửa học viên báo có gặp khó trong tuần qua, một nửa báo không gặp; kết quả không đồng nhất. Không có số phút bị mất. Phân tích này dùng chính dữ liệu khảo sát nên không phải kiểm chứng độc lập với khảo sát.

→ Nhóm không thực hiện phỏng vấn; hiện chưa có nguồn độc lập khác để đối chiếu.
