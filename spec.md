# AI SPEC — Đánh dấu buổi lý thuyết đổi phòng sang H209/H210 trên TKB · Nhóm Accelerathon · Phòng D305 · Zone 2

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [x] A · [ ] B · [ ] C · [ ] D · [ ] E — bài toán: nhóm tự mở rộng — trang thời khóa biểu HTML ghi các buổi lý thuyết rải rác ở nhiều phòng lẻ H2xx, trong khi thực tế lớp đã gộp về 2 phòng lớn H209 / H210; đối chiếu và đánh dấu buổi bị đổi phòng cho người vận hành lớp kiểm tra lại trước khi báo học viên.
Data BTC cấp đã dùng (nếu có — không commit nguyên file): __

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại của việc này, trong khoá hoặc trên app thật (3–5 bước; ảnh chụp từ tài khoản của mình, đã che thông tin):
- Công cụ / AI đang được dùng cho việc này (nếu có) + nguồn. Không kiểm được thì ghi "chưa kiểm":

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể):
- Việc họ cố làm xong (`động từ + đối tượng + bối cảnh`, không có chữ AI):
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ:
- Pain (KHÔNG chữ AI): ai — đang làm gì — vướng đâu — hậu quả gì:
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`): __

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

- **Impact / tháng** của hướng chọn = __ người × __ lần × __ phút = __ — nguồn từng thừa số: __ (không có nguồn thì ghi rõ *(tự ước tính)*)
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá):
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8):

## §3. Giải pháp tương tự *(guide 2.1)*
- [sản phẩm / tính năng gần giống]: một điều đáng học · một điều đáng né · mình khác gì

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả): **Người vận hành lớp** mở trang thời khóa biểu (TKB) HTML của **một ngày học lý thuyết mẫu** → AI **đối chiếu** từng buổi đang ghi phòng lẻ H2xx với thông tin gộp lớp về H209/H210 và **quyết định** buổi đó *đổi phòng (→ H209 hay H210)* · *giữ nguyên* · hay *chưa chắc* → trả về **bản nháp TKB đã đánh dấu rõ các buổi đổi phòng kèm căn cứ**, để người vận hành kiểm tra lại đối chiếu và duyệt trước khi báo học viên.
- Không làm (≥3 điều):
  1. Không sửa TKB gốc, không ghi đè file / hệ thống TKB của trường.
  2. Không gửi thông báo cho học viên (không nhắn nhóm chat, không email) — chỉ tạo bản nháp.
  3. Không xử lý buổi thực hành, không xử lý nhiều ngày / cả tuần — chỉ các buổi lý thuyết của **một ngày mẫu**.
  4. Không tự xếp phòng mới hay giải quyết trùng phòng (vd hai lớp cùng giờ cùng muốn H209) — chỉ đánh dấu "chưa chắc" để người quyết.
  5. Không đọc TKB trực tiếp từ hệ thống của trường — dùng file HTML lưu sẵn trong `data/`.
- **Sơ đồ** (Mermaid):

  ```mermaid
  flowchart TD
      U["Người vận hành lớp<br/>chọn ngày học lý thuyết mẫu"] --> T1["parse_timetable<br/>đọc TKB HTML → danh sách buổi"]
      T1 --> F{"Buổi lý thuyết<br/>ghi phòng H2xx?"}
      F -- "Không (thực hành / đã ở H209-H210)" --> K["Giữ nguyên"]
      F -- "Có" --> T2["lookup_merged_room<br/>tra thông tin gộp lớp → đoạn căn cứ có mã"]
      T2 --> M["Model đối chiếu từng buổi<br/>với đoạn căn cứ"]
      M --> D{"Có căn cứ rõ?"}
      D -- "Có" --> C["Đổi phòng → H209 / H210<br/>+ mã căn cứ"]
      D -- "Không / mâu thuẫn" --> X["Chưa chắc — cần người kiểm<br/>(không đoán phòng)"]
      K --> R["render_marked_timetable<br/>bản nháp TKB đánh dấu 3 màu + cột căn cứ"]
      C --> R
      X --> R
      R --> H["NGƯỜI VẬN HÀNH DUYỆT<br/>kiểm lại từng dòng đánh dấu"]
      H -- "Duyệt" --> O["Người vận hành tự báo học viên<br/>(ngoài hệ thống)"]
      H -- "Sửa" --> R
  ```

- **Hình dạng:** [x] workflow cố định · [ ] một agent · [ ] nhiều agent — Các bước luôn giống nhau và theo đúng thứ tự (đọc TKB → tra thông tin gộp → đối chiếu → đánh dấu), model chỉ làm một việc là quyết định từng buổi dựa trên căn cứ đã tra sẵn. **Không** chọn agent vì không có bước nào cần AI tự chọn công cụ tiếp theo; thêm vòng lặp agent chỉ tăng chi phí và khó kiểm, trong khi rủi ro chính (đánh dấu sai phòng) được chặn tốt hơn bằng luồng cố định + người duyệt.
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  | `parse_timetable` | ngày học mẫu (str) | danh sách buổi `{ma_buoi, gio, lop, mon, loai, phong_tkb}` đọc từ file TKB HTML trong `data/` | Không — chỉ đọc |
  | `lookup_merged_room` | một buổi (`lop`, `gio`, `mon`, `phong_tkb`) | danh sách đoạn thông tin gộp phòng `{code, text}` liên quan (rỗng nếu không có) | Không — chỉ đọc |
  | `render_marked_timetable` | danh sách quyết định `{ma_buoi, trang_thai, phong_moi, can_cu}` | trang TKB HTML **bản nháp** đánh dấu 3 trạng thái + cột căn cứ, gắn nhãn "chờ duyệt" | Không — chỉ tạo bản nháp, không ghi đè TKB gốc, không gửi |

- **Mức tự động:** [x] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — lý do: sai một dòng là cả lớp (hàng chục học viên) đi nhầm phòng / vào trễ, người vận hành mất uy tín; bắt lỗi trên bản nháp trước khi báo thì rẻ, sửa sau khi đã thông báo cả lớp thì đắt (phải nhắn đính chính, học viên đã di chuyển).
- **Chỗ chặn rủi ro** (rủi ro lớn nhất của lát cắt bị chặn ở đâu, bằng gì): rủi ro lớn nhất là **đánh dấu đổi phòng sai (sai H209/H210, hoặc đổi một buổi không bị gộp)**. Chặn ở bước "Có căn cứ rõ?": mỗi quyết định "đổi phòng" phải kèm mã đoạn căn cứ lấy từ `lookup_merged_room`; không có mã hoặc căn cứ mâu thuẫn → luồng ép về "chưa chắc", không cho model tự đoán. Cuối cùng chặn thêm ở bước người vận hành duyệt.
- **Chỗ người duyệt** (việc AI không được tự làm): duyệt bản nháp TKB đã đánh dấu trước khi dùng; quyết định các buổi "chưa chắc"; gửi thông báo đổi phòng cho học viên; sửa TKB gốc.
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc | Nhánh "Không / mâu thuẫn" → trạng thái **"Chưa chắc — cần người kiểm"**, không đoán H209 hay H210; yêu cầu ngoài lát cắt (buổi thực hành, cả tuần, gửi tin) → trả lời là ngoài phạm vi |
  | Mọi khẳng định có căn cứ kiểm được | Cột "căn cứ" trên bản nháp ghi mã dòng TKB + mã đoạn thông tin gộp cho từng buổi được đánh dấu đổi phòng |
  | Người duyệt trước mọi tác động ra ngoài | Bản nháp gắn nhãn "chờ duyệt"; không công cụ nào gửi tin hay ghi đè TKB gốc |
  | Hiện rõ mức chắc chắn | 3 trạng thái có màu riêng trên trang: đổi phòng · giữ nguyên · chưa chắc |

- Phần nào còn giả (công cụ trả dữ liệu giả, model chế độ giả…) — ghi rõ, không giả làm thật:
  - `codebase/tools.py` hiện vẫn là công cụ ví dụ `search_example`; 3 công cụ ở bảng trên **chưa code** (Vinh làm, đến CP3).
  - File TKB HTML một ngày mẫu và file thông tin gộp phòng H209/H210 **chưa có trong `data/`** — sẽ lưu bản đã ẩn danh / viết lại và mô tả ở `data/DATA_CARD.md`.
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
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** làm gì kể cả khi người dùng yêu cầu:
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"): __
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`):
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
|  |  |  |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
