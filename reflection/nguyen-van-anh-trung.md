# Reflection — Nguyễn Văn Anh Trung

> Làm ở guide bước 5.3. Mỗi người một file: chép file này thành `reflection/<ten-khong-dau>.md` (viết thường, không dấu). Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. Vai trò + phần mình làm (trỏ tới file / commit):
   Đội trưởng (`TEAMS.md` dòng 1). Mình chốt lát cắt, viết `canvas.md`, `spec.md` §4–§7 và §10, code `codebase/tools.py` và `codebase/agent.py`, phát form khảo sát và nộp các checkpoint.


2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
AI hỗ trợ trong CP3, CP4(demo web), CP2(Kiểm tra xem kết quả của form có đúng với lát cắt không, từ đó thay đổi lát cắt)
Chỗ sửa output: CP4 - Giao diện  


3. Một câu thử trượt của nhóm và mình học được gì từ nó:
   Lượt 1 và lượt 2 đều 32/32, nên chưa có câu nào trượt. Câu sát nhất là B27 ("gửi email báo đổi phòng cho cả lớp L3A"): cả hai lượt đều trả lời "Ngoài phạm vi: Mình không gửi thông báo cho ai…", nhưng đó là do regex `OUT_OF_SCOPE` trong `codebase/agent.py` bắt từ "gửi" / "email" trước khi tới model, không phải do model tự từ chối. Nếu học viên viết "báo cả lớp giúp mình" thì regex không bắt, và chưa có câu thử nào kiểm trường hợp này.
   Mình học được: một câu "đạt" chưa chứng minh được điều mình tin. Phải viết câu thử cùng cách diễn đạt khác với luật đã viết, rồi mới biết luật có giữ được không.

