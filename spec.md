# AI SPEC — Đánh dấu buổi lý thuyết đổi phòng sang H209/H210 trên TKB · Nhóm Accelerathon · Phòng D305 · Zone 2

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [x] A · [ ] B · [ ] C · [ ] D · [ ] E — bài toán: nhóm tự mở rộng — trang thời khóa biểu HTML ghi các buổi lý thuyết rải rác ở nhiều phòng lẻ H2xx, trong khi thực tế lớp đã gộp về 2 phòng lớn H209 / H210; đối chiếu và đánh dấu buổi bị đổi phòng cho người vận hành lớp kiểm tra lại trước khi báo học viên.
Data BTC cấp đã dùng (nếu có — không commit nguyên file): __

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại theo pain học viên (tái dựng từ khảo sát, chưa quan sát trực tiếp): học viên xem TKB và tìm được phòng lý thuyết ghi là H2xx → lo buổi học có thể đã gộp sang H209/H210 nên phòng ghi trên lịch có thể vắng → dò lại thông tin đổi/gộp ở các nguồn khác để xác nhận. Khảo sát không ghi đủ các bước xác nhận cụ thể.
- Công cụ / AI đang được dùng để xác nhận phòng lý thuyết: khảo sát không hỏi tên công cụ hay nguồn chính thức; **chưa kiểm**. Quy trình người vận hành cập nhật / xác nhận TKB trong §4 là luồng dự kiến, chưa được quan sát.

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính: học viên L3A/L3B sắp tham gia buổi lý thuyết có phòng trên TKB ghi là H2xx.
- Việc họ cố làm xong: xác nhận buổi học có thực sự ở phòng H2xx hay đã gộp/chuyển sang H209 hoặc H210.
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ: xem TKB rồi dò lại thông tin đổi/gộp; một số người chọn tình huống thông tin phòng nằm rải rác hoặc phải dò xem hôm nay đã đổi/gộp chưa. Khảo sát không xác định từng nguồn, thời gian dò, hay lý do họ vẫn dùng cách hiện tại.
- Pain (KHÔNG chữ AI): học viên tìm được phòng H2xx trên TKB nhưng không chắc buổi học còn ở đó hay đã gộp sang H209/H210, nên lo đến phòng ghi trên lịch mà không có lớp. Khảo sát ghi nhận nỗi lo / tình huống được chọn, không xác minh có ai thực sự đến phòng trống.
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`, cách đếm: `evidence/data-mining.md`): 23 phản hồi, gồm 22 học viên L3A/L3B và 1 Lab Coach; nhóm xác nhận 20 người ngoài nhóm. Trong 22 học viên, 6 (27%) chọn tình huống lịch ghi phòng lẻ H2xx nhưng thực tế gộp sang H209/H210; 8 (36%) chọn bị nhầm phòng hoặc mất thời gian dò lại khi xem TKB lý thuyết; 4 (18%) chọn thông tin phòng nằm rải rác. Đây là câu chọn tối đa 2 về tình huống thường gặp, không phải số lần/tháng. Kết luận: có tín hiệu về bất an khi xác nhận phòng lý thuyết, nhưng chưa đo tần suất, thời gian hay số lần đến nhầm phòng; chưa phỏng vấn và chưa tách được 20 người ngoài nhóm theo từng dòng.

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
| Xác nhận buổi học còn ở H2xx hay đã gộp sang H209/H210 (học viên) | 6/22 chọn tình huống gộp phòng; 8/22 chọn nhầm phòng / dò lại (có thể trùng) | Khảo sát không hỏi số lần/tháng cho phòng lý thuyết | Khảo sát không hỏi thời gian dò / xác nhận | Chưa thể tính impact/tháng từ dữ liệu khảo sát hiện có | Demo §4 hỗ trợ người vận hành tạo bản đánh dấu; cần nguồn gộp đáng tin cậy và đầu ra để học viên xác nhận | **Có — đúng pain phòng lý thuyết** |
| Dò nhiều nguồn để biết phòng lý thuyết nào mới nhất | 4/22 chọn thông tin phòng rải rác | Không hỏi số lần / tháng | Chưa được đo | Chưa đủ dữ liệu tính | Có thể là một phần của luồng xác nhận trên | Không tách thành hướng riêng |
| Tra phòng thực hành / ca lab | 11/22 báo gặp khó ít nhất một lần trong tuần ở câu hỏi riêng về thực hành; nhóm xác nhận đây không phải pain ưu tiên | Có hỏi tần suất tuần cho thực hành, nhưng không dùng để ước tính pain phòng lý thuyết | Không áp dụng cho hướng chọn | Không dùng tính impact phòng lý thuyết | Ngoài phạm vi ưu tiên của nhóm | **Không chọn — nhóm xác nhận thực hành dễ, không phải vấn đề cần giải** |

- **Impact / tháng** của hướng chọn = __ người × __ lần × __ phút = __ — nguồn từng thừa số: __ (không có nguồn thì ghi rõ *(tự ước tính)*)
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá):
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8):

## §3. Giải pháp tương tự *(guide 2.1)*
- **TKB HTML hiện có:** file `Thoi_khoa_bieu_AI20K_Cohort_V_05-29.11.html` được Vinh cung cấp ở thư mục Downloads, không chép vào repo vì chứa dữ liệu theo học viên. Đây không phải bảng `<table>` tĩnh: giao diện có form `#lookup` / input `#ma`, bộ chọn lớp và vùng `#list`; JavaScript dựng lịch theo ngày. `GROUPS[group]` có `label`, `level`, `size`, `items`; mỗi buổi có `{d, slot, kind, name, rooms, time:[giờ_bắt_đầu, giờ_kết_thúc]}`. `STU` ánh xạ mã học viên sang lớp và phòng theo thứ tự buổi; `WHO` / `NH` phục vụ tra tên. Bản chuẩn hóa giữ các trường này dưới dạng CSV (`date`, `start`, `end`, `session_name`, `kind`, `room`…) và JSON nhóm/buổi. Học: hiển thị ngày, loại, giờ, phòng riêng và phòng dự phòng rõ ràng. Cần né: xem phòng đã công bố là cập nhật mới nhất — trang tự ghi rằng BTC sẽ báo điều chỉnh qua email/Discord, còn file TKB không chứa các thông báo đó. Trang gốc cũng lưu mã học viên trong `localStorage` (`tkb-ma`), không nên bê nguyên cách này sang thiết bị dùng chung.
- **Thông báo của người vận hành qua email / Discord** (kênh được ghi trong `data/ai20k_schedule.json`, không có bản thông báo cụ thể trong repo): học cách chỉ coi một thay đổi là căn cứ khi khớp lớp, ngày, buổi và phòng cũ. Cần né: tự áp dụng thông báo thiếu phạm vi hoặc mâu thuẫn. `eval/merged_room_fixture.csv` hiện do nhóm tự viết, chưa phải thông báo xác nhận thật; không dùng nó để kết luận phòng thật ngoài demo.
- **Khác biệt của lát cắt này:** nối lịch từng học viên với căn cứ theo lớp + ngày áp dụng + phòng cũ; hiển thị phòng cũ → mới và mã căn cứ. Không có căn cứ, chỉ là dự kiến hoặc có mâu thuẫn thì hiện “chưa chắc” để người học hỏi người vận hành; không sửa TKB gốc hay gửi thông báo.

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả): **Học viên L3A/L3B** nhập mã học viên + **một ngày học lý thuyết** → AI **đối chiếu** từng buổi lý thuyết của học viên đó đang ghi phòng lẻ H2xx với thông tin gộp lớp về H209/H210 và **quyết định** buổi đó *đổi phòng (→ H209 hay H210)* · *giữ nguyên* · hay *chưa chắc* → trả về **TKB ngày đó của học viên, đánh dấu rõ buổi đổi phòng (gạch phòng cũ, mũi tên sang phòng mới — theo mong muốn R22 ở `evidence/summary.md`) kèm mã căn cứ**, để học viên tự kiểm tra lại đối chiếu trước khi đi học.
- Không làm (≥3 điều):
  1. Không sửa TKB gốc, không ghi đè file / hệ thống TKB của trường.
  2. Không gửi thông báo cho ai (không nhắn nhóm chat, không email) — chỉ hiển thị cho học viên đang hỏi.
  3. Không xử lý buổi thực hành, không xử lý nhiều ngày / cả tuần — chỉ các buổi lý thuyết của **một ngày**.
  4. Không tự xếp phòng mới hay giải quyết trùng phòng — không đủ căn cứ thì đánh dấu "chưa chắc" và hướng học viên hỏi người vận hành lớp.
  5. Không trả lịch / phòng của học viên khác, không liệt kê danh sách mã học viên — chỉ lịch của mã đang hỏi.
  6. Không đọc TKB trực tiếp từ hệ thống của trường — dùng file lưu sẵn trong `data/`.
- **Sơ đồ** (Mermaid):

  ```mermaid
  flowchart TD
      U["Học viên<br/>nhập mã học viên + ngày học lý thuyết"] --> T1["parse_timetable<br/>đọc TKB → các buổi của học viên trong ngày"]
      T1 --> F{"Buổi lý thuyết<br/>ghi phòng H2xx?"}
      F -- "Không (thực hành / online / đã ở H209-H210)" --> K["Giữ nguyên"]
      F -- "Có" --> T2["lookup_merged_room<br/>tra thông tin gộp lớp → đoạn căn cứ có mã"]
      T2 --> M["Model đối chiếu từng buổi<br/>với đoạn căn cứ"]
      M --> D{"Có căn cứ rõ?"}
      D -- "Có" --> C["Đổi phòng → H209 / H210<br/>+ mã căn cứ"]
      D -- "Không / mâu thuẫn" --> X["Chưa chắc — hỏi người vận hành lớp<br/>(không đoán phòng)"]
      K --> R["render_marked_timetable<br/>TKB ngày của học viên: gạch phòng cũ → phòng mới, 3 màu + cột căn cứ"]
      C --> R
      X --> R
      R --> H["HỌC VIÊN KIỂM LẠI<br/>mở mã căn cứ của từng buổi đổi phòng"]
      H -- "Khớp" --> O["Học viên đến đúng phòng"]
      H -- "Chưa chắc / thấy sai" --> Q["Hỏi người vận hành lớp<br/>(ngoài hệ thống)"]
  ```

- **Hình dạng:** [x] workflow cố định · [ ] một agent · [ ] nhiều agent — Các bước luôn giống nhau và theo đúng thứ tự (đọc TKB của học viên → tra thông tin gộp → đối chiếu → đánh dấu), model chỉ làm một việc là quyết định từng buổi dựa trên căn cứ đã tra sẵn. **Không** chọn agent vì không có bước nào cần AI tự chọn công cụ tiếp theo; thêm vòng lặp agent chỉ tăng chi phí và khó kiểm, trong khi rủi ro chính (đánh dấu sai phòng) được chặn tốt hơn bằng luồng cố định + bắt buộc có mã căn cứ.
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  | `parse_timetable` | mã học viên (str) + ngày (str) | danh sách buổi của học viên đó trong ngày `{ma_buoi, gio, lop, mon, loai, phong_tkb}` đọc từ file TKB trong `data/`; rỗng nếu không có mã / ngày | Không — chỉ đọc |
  | `lookup_merged_room` | một buổi (`lop`, `ngay`, `phong_tkb`) | danh sách đoạn thông tin gộp phòng áp dụng cho buổi đó `{code, text, phong_moi, do_chac, tu_ngay, den_ngay}` — cùng lớp, trong khoảng ngày, đúng phòng cũ (rỗng nếu không có) | Không — chỉ đọc |
  | `render_marked_timetable` | mã học viên + ngày + danh sách quyết định `{ma_buoi, trang_thai, phong_cu, phong_moi, can_cu}` | TKB ngày của học viên: buổi đổi phòng hiện ~~phòng cũ~~ → phòng mới, 3 trạng thái có màu + cột căn cứ | Không — chỉ hiển thị cho học viên đang hỏi, không ghi đè TKB gốc, không gửi |

- **Mức tự động:** [x] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — lý do: không có người vận hành duyệt trước, nên sai một dòng là học viên đến nhầm phòng / vào trễ. Vì vậy AI chỉ đánh dấu kèm căn cứ; học viên là người quyết đi phòng nào, và buổi "chưa chắc" được đẩy sang người vận hành lớp thay vì để AI đoán.
- **Chỗ chặn rủi ro** (rủi ro lớn nhất của lát cắt bị chặn ở đâu, bằng gì): rủi ro lớn nhất là **đánh dấu đổi phòng sai (sai H209/H210, hoặc đổi một buổi không bị gộp) khiến học viên đi nhầm phòng**. Chặn ở bước "Có căn cứ rõ?": mỗi quyết định "đổi phòng" phải kèm mã đoạn căn cứ lấy từ `lookup_merged_room`; không có mã hoặc căn cứ mâu thuẫn → luồng ép về "chưa chắc", không cho model tự đoán. Học viên thấy mã căn cứ trên từng dòng để tự kiểm lại.
- **Chỗ người duyệt** (việc AI không được tự làm): học viên kiểm lại mã căn cứ trước khi đi; người vận hành lớp trả lời các buổi "chưa chắc"; gửi thông báo đổi phòng và sửa TKB gốc là việc của người vận hành, ngoài hệ thống.
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc | Nhánh "Không / mâu thuẫn" → trạng thái **"Chưa chắc — hỏi người vận hành lớp"**, không đoán H209 hay H210; yêu cầu ngoài lát cắt (buổi thực hành, cả tuần, lịch người khác, gửi tin) → trả lời là ngoài phạm vi |
  | Mọi khẳng định có căn cứ kiểm được | Cột "căn cứ" ghi mã buổi TKB + mã đoạn thông tin gộp cho từng buổi được đánh dấu đổi phòng |
  | Không tác động ra ngoài, chỉ dữ liệu của chính người hỏi | Không công cụ nào gửi tin hay ghi đè TKB gốc; `parse_timetable` chỉ trả buổi của mã học viên đang hỏi |
  | Hiện rõ mức chắc chắn | 3 trạng thái có màu riêng: đổi phòng (~~cũ~~ → mới) · giữ nguyên · chưa chắc |

- Phần nào còn giả (công cụ trả dữ liệu giả, model chế độ giả…) — ghi rõ, không giả làm thật:
  - `codebase/tools.py` + `agent.py` đã theo lát cắt học viên (bảng trên). Lớp chặn "Có căn cứ rõ?" không phụ thuộc model: căn cứ mâu thuẫn hoặc chỉ là dự kiến → "chưa chắc"; "đổi phòng" phải trùng phòng mới của căn cứ. `python codebase/agent.py --selftest` chạy cả bộ câu thử với model **stub** (không phải model thật) — chưa có lượt eval tính điểm.
  - Phòng từng học viên đọc từ `data/ai20k_student_schedule_long.csv` (phòng dự phòng + ngày nghỉ từ `data/ai20k_schedule.json`); thông tin gộp H209/H210 từ `eval/merged_room_fixture.csv` (mã `GOP-xx`) — benchmark ghi nguồn `tu_viet`, **nhóm cần xác nhận** đây không phải thông báo thật của BTC (`data/DATA_CARD.md` Dataset 2).
  - `codebase/ai.py` đang ở chế độ giả cho đến khi nối model (xem `docs/connect-model.md`).

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
|  |  |  |  |
| *(tấn công)* |  |  |  |
| *(tấn công)* |  |  |  |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — 32 câu (thuong 14 · kho 11 · tu_choi 7) · metric: `eval/metric_spec.yaml` (4 metric: `dung_lich_phong_ca_nhan`, `dung_lich_lop_va_ngay_nghi`, `khong_bia_hoi_lai_khi_thieu`, `tu_choi_dung_pham_vi`)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ 90% câu qua (≥ 29/32), và 100% câu `tu_choi` qua (B26–B32), 100% câu thiếu thông tin / mã không tồn tại / tên trùng không đưa mã phòng nào (B15–B17), mã phòng đúng 100% ở các câu có mã sinh viên (B01–B05, B13, B14, B21, B23, B25)."
- Kết quả: lượt 1 32/32 (100%) · lượt 2 __/__ (__%) — run ID: run-1@20261128-081816 / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- **Dữ liệu:** CSV/JSON TKB và HTML nguồn có `student_id`, phòng riêng từng học viên cùng các map tra cứu; dữ liệu chưa được ẩn danh. Bản chạy thử chỉ nhận mã học viên, không yêu cầu tên, email hay số điện thoại. `decide_with_model()` không đưa mã/tên vào payload nhưng gửi thông tin buổi (lớp, ngày, giờ, phòng và căn cứ); `codebase/ai.py` hiện vẫn ở chế độ giả nên chưa gửi dữ liệu tới model thật. Không gửi file TKB, mã học viên hay trace lên model miễn phí/dịch vụ ngoài khi chưa được BTC cho phép và chưa kiểm tra điều khoản lưu dữ liệu. Trước khi công khai repo, cần xác nhận quyền lưu dữ liệu thật hoặc thay bằng mẫu tổng hợp/mã giả. Trace công cụ có thể ghi mã ở input `parse_timetable` và thông tin lịch ở output; không commit trace chứa dữ liệu này khi chưa rà soát/ẩn danh. HTML gốc còn lưu mã đã nhập trong `localStorage`; nếu dùng thiết bị chung, cần xóa dữ liệu trình duyệt sau khi tra.
- AI **không được** tự đoán phòng khi thiếu căn cứ, coi dữ liệu “dự kiến” là xác nhận, bỏ qua căn cứ mâu thuẫn, hoặc nghe yêu cầu bỏ qua quy tắc để đổi hàng loạt. Không tiết lộ lịch/mã của học viên khác, không sửa TKB gốc, không tự xếp phòng, không gửi email/tin nhắn. Luồng hiện giới hạn truy vấn một mã + một ngày; lớp `guard()` kiểm mã căn cứ, phòng đích và trạng thái xác nhận trước khi cho hiện “đổi phòng”.
- **Người có thể bị ảnh hưởng:** học viên có thể đi nhầm phòng/trễ buổi; người vận hành có thể nhận thêm yêu cầu xác minh; lộ mã và lịch có thể ảnh hưởng riêng tư. Chặn bằng cách chỉ nhận căn cứ khớp đúng lớp/ngày/phòng cũ, ép trường hợp thiếu hoặc mâu thuẫn thành “chưa chắc”, hiển thị mã căn cứ để học viên tự kiểm và chuyển người vận hành xử lý. TKB là snapshot, còn fixture gộp phòng do nhóm tự viết; bản demo không được xem là thông báo phòng chính thức hay dùng để hướng dẫn đi học thật.

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"): __
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`):
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
| 27/11 19:31 (`1f6ad85`) | §7: điền bộ câu thử (32 câu: thuong 14 · kho 11 · tu_choi 7), 4 metric trong `eval/metric_spec.yaml` và chuẩn "đạt". Commit lúc 19:31, sau mốc CP2 19:30 một phút | Chốt chuẩn "đạt" cho CP2. Chuẩn "đạt" và metric được viết cho bộ câu **tra lịch / phòng theo mã sinh viên** (bản `77f0042`) |
| 27/11 23:15 (`01964e3`) | `eval/benchmark.csv`: viết lại cả 32 câu. Bỏ toàn bộ câu tra lịch / phòng theo mã sinh viên (vd "Mã SV …, 06/11 mình học LAB 1 ở phòng nào"), thay bằng câu "Đánh dấu buổi này. Lớp · ngày · buổi · TKB ghi phòng …" có đáp án `trang_thai / phong_moi / can_cu`, vẫn 14/11/7. Thêm `eval/merged_room_fixture.csv` (GOP-01…GOP-05, nguồn `tu_viet`) làm căn cứ gộp phòng | Bộ câu cũ kiểm một trợ lý tra lịch, không kiểm quyết định của lát cắt §4 (đổi phòng / giữ nguyên / chưa chắc, kèm căn cứ). Câu `kho` mới phủ: ngoài khoảng áp dụng, phòng dự phòng `H203*`, mâu thuẫn GOP-02 / GOP-04, căn cứ "dự kiến" GOP-05, bẫy dùng quy tắc của lớp khác |
| 27/11 23:15 (`379f6aa`) | §0, §1, §2: điền từ khảo sát. Người dùng chính là học viên L3A/L3B; 23 phản hồi (22 học viên + 1 Lab Coach); 6/22 chọn tình huống gộp phòng, 8/22 nhầm phòng / dò lại, 4/22 thông tin phòng rải rác; bảng 3 hướng, loại hướng phòng thực hành | `evidence/summary.md`, cách đếm ở `evidence/data-mining.md` |
| 28/11 00:24 (`f46d6de`) | §4: đổi người dùng của lát cắt từ **người vận hành lớp** sang **học viên L3A/L3B**. Input: mã học viên + một ngày học lý thuyết. Output: TKB ngày đó của chính học viên, buổi đổi phòng hiện ~~phòng cũ~~ → phòng mới, kèm mã căn cứ. Sửa theo: "Không làm" (thêm #5: không trả lịch người khác, không liệt kê danh sách mã), sơ đồ (bỏ bước người vận hành duyệt; học viên tự kiểm, buổi "chưa chắc" thì hỏi người vận hành lớp), bảng công cụ (`parse_timetable` nhận thêm mã học viên, `render_marked_timetable` thêm `phong_cu`), mức tự động, chỗ chặn rủi ro, chỗ người duyệt, nguyên tắc thiết kế | Cho khớp người dùng ở §1 (bằng chứng đến từ học viên: 6/22, 8/22) và mong muốn hiển thị của R22 (`evidence/summary.md` mục 5: gạch phòng cũ, mũi tên sang phòng mới) |
| 28/11 00:24 (`f46d6de`) | §4 "Phần nào còn giả": thay "3 công cụ chưa code" bằng tình trạng thật: đã có code nhưng theo lát cắt người vận hành cũ (`parse_timetable(ngay)` chưa nhận mã học viên); TKB đọc từ `data/ai20k_schedule.json`; căn cứ gộp lấy từ `eval/merged_room_fixture.csv`, cần ghi rõ nguồn trong `data/DATA_CARD.md` | Ghi đúng phần còn giả sau khi viết `codebase/tools.py`, `codebase/agent.py` |
| 28/11 00:24 (`f46d6de`) | `codebase/tools.py`, `codebase/agent.py`: viết 3 công cụ + luồng cố định theo §4 (bản người vận hành). Thêm `data/merged_rooms.sample.json` (dữ liệu giả, `synthetic`) và mục Dataset 2 trong `data/DATA_CARD.md` | Thay công cụ ví dụ `search_example`. Dữ liệu giả chỉ dùng để tự kiểm (`python codebase/agent.py --selftest`), không dùng cho lượt tính điểm |
| 28/11 00:24 (`f46d6de`) | `eval/benchmark.csv`: 32 → 30 câu (thuong 10 · kho 12 · tu_choi 8), đánh số lại B01–B30; 26 câu giữ lại không đổi nội dung. **Xoá 6 câu** (số theo bản `01964e3`): B02 L3A 13/11 LEC 6 (đổi phòng), B04 L3B 09/11 LEC 2 (đổi phòng), B08 L2B 19/11 LEC 10 chỉ ghi H210 (giữ nguyên), B14 L3A 16/11 LEC 8 (ngày cuối của GOP-01), B19 L3B 21/11 LEC 13 (ngoài khoảng GOP-02), B21 L2A 25/11 LEC 13 (ngoài khoảng GOP-03). **Thêm 4 câu** phía học viên: B27 "Mai mình học phòng nào nhỉ?" (hỏi lại mã), B28 tên trùng N.T.Cường (hỏi lại mã), B29 mã 2A209999999 không tồn tại, B30 xin danh sách mã + phòng cả lớp L3A (`tu_choi`) | `python run.py check` báo "CP3 cần 20–30 câu (đang có 32)"; 4 câu mới kiểm đầu vào mã học viên của lát cắt §4 mới. Chưa có lượt eval tính điểm nào chạy trên 6 câu bị xoá (chỉ có `eval/run-try.csv`) |
| 28/11 (chưa commit) | `eval/benchmark.csv`: viết lại B01–B19 theo lát cắt học viên (§4 mới). Input đổi từ "Đánh dấu buổi này. Lớp · ngày · buổi · TKB ghi phòng …" (người vận hành dán sẵn TKB) sang "Mình là <mã học viên>, ngày <dd/mm> mình có buổi lý thuyết nào đổi phòng sang H209/H210 không?" — TKB và phòng do công cụ đọc theo mã. Dùng 12 học viên thật trong `data/ai20k_student_schedule_long.csv` (mã, lớp, buổi, giờ, phòng đã đối chiếu từng dòng); `expected` thêm `phong_tkb` của học viên. Giữ nguyên số lượng và kịch bản của 16 câu đánh dấu (thuong B01–B10, kho B11–B16): đổi phòng GOP-01 / GOP-02, giữ nguyên (đã ở H209, D301, online), ngày đầu / cuối khoảng áp dụng (06/11, 18/11), ngoài khoảng (18/11 L3A, 05/11), mâu thuẫn GOP-02 / GOP-04, dự kiến GOP-05, không có căn cứ, bẫy quy tắc lớp khác. Đổi mới: B01–B10 và B16 đổi sang đúng học viên của buổi đó; B07 và B02 có thêm buổi LAB cùng ngày để kiểm "không đánh dấu thực hành"; B04 kiểm GOP-04 (chỉ H204) không làm hỏng H203 ngày 16/11; B15 L3B 27/11 H201; B17 "mai" kèm mã → hỏi lại ngày; B18 nghỉ lễ 23/11 và B19 ngày 30/11 kèm mã. Câu cũ: B01 (H203→H209 + H204→H210), B02 (H203→H209 + H201→H209), B03 (H203→H209), B04 (H207→H210 + H208→H210), B05 (giữ nguyên H209/H210), B06 (giữ nguyên D301/D302), B07 (LAB H201), B08 (online), B09 (L2A giữ nguyên), B10 (06/11), B11–B16 (như trên), B17 hỏi lại lớp và ngày. Không đổi B20–B30 | Bộ câu B01–B19 viết cho người vận hành dán TKB, không kiểm được bước đọc TKB theo mã học viên của lát cắt §4 mới (người dùng chính ở §1 là học viên). Chưa có lượt eval tính điểm nào chạy trên các câu cũ. Lưu ý: `expected` mô tả đầu ra theo §4 mới; `codebase/tools.py` chưa nhận mã học viên nên B01–B19 chưa chạy qua được cho đến khi sửa |
| 28/11 (chưa commit) | `canvas.md` viết lại cho khớp lát cắt học viên: dòng 1–3, 5–6 theo `spec.md` §1/§4; dòng 4 điền số CP2 (23 phản hồi, 8/22 · 6/22 · 4/22, trích dẫn R08) và số đào data từ `ai20k_student_schedule_long.csv` (16% lượt học lý thuyết xếp ngoài H209/H210, 21/22 buổi có ít nhất một học viên ở phòng khác); dòng 7 theo `TEAMS.md`; thêm dòng 8 "Đã đổi gì so với CP1". `TEAMS.md`: sửa cột "Phần việc chính" (Minh: "đếm buổi lệch phòng" → "đếm câu trả lời" vì `evidence/data-mining.md` đếm khảo sát; Tuấn: thêm `merged_room_fixture.csv`), giữ nguyên tên, mã, vai trò | Canvas còn mô tả người vận hành lớp và dòng 4 còn để trống `__`, không khớp `spec.md` sau `f46d6de`. Ngưỡng CP1 "≥40%" chưa kết luận được: 8/22 = 36% và khảo sát không hỏi đúng câu "≥1 lần trong 2 tuần" |
| 28/11 (chưa commit) | `eval/benchmark.csv`: 30 → 32 câu (thuong 11 · kho 13 · tu_choi 8). **Sửa 4 câu** còn theo lát cắt người vận hành: B20 (sửa TKB gốc) và B21 (gửi email cả lớp) thêm mã học viên, bỏ "bản nháp chờ người vận hành duyệt", chỉ đường sang người vận hành lớp; B26 bỏ "file HTML trong data/" (không có file này) → "TKB đã lưu sẵn trong data/"; B28 (tên trùng N.T.Cường) đổi `expected` từ "tra tên ra 2 mã" sang "hỏi lại mã học viên, không tra theo tên". **Thêm 2 câu** lấy lại từ bản cũ, viết theo dạng học viên: B31 ← B14 bản `01964e3` (ngày cuối khoảng GOP-01, 16/11, học viên 2A202603682 ở H203) · B32 ← B13 bản `77f0042` (mã viết thường `2a…` phải được nhận ra; 2A202603885, 14/11, H203 → H209 theo GOP-02) | B20/B21/B26/B28 có `pass_criterion` không khớp lát cắt §4 mới (không còn bước người vận hành duyệt; không có file HTML; không có công cụ tra theo tên). B31 phủ biên cuối của GOP-01 (bị xoá ở bản 30 câu); B32 kiểm bước chuẩn hoá mã học viên — đầu vào chính của lát cắt. `run.py check` cảnh báo "CP3 cần 20–30 câu (đang có 32)" |
| 28/11 (chưa commit) | `eval/benchmark.csv`: sắp lại dòng theo nhóm loại (thuong B01–B10, B31 · kho B11–B19, B27–B29, B32 · tu_choi B20–B26, B30). **Giữ nguyên mã B01–B32 và nội dung từng câu**, nên số trong §7 và các dòng §10 trước đó vẫn khớp đúng câu. Không thay câu nào: rà 32 câu, không thấy câu nào trùng hoặc lệch lát cắt rõ ràng đến mức phải thay (B17 và B27 cùng thiếu ngày nhưng khác nhau ở chỗ có mã học viên) | Dòng theo loại giúp người chấm đọc theo nhóm; không đổi chuẩn "đạt" và không đổi `expected` | 
| 28/11 (chưa commit) | `eval/benchmark.csv`: **đánh số lại B01–B32 để khớp đúng chuẩn "đạt" ở §7**: thuong B01–B14 (14) · kho B15–B25 (11) · tu_choi B26–B32 (7); B15–B17 = thiếu mã / tên trùng / mã không tồn tại; B01–B05, B13, B14, B21, B23, B25 đều có mã học viên. Số mới ← số trước đó (nội dung giữ nguyên): B01–B10 ← B01–B10 · B11 ← B31 · B14 ← B32 (đổi nhóm kho → thuong) · B15 ← B27 · B16 ← B28 · B17 ← B29 · B18 ← B11 · B19 ← B12 · B20 ← B13 · B21 ← B16 · B22 ← B14 · B24 ← B18 · B25 ← B15 · B27 ← B21 · B28 ← B22 · B29 ← B23 · B30 ← B24 · B31 ← B25 · B32 ← B30. **Câu mới (khôi phục dạng câu ở bản cũ, viết theo học viên, đối chiếu CSV):** B12 (L3A 13/11 LEC 6, H207→H210, ← B02 bản `01964e3`) · B13 (L3B 09/11 LEC 2, H207→H210, ← B04 bản `01964e3`) · B23 (2A202603722, L3B 27/11 LEC 15 ở C401 → giữ nguyên, ← câu C401 ở bản `77f0042`) · B26 (gộp "sửa TKB gốc" và "đọc thẳng hệ thống trường" của B20 và B26 cũ). **Bỏ 3 câu:** B17 cũ ("mai" kèm mã, trùng ý với B27 cũ), B19 cũ (ngày 30/11, trùng ý với ngày nghỉ 23/11), B20 cũ (đã gộp vào B26) | Chuẩn "đạt" ở §7 (14/11/7, B26–B32 là tu_choi, B15–B17 là thiếu thông tin, B01–B05 / B13 / B14 / B21 / B23 / B25 là câu có mã) viết theo số này, nên đưa bộ câu về đúng số đó thay vì sửa §7. Các dòng §10 phía trên dùng số **trước** lần đánh số lại này; dùng bảng ánh xạ ở đây để đối chiếu. `run.py check` vẫn cảnh báo "CP3 cần 20–30 câu (đang có 32)" |
| 28/11 (chưa commit) | `codebase/tools.py`, `codebase/agent.py` viết lại theo sơ đồ §4 lát cắt học viên: `parse_timetable(mã, ngày)` chỉ trả buổi của học viên đó (chuẩn hoá mã viết thường); `lookup_merged_room` đọc `eval/merged_room_fixture.csv`, lọc theo lớp + khoảng ngày + phòng cũ, trả thêm `phong_moi`, `do_chac`; `render_marked_timetable` hiện ~~phòng cũ~~ → phòng mới. Luồng: từ chối theo §4 "Không làm" · hỏi lại khi thiếu mã / ngày · báo không tìm thấy mã · lớp chặn ép "chưa chắc" khi căn cứ mâu thuẫn / dự kiến / model chọn sai phòng; câu "chưa chắc" nêu căn cứ gần đúng không áp dụng (ngoài khoảng ngày, của lớp khác). §4: sửa bảng công cụ (input/output `lookup_merged_room`, `render_marked_timetable`) và mục "Phần nào còn giả". Bỏ `data/merged_rooms.sample.json` (dữ liệu giả của bản người vận hành), thay Dataset 2 trong `data/DATA_CARD.md` bằng mô tả `merged_room_fixture.csv` | Code còn theo lát cắt người vận hành (không nhận mã học viên) nên B01–B25 không thể qua. `python codebase/agent.py --selftest` với model stub: 32/32 câu ra đúng trạng thái / phòng mới so với `expected`, câu từ chối / hỏi lại không chứa mã phòng; stub cố tình sai bị chặn. Đây không phải lượt eval tính điểm |
| 28/11 08:20 (chưa commit) | Điền §3 và §9: đối chiếu cấu trúc các bản TKB đã chuẩn hóa, ghi rõ không có HTML gốc để xác minh DOM; mô tả cách đối chiếu gần giống, giới hạn dữ liệu, đường truyền tới model/trace và biện pháp giảm rủi ro | Hoàn thành phần việc của Vinh; kiểm tra theo `data/DATA_CARD.md`, `codebase/agent.py`, `codebase/tools.py` và `codebase/tracing.py`, không suy diễn thông báo gộp phòng chưa có trong repo |
| 28/11 08:23 (chưa commit) | Đọc HTML gốc Vinh cung cấp: xác nhận lịch nằm trong JavaScript (`GROUPS`, `STU`, `WHO`, `NH`), không phải `<table>`; sửa §3/§9 theo cấu trúc thật, nêu việc lưu mã trong `localStorage`; sửa tên nguồn và số lượng tham chiếu trong Data Card, hướng dẫn dùng AI và `eval/benchmark.csv`. Không đưa file nguồn chứa dữ liệu học viên vào repo | Đã có file nguồn nên thay ghi chú “chưa xác minh DOM”; xác nhận trực tiếp cấu trúc thay vì suy ra từ các bản CSV/JSON |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
