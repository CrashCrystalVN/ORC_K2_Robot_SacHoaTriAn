import os

section5 = """
---

## 5. CẢI TIẾN CỤM SERVO S1 NÂNG HẠ & CÁNH TAY ĐÒN V5.0 (CHUẨN ĐĨA TRÒN MG996R & CHỐNG CẤN ỐC 100%)

### A. Phân tích nguyên nhân gốc rễ (Root Cause Analysis)
1. **Lỗi cấn ốc bắt Servo S1 khóa cứng cánh tay nâng ("ốc bắt bị vướng")**:
   - Vách tháp nâng bên phải nằm ở tọa độ $X \\in [20.0, 28.0\\text{ mm}]$, dầm phải của cánh tay nâng song hành nằm ở $X \\in [14.5, 19.5\\text{ mm}]$ (khe hở thiết kế ban đầu chỉ là $0.5\\text{ mm}$).
   - 2 lỗ ốc bắt mặt trước của servo MG996R nằm ở $Y = 158.9\\text{ mm}$ ($13.9\\text{ mm}$ phía trước trục quay $Y = 145.0\\text{ mm}$).
   - Khi xỏ bu-lông M3 từ ngoài vào tháp và vặn tán M3 tiêu chuẩn ($2.4\\text{ mm}$) ở mặt trong ($X = 20.0\\text{ mm}$), đầu tán và phần ren thừa chìa ra đến $X = 17.6\\text{ mm}$, **đâm sâu tới $1.9\\text{ mm}$ trực tiếp vào quỹ đạo quay của dầm tay nâng**, khiến cánh tay nâng bị kẹt cứng, không thể hạ xuống!
2. **Vấn đề phụ kiện tay gạt: Servo MG996R chỉ có 1 đĩa tròn 25T**:
   - Phụ kiện thực tế đi kèm trong hộp servo MG996R (nhất là dòng servo nhông kim loại phổ biến) thường chỉ có **1 đĩa tròn kim loại/nhựa 25T đường kính $\\varnothing 20.0\\text{ mm}$** (có 4 lỗ ren M3 bố trí đối xứng trên đường kính vòng chia PCD $\\varnothing 14.0\\text{ mm}$).
   - Thiết kế cũ dùng khe dài hẹp $8.2\\text{ mm}$ chỉ vừa cánh tay gạt đơn dài (single arm horn - vốn không có sẵn trong túi phụ kiện này).
3. **Ràng buộc thiết kế nghiêm ngặt**:
   - Giữ nguyên $100\\%$ kết cấu thượng tầng: Trục quay tay dưới $Y = 145.0\\text{ mm}, Z = 78.0\\text{ mm}$, trục quay tay trên $Z = 106.0\\text{ mm}$ (khoảng cách trục $28.0\\text{ mm}$), tay đòn trên `03B`, đầu kẹp hoa `04` và khung gầm `01` không thay đổi tọa độ hình học.

---

### B. Giải pháp kỹ thuật triệt để trên Bản vẽ V5.0

#### 1. Tháp nâng phải V5.0 (`01C_Lift_Tower_Right_MG996R_FlatPrint.stl`)
- **4 Hốc chìm tán lục giác M3 (Recessed Hex Nut Pockets)**:
  - Bố trí chìm hoàn toàn vào mặt trong vách tháp ($X = 20.0\\text{ mm}$) với kích thước $\\varnothing 6.5\\text{ mm}$, sâu $2.8\\text{ mm}$ ($fn=6$).
  - Tán M3 tiêu chuẩn (dày $2.4\\text{ mm}$) khi nhét vào sẽ nằm **chìm sâu $0.4\\text{ mm}$ dưới bề mặt vách**, hoàn toàn không có bất kỳ chi tiết kim loại nào nhô ra cấn vào cánh tay nâng.
- **Khoét hạ bậc quét cánh tay (Inner Sweep Clearance Pocket)**:
  - Khoét sâu $1.2\\text{ mm}$ bề mặt vách trong tháp nâng tại toàn bộ vùng quét $Y \\in [138, 166\\text{ mm}]$, $Z \\in [44, 74\\text{ mm}]$.
  - Mở rộng khe hở không khí giữa tay nâng và tháp từ $0.5\\text{ mm}$ lên **$1.6\\text{ mm}$**.
  - **Quy trình bắt ốc cực chuẩn**: Bu-lông M3x10mm xỏ từ ngoài qua tai servo rồi siết vào 4 tán M3 đã nhét chìm sẵn trong vách tháp. Mặt trong phẳng lì $100\\%$.

#### 2. Cánh tay đòn nâng song hành dưới V5.0 (`03_Parallel_Arm_Truss_IBeam.stl`)
- **Hốc tròn ôm khít đĩa tròn 25T ($\\varnothing 20.8\\text{ mm}$, sâu $2.5\\text{ mm}$)**:
  - Nằm ở mặt ngoài dầm phải ($X \\in [17.0, 19.5\\text{ mm}]$), ôm chuẩn xác đĩa tròn nhôm/nhựa $\\varnothing 20.0\\text{ mm}$ của servo MG996R, triệt tiêu hoàn toàn hiện tượng rơ lắc góc khi nâng tải nặng.
- **8 Lỗ bắt ốc M3 PCD $\\varnothing 14.0\\text{ mm}$ kèm lỗ bậc chìm đầu ốc**:
  - 8 lỗ chia góc $45^\\circ$ ($r = 7.0\\text{ mm}$) tương thích $100\\%$ cả đĩa tròn 4 lỗ chữ thập ($0^\\circ, 90^\\circ, 180^\\circ, 270^\\circ$) lẫn đĩa tròn chữ X ($45^\\circ, 135^\\circ, 225^\\circ, 315^\\circ$).
  - Mặt trong dầm ($X = 14.5\\text{ mm}$) được khoét lỗ bậc chìm $\\varnothing 6.0\\text{ mm}$ sâu $1.8\\text{ mm}$.
  - **Bắt ốc**: Vặn 4 ốc M3x8mm từ mặt trong xuyên ra ăn vào ren đĩa tròn kim loại. Đầu ốc chìm hoàn toàn vào thân dầm, không cọ quẹt bất kỳ chi tiết nào.
- **Lỗ khóa trục trung tâm $\\varnothing 6.5\\text{ mm}$**:
  - Cho phép đưa đầu vít/lục giác xuyên qua tâm cánh tay để siết hoặc mở ốc khóa cốt servo 25T mà **không cần tháo rã toàn bộ cánh tay đòn**.
- **DFM in 3D 0% Support**:
  - Đáy tay nâng được cắt phẳng tại $Z = -6.0\\text{ mm}$ ($Z_{\\text{bed}} = 0$) kèm các chân tiếp xúc bàn in vững chắc, đảm bảo in nằm phẳng $100\\%$ bám bàn cực tốt, không cần bất kỳ cấu trúc chống đỡ (support) nào.

#### 3. Khớp nối dẫn động đĩa tròn S1 rời V5.0 (`08_S1_MG996R_Round_Horn_Drive_Coupler.stl`)
- **Giải pháp tình huống cứu cánh 6 phút**:
  - Dành riêng cho trường hợp bạn đã in sẵn cánh tay cũ và không muốn in lại toàn bộ cánh tay dài.
  - Kích thước siêu nhỏ $23 \\times 31.5 \\times 6.5\\text{ mm}$, thời gian in chỉ $\\approx 6$ phút.
  - Mặt trước ôm khít đĩa tròn $\\varnothing 20\\text{ mm}$ với 4 lỗ M3 PCD $\\varnothing 14\\text{ mm}$, mặt sau có then mộng chữ nhật $8.0\\text{ mm}$ ngàm khít vào rãnh $8.2\\text{ mm}$ của tay cũ cùng 2 lỗ ốc M3 cố định ($Y = 10, 16\\text{ mm}$).

---

### C. Khay in Bambu Lab A1 Plate 8
- **Tệp khay in**: `Plate_8_Cum_Servo_S1_Nang_Ha_Va_Tay_Nang.3mf`
- **Các chi tiết trên khay**:
  1. `01C_Lift_Tower_Right_MG996R_FlatPrint.stl` (Tháp nâng phải chống cấn ốc V5.0)
  2. `03_Parallel_Arm_Truss_IBeam.stl` (Tay đòn nâng đĩa tròn V5.0)
  3. `08_S1_MG996R_Round_Horn_Drive_Coupler.stl` (Khớp nối đĩa tròn Module rời)
- **Thông số in**: In nằm phẳng $Z=0$, $0\\%$ Support, 4 wall loops, $25\\%$ gyroid infill, thời gian in $\\approx 42$ phút.
"""

readme_path = r"c:\Users\vuasu\.gemini\antigravity\scratch\ORC_K2_Robot_SacHoaTriAn\README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

if "## 5. CẢI TIẾN CỤM SERVO S1" not in content:
    content = content + section5
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated README.md with Section 5 successfully!")
else:
    print("Section 5 already exists in README.md!")

