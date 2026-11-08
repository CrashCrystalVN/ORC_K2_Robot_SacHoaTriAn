# TRỌN BỘ GIẢI PHÁP ROBOT THI ĐẤU ORC-X1 PRO UNIBODY MECANUM (V3.1 - FULL MG996R)
**GIẢI ĐẤU "SẮC HOA TRI ÂN" - STEM THPT NGÔ QUYỀN & KỶ NIỆM NGÀY NHÀ GIÁO VN 20/11**
*Thiết kế cơ khí tối ưu hiện đại bằng công nghệ In 3D & Cơ học robot chuẩn quốc tế – Đã chuẩn hóa 100% cho 2 Servo MG996R, Mặt bích GA25 & Cánh tay gạt*

---

## 1. TỔNG QUAN GIẢI PHÁP CƠ KHÍ V3.1 (ĐÃ RÀ SOÁT TOÀN DIỆN)

1. **Khung gầm Monocoque Unibody liền khối (`01_Monocoque_Chassis_GA25_Mecanum`):**
   * **Vách mặt bích động cơ GA25 dày $4.0\text{ mm}$ nguyên vẹn:** Lỗ cổ trục $\varnothing 9.0\text{ mm}$ (lọt chuẩn cổ $\varnothing 7.0\text{ mm}$ của GA25) + **4 lỗ ốc M3 ($\varnothing 3.3\text{ mm}$) trên vòng chia chuẩn $\text{PCD } \varnothing 17.0\text{ mm}$** ($0^\circ, 90^\circ, 180^\circ, 270^\circ$).
   * **4 Ổ đỡ & Nắp kẹp động cơ GA25 (`02_GA25_Motor_Clamp_Cap`):** Rãnh bán nguyệt $\varnothing 25.4\text{ mm}$ ôm dọc theo trục $X$, cố định bằng 2 ốc M3 tại $dy = \pm 17.5\text{ mm}$ (nằm hoàn toàn trên mặt tai phẳng ngoài thân động cơ, vặn vít thẳng đứng từ trên xuống không bị cấn).
   * **4 Cột trụ bắt mạch ORC Control Hub ($65 \times 55\text{ mm}$):** Có sẵn **4 lỗ ốc M3 ($\varnothing 3.0\text{ mm}$ sâu $19\text{ mm}$)** tại $X = \pm 32.5\text{ mm}, Y = 80.0 \pm 27.5\text{ mm}$.
   * **Bệ gá Mạch nhận tín hiệu tay cầm PS4 (I2C Receiver):** Tích hợp ở sườn trái kèm **2 lỗ bu-lông M4 ($\varnothing 4.2\text{ mm}$ cách nhau $16.0\text{ mm}$)** chuẩn tài liệu Canva OhStem.
   * **Cảm biến siêu âm HC-SR04 & Cảm biến dò line:** Mũi cản trước có 2 hốc mắt $\varnothing 16.4\text{ mm}$ cách nhau $26.0\text{ mm}$, kèm 2 lỗ ốc M3 dưới gầm mũi xe ($X = \pm 12.0, Y = 160.0$) cho thanh dò line 4 mắt.
   * **Hộc chứa Pin Li-ion 2S hạ trọng tâm:** Lọt lòng $38 \times 54 \times 18\text{ mm}$ đặt sát đáy tâm xe.

2. **Tháp nâng đối xứng & Cánh tay song hành 4 khâu chữ H dùng Servo MG996R (`S1`):**
   * **Hốc lắp chuẩn Servo MG996R (S1) trên tháp phải:** Kích thước hốc thân $41.2 \times 20.2\text{ mm}$, kèm **4 lỗ ốc M3/M4 ($\varnothing 3.4\text{ mm}$) chuẩn $48.5 \times 10.0\text{ mm}$** trên mặt phẳng $X = +28.0\text{ mm}$ (cách mặt cánh tay gạt tại $X = +17.5\text{ mm}$ đúng $10.5\text{ mm}$ theo kích thước thực tế của MG996R).
   * **Khung tay nâng dưới chữ H (`03_Parallel_Arm_Truss_IBeam`):** Dài $98.0\text{ mm}$, có thanh giằng ngang chữ H nối cứng 2 bên trái/phải chống xoắn vặn $100\%$. Đầu gốc bên phải tích hợp **Hốc âm lắp Cánh tay gạt (Servo Horn) MG996R** đồng trục tại $(Y = 115.0, Z_{\text{local}} = 58.0)$ kèm 2 lỗ vít khóa cánh tay gạt ($\varnothing 2.3\text{ mm}$).
   * **Khung tay nâng trên chữ H (`03B_Upper_H_Frame_Follower_Arm`):** Giữ góc đầu kẹp hoa luôn thẳng đứng $90.0^\circ$ bất biến ở mọi cao độ.

3. **Cụm đầu kẹp hoa $\varnothing 32.0\text{ mm}$ tự định tâm V-Guide dùng Servo MG996R (`S2`):**
   * **Bệ đầu kẹp (`04_Gripper_Base_Head`):** Tích hợp cầu gá trên cho **Servo MG996R (S2)** đặt chúc trục xuống, mặt cầu ở $Z = 35.0\text{ mm}$ (cách mặt cánh tay gạt tại $Z = 24.5\text{ mm}$ đúng $10.5\text{ mm}$), có hốc $41.2 \times 20.2\text{ mm}$ và **4 lỗ ốc bắt tai MG996R chuẩn $48.5 \times 10.0\text{ mm}$** lộ thiên hoàn toàn từ mặt trên.
   * **Hàm kẹp phải chủ động (`06_Gripper_Jaw_Right_VGuide_Flower32`) & Hàm kẹp trái (`05_Gripper_Jaw_Left_VGuide_Flower32`):**
     - Khoảng cách 2 tâm trục xoay $= 28.0\text{ mm}$ ($X = \pm 14.0\text{ mm}, Y = 32.0\text{ mm}$).
     - Hàm phải đồng trục với trục ra của Servo MG996R S2, mặt trên có **Hốc âm lắp Cánh tay gạt (Servo Horn) MG996R** kèm 2 lỗ vít khóa.
     - **Bánh răng rẻ quạt ($R_{\text{pitch}} = 14.0\text{ mm}$) đặt lệch pha nửa bước răng ($9^\circ$):** Ăn khớp khít tại $(X = 0, Y = 32.0)$, truyền động đồng bộ cho cả 2 hàm đóng/mở đối xứng tuyệt đối.
     - **Máng ôm bán nguyệt $R_{in} = 16.5\text{ mm}$ + Phễu V-Guide mở rộng $72.0\text{ mm}$ + Gờ đỡ đáy $3.0\text{ mm}$:** Tự định tâm ống hoa $\varnothing 32.0\text{ mm}$, cách cầu servo $6.5\text{ mm}$ hoàn toàn không cạ vướng, chống rơi tuột hoa $100\%$.

---

## 2. CẤU TRÚC TỆP DỰ ÁN

```
ORC_K2_Robot_SacHoaTriAn/
│
├── cad_core.py                                  # Nhân hình học 3D ORC-X1 Pro V3.1 (OpenCASCADE)
├── README.md                                    # Tài liệu kỹ thuật toàn diện
├── flash_to_orc_hub.py                          # Script nạp firmware tự động vào ORC Control Hub
├── vfs_ready_to_flash.bin                       # Phân vùng LittleFS 2MB đã đóng gói
│
├── STEP_Models/                                 # File CAD STEP ISO 10303 (V3.1 - Full MG996R)
│   ├── 00_ORC_X1_Pro_Unibody_Full_Assembly.step # Lắp ráp tổng thể toàn bộ xe (49.460 entities)
│   ├── 01_Monocoque_Chassis_GA25_Mecanum.step   # Khung gầm unibody liền khối
│   ├── 02_GA25_Motor_Clamp_Cap.step             # Nắp kẹp ôm động cơ GA25
│   ├── 03_Parallel_Arm_Truss_IBeam.step         # Khung tay nâng dưới chữ H (có hốc Horn MG996R)
│   ├── 03B_Upper_H_Frame_Follower_Arm.step      # Khung tay nâng trên chữ H
│   ├── 04_Gripper_Base_Head.step                # Bệ đầu kẹp hoa tích hợp cầu gá Servo MG996R
│   ├── 05_Gripper_Jaw_Left_VGuide_Flower32.step # Hàm kẹp trái V-Guide & gờ đỡ đáy
│   ├── 06_Gripper_Jaw_Right_VGuide_Flower32.step# Hàm kẹp phải V-Guide (có hốc Horn MG996R)
│   ├── 07_Mecanum_Wheel_K3_80mm.step            # Vành bánh xe Mecanum K3 Ø80mm
│   └── 08_MG996R_Servo_Lever_Horn.step          # Cánh tay gạt Servo MG996R rời (dự phòng)
│
├── 3D_Models/                                   # File 3D STL sẵn sàng in trực tiếp (Watertight Manifold)
│   ├── full_assembly.scad                       # File mã nguồn lắp ghép OpenSCAD V4.2
│   ├── 00_ORC_X1_Pro_Unibody_Full_Assembly.stl
│   ├── 01_Monocoque_Chassis_GA25_Mecanum.stl
│   ├── 01B_Lift_Tower_Left_FlatPrint.stl
│   ├── 01C_Lift_Tower_Right_MG996R_FlatPrint.stl
│   ├── 01D_MCU_Control_Hub_Deck_FlatPrint.stl
│   ├── 01D_K2_Hub_Adapter_Plate.stl             # TẤM BỆ ADAPTER K2 CONTROL HUB V5.0 (HỐC TÁN NGANG, ĐÁY KÍN)
│   ├── 01D_Riser_Standoff_18mm.stl              # 4x TRỤ ĐỆM ĐÔN CAO 18MM (VƯỢT ĐỈNH MOTOR SAU 4.0MM)
│   ├── 01D_K2_Control_Hub_Riser_Adapter_Monolithic.stl # BẢN ADAPTER LIỀN KHỐI 1 CHI TIẾT V5.0 (0% SUPPORT)
│   ├── 01E_Line_Sensor_Spacer_Pod_FlatPrint.stl
│   ├── 02_GA25_Motor_Clamp_Cap.stl              # Nẹp động cơ trước
│   ├── 02B_GA25_Rear_Motor_Clamp_Left.stl       # NẸP ĐỘNG CƠ SAU - TRÁI V4.3 (VÒM Ø26.2MM, CÁCH TRỤ MCU 2.5MM)
│   ├── 02C_GA25_Rear_Motor_Clamp_Right.stl      # NẸP ĐỘNG CƠ SAU - PHẢI V4.3 (VÒM Ø26.2MM, CÁCH TRỤ MCU 2.5MM)
│   ├── 02_GA25_Rear_Motor_Clamp_Universal.stl   # NẸP ĐỘNG CƠ SAU DÙNG CHUNG V4.3 (LẮP CẢ 2 BÊN)
│   ├── 03_Parallel_Arm_Truss_IBeam.stl
│   ├── 03B_Upper_H_Frame_Follower_Arm.stl
│   ├── 04_Gripper_Base_Head.stl
│   ├── 05_Gripper_Jaw_Left_VGuide_Flower32.stl
│   ├── 06_Gripper_Jaw_Right_VGuide_Flower32.stl
│   ├── 07_Mecanum_Wheel_K3_80mm.stl
│   └── 08_MG996R_Servo_Lever_Horn.stl
│
├── 3MF_Models/                                  # File cấu hình khay in Bambu Lab A1 (0% Support, In Phẳng)
│   ├── 00_ORC_K2_V4.0_DFM_Bambu_A1_Full_Robot_2_Plates.3mf
│   ├── Plate_1_Khung_Gam_Chinh_Chassis.3mf
│   ├── Plate_2_Tay_Nang_HFrame_Va_4x_Nap_Kep_Motor.3mf
│   ├── Plate_3_Cum_Tay_Kep_Hoa_Va_Tay_Gat_MG996R.3mf
│   ├── Plate_4_Combo_Khung_Gam_Va_4x_Nap_Kep.3mf
│   ├── Plate_5_4x_Banh_Xe_Mecanum_K3_80mm.3mf
│   ├── Plate_6_K2_Control_Hub_Riser_Adapter_Patch.3mf  # KHAY IN VÁ 1: TẤM BỆ PHẲNG + 4 TRỤ ĐÔN + 2 NẸP SAU (30 PHÚT)
│   └── Plate_7_K2_Monolithic_Riser_Va_Nep_Motor_Sau.3mf# KHAY IN VÁ 2: BẢN LIỀN KHỐI 1 CHI TIẾT + 2 NẸP SAU (35 PHÚT)
│
└── Firmware/                                    # Mã nguồn điều khiển MicroPython (ORC Hub ESP32-S3)
    ├── config.py                                # Cấu hình chân cắm, động cơ GA25, Mecanum 202mm
    ├── maze_strategy.py                         # Chiến thuật tự động giải mê cung bằng IMU & Encoder
    └── main.py                                  # Vòng lặp chính, điều khiển Gamepad đa hướng & Combo kẹp hoa
```

---

## 3. GIẢI PHÁP NÂNG CẤP V5.0 (VÁ LÊN KHUNG GẦM ĐÃ IN - KHÔNG CẦN IN LẠI BASE)

Nhằm giữ nguyên khung gầm xe (`01_Chassis_Lower_Base` / `01_Monocoque_Chassis_GA25_Mecanum`) mà bạn đã in 3D xong, bộ phận cơ khí đã thiết kế lại trọn gói 2 cụm chi tiết:

### A. Tấm bắt bo mạch ORC K2 Control Hub V7.0 (Khắc phục triệt để 100% nghịch lý bắt ốc & kẹt motor)

- **Nguyên nhân gốc rễ khiến các bản V5.0 & V6.0 VẪN QUÁ KHÓ BẮT ỐC**:
  1. **Nghịch lý lắp ráp (Bắt K2 Hub trước thì che mất ốc đế, bắt đế trước thì không giữ được tán K2 Hub)**:
     - Nếu bắt tấm Plate xuống khung gầm trước: Bạn không thể thò ngón tay xuống gầm (do vướng 2 động cơ sau và vách sườn xe) để giữ 4 con tán M3 của K2 Hub.
     - Nếu dùng rãnh nhét tán ngang (Side-entry Nut Slot) hình chữ nhật rộng $6.2\text{ mm}$: Do khoảng cách 2 đỉnh lục giác của tán M3 chỉ là $6.08\text{ mm}$, khi vặn ốc thì **tán M3 bị xoay tròn bên trong rãnh ngang**, không tài nào siết chặt được!
     - Hơn nữa, ở bản V6.0, khối khoét thoát motor sau (`30x30x18.5mm`) đã vô tình cắt cụt mất 2 hốc tán sau của K2 Hub và cắt lẹm vào 2 chân trụ sau, còn ô thoáng giữa lại cắt thủng vách giếng ốc khiến ốc rơi tuột vào khoang pin!

- **Giải pháp cơ học hoàn thiện V7.0 (Bắt K2 Hub ở ngoài bàn trước + Hốc Lục Giác Khóa Tán 6 Cạnh + Ốc Đế Lộ Thiên Ngoài K2 Hub)**:
  Chúng tôi cung cấp **2 phương án V7.0** để bạn tùy chọn (cả 2 đều cho phép **bắt cứng K2 Control Hub vào tấm Plate ở ngoài bàn trên tay trước**, sau đó mới đưa lên xe khóa ốc lộ thiên):

  1. **Phương án 1: Bản Liền Khối 1 Chi Tiết V7.0 (`01D_K2_Control_Hub_Riser_Adapter_Monolithic.stl` - Khuyên dùng, gọn nhất)**:
     - **4 Góc bắt K2 Hub ($X = \pm 48.0, Y = 11.0 \text{ & } 83.0\text{ mm}$) tích hợp Hốc Lục Giác Âm 6 Cạnh ($\varnothing 6.45\text{ mm}, \$fn=6$) + Lỗ trên tự taro $\varnothing 2.9\text{ mm}$**:
       - Mặt dưới có hốc lục giác chuẩn 6 cạnh ôm khít tán M3, **khóa cứng 100% chống xoay tán**. Bạn cầm tấm Plate trên tay ở ngoài bàn, ấn 4 tán M3 vào mặt dưới và vặn 4 ốc cố định K2 Hub vào tấm Plate cực kỳ dễ dàng! (Hoặc vặn trực tiếp ốc M3 vào lỗ tự taro $\varnothing 2.9\text{ mm}$ mà không cần tán!).
       - Đáy sàn đôn lên cao độ **$Z = 37.5\text{ mm}$** (cao hơn đỉnh nẹp motor sau $Z = 36.0\text{ mm}$ tới $1.5\text{ mm}$ và cao hơn thân motor $5.0\text{ mm}$), giúp mặt sàn nguyên khối dày $5.0\text{ mm}$ không cần khoét thủng và **ốc sau không bao giờ chạm motor**!
     - **2 Chân Đôn Sau ($X = \pm 33.0, Y = 49.0\text{ mm}$) có Ngàm Chữ U Cài Trượt (Slide-In Fork)**:
       - Chỉ cần vặn hờ 2 ốc M3x10mm/12mm vào 2 trụ sau trên khung gầm (chừa khe $4\text{ mm}$ dưới mũ ốc). Khi cầm cụm `[K2 Hub + Plate]` đẩy trượt nhẹ từ trước ra sau, 2 ngàm chữ U dưới chân sau sẽ tự động ngậm khóa chặt vào 2 con ốc trụ sau mà không cần chọc tô-vít xuyên qua K2 Hub!
     - **2 Tai Trụ Trước Lộ Thiên ($X = \pm 33.0, Y = 99.0\text{ mm}$) nằm PHÍA TRƯỚC K2 Hub $9.0\text{ mm}$**:
       - Nhờ dịch vị trí K2 Hub về $Y \in [4.0, 90.0\text{ mm}]$, 2 trụ trước ($Y = 99.0\text{ mm}$) nằm **lộ thiên hoàn toàn ở phía trước bo mạch K2 Hub**, có giếng mở chữ U rộng $\varnothing 10.5\text{ mm}$ thông ra mặt trước và bên hông. Bạn nhìn thấy lỗ ốc rõ mồn một và đưa tô-vít thẳng đứng vặn 2 ốc M3x10mm/12mm khóa cứng mũi bệ trong 10 giây!

  2. **Phương án 2: Bộ 2 Tầng Tai Bắt Ốc Lộ Thiên V7.0 (`01D_Base_Riser_Frame.stl` + `01D_K2_Hub_Adapter_Plate.stl`)**:
     - **Bước 1**: Đặt `01D_Base_Riser_Frame` lên 4 trụ khung gầm ($X = \pm 33, Y = 49 \text{ & } 99$) khi chưa có K2 Hub che khuất — 4 hốc ốc mở chữ U cực rộng $\varnothing 10.5\text{ mm}$ lộ thiên 100%, vặn 4 ốc M3x10mm/12mm cực dễ.
     - **Bước 2**: Cầm tấm sàn phẳng `01D_K2_Hub_Adapter_Plate` ở ngoài bàn, bắt cứng K2 Control Hub vào tấm sàn nhờ 4 **Hốc Lục Giác Âm 6 Cạnh giữ tán M3 chống xoay** ở mặt dưới.
     - **Bước 3**: Đặt cụm `[K2 Hub + Tấm Sàn]` lên `Khung Chân Đôn` (ở cao độ $Z = 40.0\text{ mm}$, cách đỉnh nẹp motor sau $4.0\text{ mm}$) và vặn 4 ốc M3 từ trên xuống vào **4 Tai Bắt Ốc Lộ Thiên vươn ra ngoài K2 Hub** ($2$ tai sau tại $X = \pm 33, Y = 7.5\text{ mm}$ và $2$ tai trước tại $X = \pm 36, Y = 108.5\text{ mm}$)!

### B. 2 Nẹp động cơ GA25 phía sau (Rear Motor Clamps V4.3)
- **Nguyên nhân va chạm & cấn hộp số ở bản trước**:
  1. **Hộp số giảm tốc GA25 to hơn**: Động cơ GA25 có đường kính hộp số kim loại thực tế là $25.0 - 25.4\text{ mm}$ (nhiều loại vỏ hộp số hoặc gờ tán kim loại lên đến $25.6 - 25.8\text{ mm}$). Việc để vòm ôm $\varnothing 24.8\text{ mm}$ khiến nẹp bị kích, không thể chụp xuống ôm khít động cơ.
  2. **Chỉ khoét 1 chỗ ở tai sau**: Bản trước chỉ vát góc ở tai sau, trong khi phần thân vòm ôm (central arch) ở giữa vẫn giữ nguyên bề rộng kéo dài đến $X = \pm 32.0\text{ mm}$ nên đâm trực tiếp vào cột trụ MCU cũ tại $Y \in [44.0, 46.2\text{ mm}]$ (va chạm $6\text{ mm} \times 2.2\text{ mm} \times 2\text{ mm}$ ở cả 2 bên Trái và Phải).
- **Cải tiến thiết kế V4.3 (Chuẩn xác 100%, Zero Collision)**:
  - **Tăng đường kính vòm ôm lên $\varnothing 26.2\text{ mm}$**: Thoải mái ôm trọn mọi loại hộp số giảm tốc GA25 (kể cả hộp số ngoại cỡ có gờ gá hoặc vòng tán), kết hợp vát mép mở miệng $45^\circ$ ($\varnothing 27.5\text{ mm}$) ở cả 2 đầu ngoài và trong để trượt nhẹ nhàng không xước vỏ.
  - **Thu hẹp toàn bộ mép trong suốt chiều dài (cả 2 tai lẫn thân vòm ôm)**:
    - Mép trong thu hẹp về $|X| = 40.5\text{ mm}$ ($x = \pm 3.5\text{ mm}$ so với tâm lỗ ốc $X = \pm 44.0\text{ mm}$), tạo **khe hở an toàn tuyệt đối $2.5\text{ mm}$** so với 2 cột trụ MCU cũ trên khung gầm đã in ($X \in [-38, -28]$ và $[28, 38]$) trên toàn bộ cao độ từ đáy đến đỉnh.
    - Vát góc $45^\circ$ ở cả 2 góc trong để triệt tiêu mọi khả năng kẹt.
  - Cung cấp đủ 3 phiên bản:
    1. `02B_GA25_Rear_Motor_Clamp_Left.stl` (Nẹp sau Trái V4.3: vế ngoài $12\text{ mm}$, vế trong $3.5\text{ mm}$, in nằm phẳng Z=0).
    2. `02C_GA25_Rear_Motor_Clamp_Right.stl` (Nẹp sau Phải V4.3: đối xứng gương chuẩn).
    3. `02_GA25_Rear_Motor_Clamp_Universal.stl` (Nẹp sau Dùng Chung V4.3: thu hẹp đối xứng $8\text{ mm}$, lắp vừa cả 2 bên).

---

### C. Khay in nhanh cho Bambu Lab A1 / Slicer
- **`Plate_6_K2_Control_Hub_Riser_Adapter_Patch.3mf`**: Gồm Bộ 2 Tầng V7.0 (`01D_K2_Hub_Adapter_Plate` + `01D_Base_Riser_Frame` có 4 tai bắt ốc lộ thiên ngoài K2 Hub) + 2 Nẹp động cơ sau V4.3 (0% Support).
- **`Plate_7_K2_Monolithic_Riser_Va_Nep_Motor_Sau.3mf`**: Gồm Bản Liền Khối 1 Chi Tiết V7.0 (`01D_K2_Control_Hub_Riser_Adapter_Monolithic` có ngàm chữ U cài trượt chân sau + 2 tai trụ trước lộ thiên ngoài K2 Hub) + 2 Nẹp động cơ sau V4.3 (0% Support).

---

## 4. BẢNG TỔNG HỢP DANH MỤC ỐC VÍT CẦN DÙNG (FULL BOM SCREWS & FASTENERS)

Dưới đây là bảng kê chi tiết toàn bộ các loại bu-lông, đai ốc cần mua cho Robot ORC K2 (chuẩn M3 & M4 thép không gỉ / inox hoặc thép đen 12.9):

### A. Ốc vít dành riêng cho Bộ bản vá K2 Hub V5.0 & Nẹp động cơ sau
| STT | Loại ốc / Tán | Chiều dài ren | Số lượng | Vị trí lắp ráp & Chú thích kỹ thuật |
| :---: | :--- | :---: | :---: | :--- |
| 1 | **Bu-lông M3** | **$12\text{ mm}$** (hoặc $16\text{ mm}$) | **4 con** | Bắt tấm bệ Adapter V6.0 qua lỗ bậc chìm 14mm xuống 4 cột trụ khung gầm (dùng ngay ốc ngắn thông dụng, không cần ốc 30mm!). |
| 2 | **Bu-lông M3** | **$10\text{ mm}$** (hoặc $12\text{ mm}$) | **4 con** | Bắt cố định bo mạch ORC K2 Control Hub từ trên xuống vào 4 hốc tán ngang. |
| 3 | **Đai ốc (Tán) M3** | Chuẩn M3 ($5.4\text{ mm}$) | **4 con** | Trượt ngang từ cạnh bên vào 4 hốc nhét tán của bệ Adapter để siết bo mạch K2. |
| 4 | **Bu-lông M3** | **$12\text{ mm}$** (hoặc $10\text{ mm}$) | **4 con** | Bắt 2 nẹp động cơ sau (`02B` & `02C`) xuống khung gầm (mỗi nẹp 2 con). |

### B. Toàn bộ danh mục ốc vít cho toàn bộ Robot hoàn chỉnh
| STT | Hạng mục cụm cơ khí | Loại bu-lông | Số lượng | Chú thích lắp ghép |
| :---: | :--- | :--- | :---: | :--- |
| 1 | **Mặt bích 4 động cơ GA25** | M3 x $6\text{ mm}$ hoặc $8\text{ mm}$ | **16 con** | Bắt xuyên vách gầm $4\text{ mm}$ vào 4 lỗ ren M3 mặt bích động cơ GA25 (4 ốc/động cơ). |
| 2 | **4 Nắp kẹp ôm động cơ GA25** | M3 x $10\text{ mm}$ hoặc $12\text{ mm}$ | **8 con** | Cố định 2 nẹp trước + 2 nẹp sau ôm chặt động cơ vào khung xe (2 ốc/nẹp). |
| 3 | **Bệ bắt bo mạch ORC K2 Hub** | M3 x $30\text{ mm}$ | **4 con** | Bắt bệ adapter xuyên trụ đệm 18mm xuống 4 trụ khung gầm. |
| 4 | **Bắt bo mạch ORC K2 Hub** | M3 x $10\text{ mm}$ | **4 con** | Bắt 4 góc K2 Hub vào 4 tán ngang trên bệ adapter. |
| 5 | **Đai ốc (Tán) M3 cho bệ K2** | Tán lục giác M3 | **4 con** | Nhét vào 4 hốc tán ngang trên bệ adapter. |
| 6 | **Bắt 2 Tháp nâng (01B & 01C)** | M3 x $16\text{ mm}$ + Tán M3 | **6 bộ** | Cố định chân tháp nâng vào sườn xe (mỗi bên 3 ốc). |
| 7 | **Bắt Servo MG996R (S1 - Nâng tay)** | M3 x $12\text{ mm}$ hoặc $14\text{ mm}$ + Tán | **4 bộ** | Bắt 4 tai cao su giảm chấn của Servo MG996R vào vách tháp nâng phải. |
| 8 | **Bắt Servo MG996R (S2 - Kẹp hoa)** | M3 x $12\text{ mm}$ hoặc $14\text{ mm}$ + Tán | **4 bộ** | Bắt 4 tai của Servo MG996R vào cầu gá của bệ đầu kẹp hoa. |
| 9 | **Vít cánh tay gạt Servo Horn** | Vít ren nhọn $2.2 \times 8\text{ mm}$ (có sẵn trong túi phụ kiện MG996R) | **4 con** | Khóa cánh tay gạt kim loại/nhựa vào khớp tay nâng và hàm kẹp phải. |
| 10 | **Các trục khớp xoay tay nâng chữ H** | M3 x $25\text{ mm}$ hoặc $30\text{ mm}$ (dùng làm chốt xoay) + Tán tự khóa (Nyloc) | **4 bộ** | Làm trục quay cho 4 mắt khớp xoay song hành của tay nâng. |
| 11 | **Trục xoay 2 hàm kẹp hoa** | M3 x $25\text{ mm}$ + Tán tự khóa | **2 bộ** | Trục xoay độc lập cho hàm trái và hàm phải ăn khớp bánh răng. |
| 12 | **Bệ cảm biến dò line 4 mắt (01E)** | M3 x $10\text{ mm}$ | **2 con** | Bắt bệ đệm cảm biến dò line vào mũi gầm trước. |
| 13 | **Mạch nhận tín hiệu PS4 (I2C)** | M4 x $10\text{ mm}$ (hoặc M3 x $12\text{ mm}$) | **2 con** | Bắt mạch PS4 vào bệ sườn xe. |
| **TỔNG** | **Đầy đủ linh kiện bu-lông ốc vít** | | **~ 60 con** | **Khuyên dùng hộp vít combo M3 (dài từ 6mm đến 30mm) + túi tán M3 thông dụng.** |

---

## 5. CẢI TIẾN CỤM SERVO S1 NÂNG HẠ & CÁNH TAY ĐÒN V5.0 (CHUẨN ĐĨA TRÒN MG996R & CHỐNG CẤN ỐC 100%)

### A. Phân tích nguyên nhân gốc rễ (Root Cause Analysis)
1. **Lỗi cấn ốc bắt Servo S1 khóa cứng cánh tay nâng ("ốc bắt bị vướng")**:
   - Vách tháp nâng bên phải nằm ở tọa độ $X \in [20.0, 28.0\text{ mm}]$, dầm phải của cánh tay nâng song hành nằm ở $X \in [14.5, 19.5\text{ mm}]$ (khe hở thiết kế ban đầu chỉ là $0.5\text{ mm}$).
   - 2 lỗ ốc bắt mặt trước của servo MG996R nằm ở $Y = 158.9\text{ mm}$ ($13.9\text{ mm}$ phía trước trục quay $Y = 145.0\text{ mm}$).
   - Khi xỏ bu-lông M3 từ ngoài vào tháp và vặn tán M3 tiêu chuẩn ($2.4\text{ mm}$) ở mặt trong ($X = 20.0\text{ mm}$), đầu tán và phần ren thừa chìa ra đến $X = 17.6\text{ mm}$, **đâm sâu tới $1.9\text{ mm}$ trực tiếp vào quỹ đạo quay của dầm tay nâng**, khiến cánh tay nâng bị kẹt cứng, không thể hạ xuống!
2. **Vấn đề phụ kiện tay gạt: Servo MG996R chỉ có 1 đĩa tròn 25T**:
   - Phụ kiện thực tế đi kèm trong hộp servo MG996R (nhất là dòng servo nhông kim loại phổ biến) thường chỉ có **1 đĩa tròn kim loại/nhựa 25T đường kính $\varnothing 20.0\text{ mm}$** (có 4 lỗ ren M3 bố trí đối xứng trên đường kính vòng chia PCD $\varnothing 14.0\text{ mm}$).
   - Thiết kế cũ dùng khe dài hẹp $8.2\text{ mm}$ chỉ vừa cánh tay gạt đơn dài (single arm horn - vốn không có sẵn trong túi phụ kiện này).
3. **Ràng buộc thiết kế nghiêm ngặt**:
   - Giữ nguyên $100\%$ kết cấu thượng tầng: Trục quay tay dưới $Y = 145.0\text{ mm}, Z = 78.0\text{ mm}$, trục quay tay trên $Z = 106.0\text{ mm}$ (khoảng cách trục $28.0\text{ mm}$), tay đòn trên `03B`, đầu kẹp hoa `04` và khung gầm `01` không thay đổi tọa độ hình học.

---

### B. Giải pháp kỹ thuật triệt để trên Bản vẽ V5.0

#### 1. Tháp nâng phải V5.0 (`01C_Lift_Tower_Right_MG996R_FlatPrint.stl`)
- **4 Hốc chìm tán lục giác M3 (Recessed Hex Nut Pockets)**:
  - Bố trí chìm hoàn toàn vào mặt trong vách tháp ($X = 20.0\text{ mm}$) với kích thước $\varnothing 6.5\text{ mm}$, sâu $2.8\text{ mm}$ ($fn=6$).
  - Tán M3 tiêu chuẩn (dày $2.4\text{ mm}$) khi nhét vào sẽ nằm **chìm sâu $0.4\text{ mm}$ dưới bề mặt vách**, hoàn toàn không có bất kỳ chi tiết kim loại nào nhô ra cấn vào cánh tay nâng.
- **Khoét hạ bậc quét cánh tay (Inner Sweep Clearance Pocket)**:
  - Khoét sâu $1.2\text{ mm}$ bề mặt vách trong tháp nâng tại toàn bộ vùng quét $Y \in [138, 166\text{ mm}]$, $Z \in [44, 74\text{ mm}]$.
  - Mở rộng khe hở không khí giữa tay nâng và tháp từ $0.5\text{ mm}$ lên **$1.6\text{ mm}$**.
  - **Quy trình bắt ốc cực chuẩn**: Bu-lông M3x10mm xỏ từ ngoài qua tai servo rồi siết vào 4 tán M3 đã nhét chìm sẵn trong vách tháp. Mặt trong phẳng lì $100\%$.

#### 2. Cánh tay đòn nâng song hành dưới V5.0 (`03_Parallel_Arm_Truss_IBeam.stl`)
- **Hốc tròn ôm khít đĩa tròn 25T ($\varnothing 20.8\text{ mm}$, sâu $2.5\text{ mm}$)**:
  - Nằm ở mặt ngoài dầm phải ($X \in [17.0, 19.5\text{ mm}]$), ôm chuẩn xác đĩa tròn nhôm/nhựa $\varnothing 20.0\text{ mm}$ của servo MG996R, triệt tiêu hoàn toàn hiện tượng rơ lắc góc khi nâng tải nặng.
- **8 Lỗ bắt ốc M3 PCD $\varnothing 14.0\text{ mm}$ kèm lỗ bậc chìm đầu ốc**:
  - 8 lỗ chia góc $45^\circ$ ($r = 7.0\text{ mm}$) tương thích $100\%$ cả đĩa tròn 4 lỗ chữ thập ($0^\circ, 90^\circ, 180^\circ, 270^\circ$) lẫn đĩa tròn chữ X ($45^\circ, 135^\circ, 225^\circ, 315^\circ$).
  - Mặt trong dầm ($X = 14.5\text{ mm}$) được khoét lỗ bậc chìm $\varnothing 6.0\text{ mm}$ sâu $1.8\text{ mm}$.
  - **Bắt ốc**: Vặn 4 ốc M3x8mm từ mặt trong xuyên ra ăn vào ren đĩa tròn kim loại. Đầu ốc chìm hoàn toàn vào thân dầm, không cọ quẹt bất kỳ chi tiết nào.
- **Lỗ khóa trục trung tâm $\varnothing 6.5\text{ mm}$**:
  - Cho phép đưa đầu vít/lục giác xuyên qua tâm cánh tay để siết hoặc mở ốc khóa cốt servo 25T mà **không cần tháo rã toàn bộ cánh tay đòn**.
- **DFM in 3D 0% Support**:
  - Đáy tay nâng được cắt phẳng tại $Z = -6.0\text{ mm}$ ($Z_{\text{bed}} = 0$) kèm các chân tiếp xúc bàn in vững chắc, đảm bảo in nằm phẳng $100\%$ bám bàn cực tốt, không cần bất kỳ cấu trúc chống đỡ (support) nào.

#### 3. Khớp nối dẫn động đĩa tròn S1 rời V5.0 (`08_S1_MG996R_Round_Horn_Drive_Coupler.stl`)
- **Giải pháp tình huống cứu cánh 6 phút**:
  - Dành riêng cho trường hợp bạn đã in sẵn cánh tay cũ và không muốn in lại toàn bộ cánh tay dài.
  - Kích thước siêu nhỏ $23 \times 31.5 \times 6.5\text{ mm}$, thời gian in chỉ $\approx 6$ phút.
  - Mặt trước ôm khít đĩa tròn $\varnothing 20\text{ mm}$ với 4 lỗ M3 PCD $\varnothing 14\text{ mm}$, mặt sau có then mộng chữ nhật $8.0\text{ mm}$ ngàm khít vào rãnh $8.2\text{ mm}$ của tay cũ cùng 2 lỗ ốc M3 cố định ($Y = 10, 16\text{ mm}$).

---

### C. Khay in Bambu Lab A1 Plate 8
- **Tệp khay in**: `Plate_8_Cum_Servo_S1_Nang_Ha_Va_Tay_Nang.3mf`
- **Các chi tiết trên khay**:
  1. `01C_Lift_Tower_Right_MG996R_FlatPrint.stl` (Tháp nâng phải chống cấn ốc V5.0)
  2. `03_Parallel_Arm_Truss_IBeam.stl` (Tay đòn nâng đĩa tròn V5.0)
  3. `08_S1_MG996R_Round_Horn_Drive_Coupler.stl` (Khớp nối đĩa tròn Module rời)
- **Thông số in**: In nằm phẳng $Z=0$, $0\%$ Support, 4 wall loops, $25\%$ gyroid infill, thời gian in $\approx 42$ phút.

---

## 6. CỤM ĐẦU KẸP 3 TRỤ HOA GẬP DỌC $90^\circ$ TIẾT KIỆM DIỆN TÍCH V7.1 (PITCH-FOLDING TRIPLE-FLOWER GRIPPER)

Nhằm tăng gấp 3 lần tốc độ gom trụ hoa $\varnothing 32.0\text{ mm}$ mà vẫn có thể **gập dựng đứng cụm kẹp lên $90^\circ$ (Pitch quanh trục ngang $X$)** để tiết kiệm $105\text{ mm}$ chiều dài mũi xe khi xoay sở trong mê cung hẹp $248\text{ mm}$, cụm đầu kẹp được thiết kế thành hệ cổ tay gập chủ động dùng **Servo thứ 3 (S3 - MG996R)** và giữ nguyên $100\%$ bộ tay nâng chữ H (`03` & `03B`) đã in:

### A. Cổ Tay Nối Tay Nâng H-Frame & Gá Servo S3 Gập Dọc (`04A_Wrist_Clevis_Pitch_Bracket_S3.stl`)
- **Phía sau lắp vừa $100\%$ vào 4 chốt xoay của cánh tay chữ H cũ (`03` & `03B`)**: Giữ nguyên tọa độ 2 tai clevis ($X \in [\pm 8.5, \pm 14.0\text{ mm}]$) và 4 lỗ chốt tại $Y = 8.0\text{ mm}, Z = 10.0 \text{ & } 38.0\text{ mm}$, kèm **4 Hốc Lục Giác Âm ($\varnothing 6.5\text{ mm}$)** ở mặt trong để giữ chặt 4 tán M3 không cần kìm.
- **Khoang gá Servo S3 (MG996R) đặt dọc**:
  - Ôm khít thân Servo S3 tại $Y \in [16.6, 37.0\text{ mm}]$, trục quay hướng sang phải ($+X$) tại đúng cao độ $(Y_{\text{piv}} = 26.8\text{ mm}, Z_{\text{piv}} = 38.0\text{ mm})$.
  - 4 lỗ bắt tai Servo S3 ($X = +13.0\text{ mm}$) lộ thiên hoàn toàn bên sườn phải, có lỗ tự taro M3 sâu $8.5\text{ mm}$ kèm khoang nhét tán M3 mở phía trước.
  - Gối trục xoay đồng trục bên trái ($X = -27.0\text{ mm}$) đỡ đối xứng đầu bên kia của bệ kẹp `04`, chịu tải cắt kép (Double-Shear Support) chống xệ tuyệt đối.
- **In 3D phẳng mặt lưng tại $Z = 0.0\text{ mm}$ (`rotate([90, 0, 0])`) với $0\%$ Support**.

### B. Bệ Đầu Kẹp 3 Hoa Tích Hợp 2 Má Bản Lề Gập Dọc $90^\circ$ (`04_Gripper_Base_Head.stl`)
- **Cặp Má Bản Lề Gập Dọc $90^\circ$ tại $(Y_{\text{piv}} = 6.0\text{ mm}, Z_{\text{piv}} = 38.0\text{ mm})$**:
  - **Má Bản Lề Phải ($X \in [+27.0, +35.0\text{ mm}]$)**: Khoét sẵn **Hốc tròn âm $\varnothing 20.8\text{ mm}$ sâu $2.5\text{ mm}$ + 8 lỗ M3 trên $\text{PCD }\varnothing 14.0\text{ mm}$ + lỗ tâm $\varnothing 6.5\text{ mm}$** lắp vừa khít **Đĩa Tròn $\varnothing 20\text{ mm}$ của Servo S3** (vẫn giữ rãnh chữ nhật $8.2\text{ mm}$ cho tay gạt đơn).
  - **Má Bản Lề Trái ($X \in [-33.0, -27.0\text{ mm}]$)**: Lỗ trục xoay đồng trục $\varnothing 3.4\text{ mm}$ có bậc chìm đầu ốc M3, bắt thẳng vào gối xoay bên trái của cổ tay `04A`.
- **Hành trình gập dọc $0^\circ \leftrightarrow 90^\circ$ không va chạm**:
  - Khi hạ ngang ($0^\circ$): Cặp hàm kẹp vươn thẳng về phía trước để lùa và kẹp liên tiếp 3 trụ hoa $\varnothing 32\text{ mm}$ (hoặc hơi ngóc nhẹ $15^\circ$ khi di chuyển để chống quệt sàn).
  - Khi gập đứng ($90^\circ$): Toàn bộ cụm hàm kẹp dựng thẳng đứng theo phương $+Z$, thu ngắn chiều dài vươn trước của robot đi **$105\text{ mm}$**!
- **In 3D phẳng đáy $Z = 0.0\text{ mm}$ với $0\%$ Support** (nhờ đáy 2 má bản lề vát giọt nước ngược $45^\circ$ tự đỡ).

### C. Cặp Hàm Kẹp Liên Hoàn 3 Trụ Hoa V7.1 (`05_Gripper_Jaw_Left_VGuide_Flower32.stl` & `06_Gripper_Jaw_Right_VGuide_Flower32.stl`)
- **3 Hốc Kẹp Định Tâm Liên Hoàn ($\varnothing 32.2\text{ mm}$ tại $Y_1 = 33.0\text{ mm}, Y_2 = 66.0\text{ mm}, Y_3 = 99.0\text{ mm}$)** kèm phễu V-Guide $35^\circ$ và mấu sóng định tâm ($X = \pm 13.0\text{ mm}$).
- **3 Khe Đàn Hồi Lò Xo Lá Độc Lập (Independent Leaf-Spring Compliance Slots)** giúp ép chặt đồng đều cả 3 trụ hoa cùng lúc.
- **Gờ đỡ đáy vát $45^\circ$ ($R = 14.9\text{ mm}$) + 3 Rãnh gân ngang ma sát** + **Hốc Đĩa Tròn MG996R $\varnothing 20.8\text{ mm}$ trên Hàm Phải (`06`)**.

### D. Khay in Bambu Lab A1 cho Cụm Kẹp 3 Hoa Gập Dọc $90^\circ$
- **Tệp khay in**: `Plate_3_Cum_Tay_Kep_Hoa_Va_Tay_Gat_MG996R.3mf` (và đã cập nhật trực tiếp trong `Plate_2_Tay_Nang_HFrame_Va_4x_Nap_Kep_Motor.3mf` cùng `00_ORC_K2_V4.0_DFM_Bambu_A1_Full_Robot_2_Plates.3mf`).
- **Thông số in**: Toàn bộ 4 chi tiết (`04A`, `04`, `05`, `06`) đặt phẳng $100\%$ tại $Z = 0.0\text{ mm}$, **0% Support**, 4 wall loops, $35\%$ gyroid infill.
