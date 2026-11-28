# Reflection — Triệu Tuấn Minh

> Bản nháp, Minh đọc lại và sửa theo giọng của mình trước 23:59 Thứ Bảy 28/11. Mỗi câu 3–6 dòng.

1. **Vai trò + phần mình làm:**
   Thành viên (`TEAMS.md` dòng 2). Mình làm khảo sát và đếm câu trả lời (`evidence/summary.md`, `evidence/data-mining.md`), viết `spec.md` §0–§2, nối model thật vào `codebase/ai.py` (commit `374c446`), chạy và chấm eval lượt 1 (`eval/run-1.csv`: 32/32), làm slides và reflection.
   Mình cũng bổ sung tần suất phòng lý thuyết đếm từ TKB (`evidence/data-mining.md` mục 6), vì khảo sát không có câu hỏi tần suất cho phòng lý thuyết.

2. **AI hỗ trợ mình thế nào:**
   Mình dùng Claude Code để viết `ai.py` theo `docs/connect-model.md` (nhánh Gemini REST, đọc token từ `usageMetadata`), kiểm từng câu của lượt 1 với `pass_criterion` và đếm số buổi lý thuyết ở phòng lẻ H2xx trong `data/ai20k_student_schedule_long.csv`.
   Chỗ phải tự kiểm / sửa: mã model phải lấy từ danh sách model thật của key AI Studio chứ không lấy theo tên AI đoán; cột `pass` mình tự điền sau khi đọc lại output, không để AI tự chấm; AI không mở được Google Sheet nên số khảo sát lấy từ phần đếm của nhóm, mình phải tự đối chiếu với sheet gốc. *(Minh sửa câu này cho đúng việc đã làm.)*

3. **Một câu thử trượt của nhóm và mình học được gì:**
   Lượt 1 không có câu trượt (32/32), nhưng điều đó không có nghĩa là model giỏi: trung bình chỉ 0,4 lần gọi model mỗi câu, phần lớn câu được luật trong `agent.py` xử lý trước khi tới model. Ở B11, trạng thái và phòng đúng nhưng lý do model viết ("L3A học tại H209") không nói phòng cũ H203, nếu chấm chặt phần giải thích thì có thể trượt.
   Mình học được: bộ câu thử cần có câu buộc model phải tự quyết (nhiều căn cứ, nhiều buổi trong ngày) thì mới đo được đóng góp của AI; và metric phải viết lại cùng lúc khi đổi bộ câu thử — `eval/metric_spec.yaml` của nhóm vẫn là bản cho ý tưởng tra lịch cũ.
