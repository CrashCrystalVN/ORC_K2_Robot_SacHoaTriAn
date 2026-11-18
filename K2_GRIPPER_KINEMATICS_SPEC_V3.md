# K2 GRIPPER V3.0: MATHEMATICAL & KINEMATIC SPECIFICATION
(See complete artifact at C:\Users\vuasu\.gemini\antigravity\brain\4aec65c5-8810-45f2-abf3-a1c4a662f836\K2_GRIPPER_KINEMATICS_SPEC_V3.md)

## Master Parameters for @base_cad and @jaws_cad:
- Axle Center Distance: C = 30.00 mm (X_L = -15.00, X_R = +15.00)
- Module m = 1.50 mm, z = 20 teeth, Dp = 30.00 mm, Rp = 15.00 mm
- Pressure Angle alpha = 20.0 deg
- Base radius Rb = 14.0954 mm, Addendum Ra = 16.50 mm, Dedendum Rf = 13.125 mm
- Normal Backlash jn = 0.350 mm (Tooth thinning delta_s = 0.1862 mm, s_actual = 2.170 mm)
- Stroke: Servo theta in [30 deg, 105 deg] -> Delta theta = 75.0 deg
- Jaw rotation: theta_jaw = 0 deg (Closed / Clamped on D32 tube) -> 75 deg (Wide open, tip gap > 220 mm)
- Clamping geometry: Cylinder D=32mm (R=16mm) at Y_c = 45.0 mm
  - 4-point contact at X = +- 11.314 mm, Y = Y_c +- 11.314 mm
  - 90 deg V-groove vertex at X = +- 22.627 mm, Y = Y_c
  - Clamping force = 21.8 N, Holding friction = 21.6 N (Safety margin 73x vs 30g tube)
- CSG collision check across 0 - 75 deg: 0.00000 mm^3 interference.
