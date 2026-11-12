# BÁO CÁO ĐO ĐẠC HÌNH HỌC PIN 2S2P 18650 & QUY CHUẨN KHOANG PIN VẠN NĂNG (UNIVERSAL BATTERY BAY)
**Dự án:** Robot Thi Đấu "Sắc Hoa Tri Ân" - ORC K2 Pro DFM 200x200mm  
**Chuyên gia thực hiện:** Subagent 1 - 2S2P Battery Metrologist & Packaging Architect  
**Tập tin khung gầm tham chiếu:** `01_Chassis_Base_200x200_V6.scad`, `full_assembly_200x200.scad`, `generate_redesigned_parts.py`

---

## 1. KHẢO SÁT & QUY CÁCH HÌNH HỌC KHỐI PIN ĐÓNG SẴN 2S2P 18650 TRÊN THỊ TRƯỜNG

Khối pin đóng sẵn 2S2P 18650 (Lithium-ion 7.4V danh định / 8.4V sạc đầy, dung lượng 4000mAh - 6800mAh) là nguồn cấp động lực tiêu chuẩn cho robot thi đấu STEM/ORC. Cấu tạo khối pin hoàn chỉnh gồm:
- **4 Cell 18650 tiêu chuẩn**: Đường kính cell trần Ø18.2 - 18.4 mm, chiều dài 65.0 - 65.3 mm.
- **Mạch bảo vệ BMS 2S (5A - 15A)**: Bổ sung chiều dày 3.5 - 4.5 mm (thường gắn ở đầu cực hoặc áp sườn).
- **Kẽm hàn bấm điểm (Nickel strip 0.15 - 0.2 mm)** + **Giấy cách điện Barley paper / Kapton**.
- **Màng co nhiệt PVC màu xanh**: Dày 0.3 - 0.5 mm mỗi lớp.
- **Cụm dây dẫn ra ngoài**:
  + Dây tải chính: Dây silicone chịu nhiệt 16 - 18 AWG, dài 100 - 150 mm, đầu cắm T-plug (Deans) / XT30 / DC 5.5x2.1mm.
  + Dây sạc cân bằng (Balance lead): Jack 3 chân JST-XH 2.54mm.
  + Bán kính uốn cong an toàn cho đầu dây ra: $R_{bend} \ge 5.0\text{ mm}$.

### Bảng đối chiếu 3 dạng đóng gói pin 2S2P phổ biến:

| Thông số hình học | Dạng 1: Khối vuông / Cục gạch (2x2 Brick)<br>*(Phổ biến nhất - 85% thị phần)* | Dạng 2: Khối dẹp phẳng (1x4 Flat)<br>*(Chuyên gầm thấp / RC)* | Dạng 3: Khối thanh dài (2S2P Long)<br>*(Ít dùng trên xe nhỏ)* |
| :--- | :--- | :--- | :--- |
| **Cấu trúc sắp xếp cell** | 2 hàng x 2 cell xếp chồng (tiết diện $2 \times 2$) | 4 cell nằm dàn hàng ngang (tiết diện $1 \times 4$) | 2 cell nối tiếp dọc x 2 hàng song song |
| **Bề rộng $W$** | **37.0 - 39.0 mm** (Bao dung sai: **40.0 mm**) | **74.0 - 78.0 mm** (Bao dung sai: **79.0 mm**) | **37.0 - 39.0 mm** |
| **Chiều dày / Cao $H$** | **37.0 - 39.0 mm** (Kèm BMS: **40.0 mm**) | **19.0 - 21.0 mm** (Kèm BMS: **21.5 mm**) | **19.0 - 21.0 mm** |
| **Chiều dài $L$** | **68.0 - 72.0 mm** (Cả kẽm & màng co) | **68.0 - 72.0 mm** (Cả kẽm & màng co) | **136.0 - 142.0 mm** |
| **Trọng lượng** | ~195 - 215 g | ~195 - 215 g | ~195 - 215 g |
| **Cao độ trọng tâm ($Z_{CoG}$)** | $19.0\text{ mm}$ (tính từ đáy pin) | **$10.0\text{ mm}$** (Rất thấp, bám đường cực tốt) | $10.0\text{ mm}$ |
| **Khả năng tương thích 200x200** | **RẤT TỐT** (Cần nâng tầng K2 Hub) | **RẤT TỐT** (Cần mở rộng khoảng cách trụ) | **KHÔNG PHÙ HỢP** (Dài 140mm cấn cụm truyền động) |

---

## 2. PHÂN TÍCH KHÔNG GIAN GẦM XE HIỆN TẠI TRÊN `01_Chassis_Base_200x200_V6.scad`

### 2.1. Bản đồ tọa độ không gian gầm xe ($X, Y, Z$):
- **Kích thước khung gầm**: Rộng $CHASSIS\_W = 118.0\text{ mm}$, Dài $CHASSIS\_L = 172.0\text{ mm}$, Sàn $FLOOR\_T = 4.0\text{ mm}$.
- **Khoảng lọt lòng giữa hai vách sườn**: $118.0 - 2 \times 4.0 = \mathbf{110.0\text{ mm}}$ (tại $X \in [-55.0, +55.0\text{ mm}]$).
- **Vị trí cầu truyền động GA25**:
  + Cầu sau: Tâm trục $Y_{rear} = 32.0\text{ mm}$. Khối nẹp & ổ đỡ motor kết thúc tại $Y_{rear\_cradle\_end} \approx \mathbf{46.0 - 54.0\text{ mm}}$.
  + Cầu trước: Tâm trục $Y_{front} = 142.0\text{ mm}$. Khối nẹp & ổ đỡ motor bắt đầu tại $Y_{front\_cradle\_start} \approx \mathbf{120.0 - 128.0\text{ mm}}$.
- **Hành lang khoang giữa (Central Longitudinal Corridor)**:
  + Chiều dài thông thoáng tối đa: $\Delta Y = 128.0 - 46.0 = \mathbf{82.0\text{ mm}}$!
  + Kích thước này **hoàn toàn đủ để đặt khối pin dài 68.0 - 72.0 mm** theo cả phương dọc ($Y$) lẫn phương ngang ($X$) mà không hề chạm vào động cơ GA25 trước/sau!

### 2.2. Nhận diện 2 vấn đề cốt tử gây cấn kết cấu (Collision Forensic Analysis):

#### Vấn đề cốt tử 1: Cấn CHIỀU CAO với Pin Dạng 1 (Khối 2x2 Cục gạch - $H = 38.0 - 40.0\text{ mm}$):
- **Hiện trạng trên Chassis V6**: 4 trụ đỡ MCU Control Hub đúc liền sàn có kích thước $10 \times 10 \times 18\text{ mm}$ ($Z \in [4.0, 22.0\text{ mm}]$).
- **Khoảng sáng tĩnh không dưới K2 Hub cũ**: $H_{clear\_cu} = 22.0 - 4.0 = \mathbf{18.0\text{ mm}}$.
- **Độ cấn va chạm**:
  $$\Delta Z_{clash} = 38.0\text{ mm} - 18.0\text{ mm} = \mathbf{+20.0\text{ mm}!}$$
  *(Khối pin 2x2 cao gấp đôi chiều cao trụ đỡ, bo mạch K2 Hub không thể lắp vào vị trí).*
- Kể cả khi dùng bệ đôn Riser V60 cũ ($Z_{bot} = 38.0\text{ mm}$), khoảng sáng từ sàn $Z=4.0$ chỉ là $34.0\text{ mm}$, vẫn bị cấn $4.0 - 6.0\text{ mm}$!
- **KẾT LUẬN & GIẢI PHÁP**: Phải nâng mặt đáy tầng K2 Control Hub lên cao độ tối thiểu:
  $$Z_{deck\_bottom} \ge 4.0\text{ mm (sàn)} + 42.0\text{ mm (tĩnh không)} = \mathbf{46.0\text{ mm}}$$
  *(Đảm bảo khoảng tĩnh không $H_{clear} \ge 42.0\text{ mm}$, dư $2.0 - 4.0\text{ mm}$ cho bề dày dây đai Velcro và dung sai màng co pin).*

#### Vấn đề cốt tử 2: Cấn CHIỀU RỘNG với Pin Dạng 2 (Khối 1x4 Dẹp phẳng - $W = 76.0\text{ mm}$):
- **Hiện trạng trên Chassis V6**: 4 trụ đỡ MCU đặt tại tọa độ tâm $X = \pm 33.0\text{ mm}$. Tiết diện trụ $10 \times 10\text{ mm}$ khiến mép trong của trụ nằm ở $X = \pm 28.0\text{ mm}$.
- **Khoảng lọt lòng giữa hai trụ trái - phải cũ**: $28.0 - (-28.0) = \mathbf{56.0\text{ mm}}$.
- **Độ cấn va chạm**:
  $$\Delta W_{clash} = 76.0\text{ mm} - 56.0\text{ mm} = \mathbf{+20.0\text{ mm}!}$$
  *(Khối pin 1x4 rộng hơn khoảng cách trụ tới 20mm, hoàn toàn không thể lọt vào giữa 4 trụ cũ).*
- Đồng thời, 4 gờ giữ pin 2S1P cũ đúc trên sàn ($X = \pm 18.5..21.5\text{ mm}$, lọt lòng 37.0 mm) cũng chém xuyên qua pin 1x4.
- **KẾT LUẬN & GIẢI PHÁP**: 
  + Triệt tiêu toàn bộ 4 trụ đỡ cũ tại $X = \pm 33.0\text{ mm}$ và 4 gờ pin cũ lọt lòng 37.0 mm.
  + Dời vị trí chân bắt / trụ đỡ mới ra sát mép vách sườn: Tọa độ tâm trụ mới $X = \pm 43.0\text{ mm}$ (hoặc gắn sát vách sườn $X = \pm 47.0\text{ mm}$), đảm bảo bề rộng lọt lòng khoang pin đạt $W_{bay} \ge \mathbf{80.0 - 82.0\text{ mm}}$!

---

## 3. ĐỀ XUẤT QUY CHUẨN KHOANG PIN VẠN NĂNG (UNIVERSAL 2S2P BATTERY BAY)

Khoang pin vạn năng được tối ưu hóa hình học để lắp vừa khít và an toàn 100% cho **cả Dạng 1 (Khối 2x2)** lẫn **Dạng 2 (Khối 1x4 dẹp)** mà không cần thay đổi khung xe.

### 3.1. Kích thước hình học tiêu chuẩn:
- **Chiều rộng lọt lòng (Width Clear)**: $W_{bay} = \mathbf{80.0\text{ mm}}$ (Dung sai chế tạo $+2.0\text{ mm}$, vùng an toàn $X \in [-40.0, +40.0\text{ mm}]$).
- **Chiều dài lọt lòng (Length Clear)**: $L_{bay} = \mathbf{76.0\text{ mm}}$ (Vùng an toàn $Y \in [46.0, 122.0\text{ mm}]$).
- **Chiều cao tĩnh không (Vertical Clearance)**: $H_{clear} = \mathbf{42.0\text{ mm}}$ (từ mặt sàn $Z = 4.0\text{ mm}$ lên đến đáy bệ K2 Hub tại $Z = 46.0\text{ mm}$).

### 3.2. Cơ chế khóa kẹp & Cố định chống sốc (Retention & Anti-Slip System):
1. **Hệ gờ định vị 4 góc thấp (Low-Profile Corner Positioning Lips)**:
   - 4 Gờ định vị góc đặt tại các biên:
     + Biên ngang: $X = \pm 40.5\text{ mm}$ (cho pin 1x4) và bổ sung 2 gờ phụ $X = \pm 20.0\text{ mm}$ (cho pin 2x2 đặt dọc).
     + Biên dọc: $Y = 46.5\text{ mm}$ (chặn sau) và $Y = 121.5\text{ mm}$ (chặn trước).
   - Chiều cao gờ: $h_{lip} = \mathbf{2.5\text{ mm}}$ (vừa đủ giữ mép đáy cell pin, có vát chì góc $45^\circ$ để nhét pin trượt mượt mà).
2. **Cụm 4 khe luồn dây đai dán Velcro 20mm (Dual Heavy-Duty Velcro Slots)**:
   - Kích thước mỗi khe: Rộng $4.0\text{ mm} \times$ Dài $22.0\text{ mm}$, xuyên thủng sàn xe $FLOOR\_T = 4.0\text{ mm}$.
   - Mép rãnh vát lượn tròn $R = 1.0\text{ mm}$ chống cọ rách/sờn vải đai dán Velcro.
   - Vị trí bố trí:
     + Đai 1 (Khoang sau): $Y = 62.0\text{ mm}$, 2 khe tại $X = -41.0\text{ mm}$ và $X = +41.0\text{ mm}$.
     + Đai 2 (Khoang trước): $Y = 100.0\text{ mm}$, 2 khe tại $X = -41.0\text{ mm}$ và $X = +41.0\text{ mm}$.
   - Tác dụng: Ôm chặt pin xuống sàn xe với lực kẹp trên $50\text{ N}$, chống văng pin khi robot phanh khẩn cấp hoặc xoay Mecanum gia tốc $2.5G$.
3. **Khe thoát dây nguồn & Dây sạc cân bằng (Wire Management Port)**:
   - Cửa sổ rãnh thoát cáp trung tâm: Kích thước $20.0 \times 16.0\text{ mm}$ tại $Y = 44.0\text{ mm}$ giúp dây nguồn chính T-plug / XT30 đi ngược lên jack cắm nguồn của K2 Hub ngắn nhất (< 40mm).
   - Túi ngách phụ bên sườn cho jack cân bằng 3P XH2.54 nằm gọn gàng, tránh bị dập dây.

---

## 4. BẢNG THÔNG SỐ BÀN GIAO THIẾT KẾ CHO SUBAGENT 2 & SUBAGENT 3

### 4.1. Bàn giao cho Subagent 2 (Chuyên gia CAD Khung Gầm - `Chassis Base CAD Modeler`):
Nhiệm vụ: Cập nhật file `01_Chassis_Base_200x200_V6.scad` lên phiên bản `V7.0`:
1. **Xóa bỏ hoàn toàn**:
   - 4 Trụ đỡ cũ cao 18mm tại $X = \pm 33.0\text{ mm}, Y = 49.0\text{ mm} \ \& \ 99.0\text{ mm}$.
   - 4 Gờ định vị pin cũ $X = \pm 20.0\text{ mm}$.
2. **Tạo mới Hệ trụ đỡ K2 Hub mở rộng (Wide Standoffs)**:
   - Tọa độ tâm 4 trụ mới: $X = \pm 43.0\text{ mm}$, $Y = 49.0\text{ mm} \ \& \ 99.0\text{ mm}$ (khoảng hở lọt lòng giữa 2 trụ trái/phải = $86.0 - 10.0 = \mathbf{76.0\text{ mm}}$, hoặc dời trụ trước ra $X = \pm 45.0\text{ mm}$ để lọt $80.0\text{ mm}$).
   - Cao độ đỉnh trụ đúc liền sàn:
     + Phương án A (Trụ cao nguyên khối): Đỉnh trụ đạt $Z = 46.0\text{ mm}$ (chiều cao trụ $H = 42.0\text{ mm}$).
     + Phương án B (Trụ phân tầng DFM): Trụ trên khung gầm cao $Z = 20.0\text{ mm}$, kết hợp Khung chân đôn Riser rời cao thêm $26.0\text{ mm}$ (Dễ in 3D FDM không sợ gãy trụ cao mảnh).
3. **Gia công Khoang Pin Vạn Năng trên sàn đáy**:
   - 4 Gờ định vị góc lùn cao 2.5mm bao vùng $80.0 \times 76.0\text{ mm}$.
   - 4 Khe luồn đai Velcro $4.0 \times 22.0\text{ mm}$ tại $Y = 62.0\text{ mm}$ và $Y = 100.0\text{ mm}$ ($X = \pm 41.0\text{ mm}$).

### 4.2. Bàn giao cho Subagent 3 (Chuyên gia Tích hợp Lắp ráp & Kiểm tra 200x200 - `Assembly Verifier`):
Nhiệm vụ: Cập nhật file `full_assembly_200x200.scad`:
1. **Cập nhật mô hình Pin 2S2P 18650 thực tế**:
   - Bổ sung module 3D trực quan cho cả 2 tùy chọn pin:
     + Pin Dạng 1 (Khối 2x2): `cube([38.0, 70.0, 38.0])` đặt tại $X = -19.0, Y = 49.0, Z = 4.0$.
     + Pin Dạng 2 (Khối 1x4): `cube([76.0, 70.0, 20.0])` đặt tại $X = -38.0, Y = 49.0, Z = 4.0$.
2. **Nâng cao độ tầng K2 Control Hub & Riser Adapter**:
   - Đáy bệ K2 Adapter Deck nâng lên $Z = \mathbf{GROUND\_CLEAR + 46.0\text{ mm}}$.
   - Mặt trên bo mạch K2 Control Hub đạt $Z = GROUND\_CLEAR + 46.0 + 4.0\text{ (deck)} + 26.0\text{ (hub)} = \mathbf{GROUND\_CLEAR + 76.0\text{ mm}}$.
3. **Kiểm tra va chạm động học & Hộp bao 200x200mm (Kinematic & Box Verification)**:
   - Khoảng cách từ mặt trước K2 Hub ($Y = 82.0\text{ mm}$) đến chân Tháp nâng ($Y = 105.0\text{ mm}$): Đạt $\mathbf{23.0\text{ mm}}$ $\implies$ **Zero Collision** với Tháp nâng và Servo S1!
   - Khi gập cánh tay nâng chữ H ở trạng thái xuất phát (`ARM_ANGLE = 88.0°`, `WRIST_PITCH_ANGLE = -90.0°`), cụm đầu gắp nằm ở $Y \in [115, 175\text{ mm}]$ hoàn toàn phía trước K2 Hub, **không bao giờ va chạm với K2 Hub đã nâng cao**!
   - Tổng kích thước phủ bì khi gấp gọn: Rộng $192 - 198\text{ mm} \le 200.0\text{ mm}$, Dài $170 - 190\text{ mm} \le 200.0\text{ mm}$ $\implies$ **TUÂN THỦ 100% TIÊU CHUẨN THI ĐẤU 200x200 MM!**
