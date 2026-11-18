# K2 ULTRA-COMPACT 2-PART DIRECT-DRIVE LIFT TOWER V1.1: SPECIFICATION & KINEMATIC MASTER (OPTION A)
(See complete artifact at C:\Users\vuasu\.gemini\antigravity\brain\4aec65c5-8810-45f2-abf3-a1c4a662f836\K2_TOWER_2PART_SPEC_V1.md)

## Master Parameters for @base_cad and @jaws_cad (Updated per Coordinator Directive #29):
1. Chassis Interface: 10 M3 bolts (5 per stanchion)
   - Left Stanchion: X = -16.0 (Y = 110.5, 122.0, 160.25) & X = -24.0 (Y = 116.0, 160.25)
   - Right Stanchion: X = +16.0 (Y = 110.5, 122.0, 160.25) & X = +24.0 (Y = 116.0, 160.25)
   - Counterbores: Dia 6.5mm x 3.5mm deep on top of stanchion feet (T_foot = 6.0mm).

2. Pitch Pivot Axis (Option A): Coaxial at Y_pivot = 160.25 mm, Z_pivot = 58.00 mm.
   - Upright column rises directly above front foot at Y = 160.25 mm.
   - Diagonal truss brace slopes BACKWARD to rear feet (Y = 110.5 .. 122.0 mm).
   - Space forward of Y = 160.25 mm is 100% open air (ZERO collision with Gripper Base Head V3!).
   - Left Stanchion Outer Pivot Face: X = -27.00 mm (M3 through-hole Dia 3.4mm + M3 locknut pocket / brass insert).
   - Right Stanchion Outer Pivot Face: X = +27.00 mm (MG996R spline coaxial, Dia 21.2mm x 3.0mm horn recess + Dia 7.0mm screwdriver tunnel).
   - External span between pivot faces: exactly 54.00 mm (matches 54.00 mm internal clevis span of Gripper Base Head V3!).

3. Kinematic Range:
   - Ground picking: theta_pitch = -15.0 deg (tube at Z = 26.2mm, tip at Z = 10.7mm above ground, reach = 57.6mm past bumper).
   - Horizontal transit: theta_pitch = 0.0 deg (tube at Z = 45.0mm, tip at Z = 45.0mm above ground).
   - Scoring lift: theta_pitch = +45.0 deg (tube at Z = 109.1mm, tip at Z = 151.5mm above ground).
   - Stowed upright: theta_pitch = +90.0 deg (Y_tip = 193.25mm <= 200mm, Z_tip = 215.0mm << 500mm).
   - Stowed tilted: theta_pitch = +95.0 deg (Y_tip = 181.18mm, Margin inside 200mm box = 18.82mm).

4. Collision Clearances:
   - Tower to Gripper: 0.0000 mm^3 interference across ALL angles (-15 deg to +95 deg).
   - Battery deck: Delta Y >= 46.0 mm clearance (ZERO collision).
   - Front sensor: fully unobstructed.
   - Robot 200x200mm box: fits with 6.75mm to 18.8mm safety margin.
