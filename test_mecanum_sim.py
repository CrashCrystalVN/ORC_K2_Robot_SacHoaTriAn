import itertools
import numpy as np

# Robot geometry from full_assembly.scad and config.py
# FL: X = -90 mm, Y = +55 mm
# FR: X = +90 mm, Y = +55 mm
# RL: X = -90 mm, Y = -55 mm
# RR: X = +90 mm, Y = -55 mm
w = 90.0  # mm
L = 55.0  # mm

def run_sim(title, F_forward):
    print(f"\n{'='*25} {title} {'='*25}")
    print("Force vectors when each wheel spins FORWARD (+1):")
    wheel_names = ["FL (m1)", "FR (m2)", "RL (m3)", "RR (m4)"]
    for name, f in zip(wheel_names, F_forward):
        print(f"  {name:8s}: Fx = {f[0]:+5.1f}, Fy = {f[1]:+5.1f}")
        
    print(f"\n{'m1':>3} {'m2':>3} {'m3':>3} {'m4':>3} | {'Fx':>5} {'Fy':>5} {'Torque':>10} | {'Behavior'}")
    print("-" * 55)
    
    pure_strafe = []
    pure_turn = []
    pure_drive = []
    
    for signs in itertools.product([-1, 1], repeat=4):
        m1, m2, m3, m4 = signs
        m = np.array([m1, m2, m3, m4])
        
        # Individual forces
        f1 = F_forward[0] * m1
        f2 = F_forward[1] * m2
        f3 = F_forward[2] * m3
        f4 = F_forward[3] * m4
        
        # Total force
        Fx = f1[0] + f2[0] + f3[0] + f4[0]
        Fy = f1[1] + f2[1] + f3[1] + f4[1]
        
        # Torque tau = x * Fy - y * Fx
        t1 = (-w) * f1[1] - (+L) * f1[0]
        t2 = (+w) * f2[1] - (+L) * f2[0]
        t3 = (-w) * f3[1] - (-L) * f3[0]
        t4 = (+w) * f4[1] - (-L) * f4[0]
        tau = t1 + t2 + t3 + t4
        
        desc = []
        if abs(Fy) > 0.1: desc.append("FW" if Fy > 0 else "BW")
        if abs(Fx) > 0.1: desc.append("RIGHT" if Fx > 0 else "LEFT")
        if abs(tau) > 0.1: desc.append("SPIN_CCW" if tau > 0 else "SPIN_CW")
        if not desc: desc.append("STILL")
        b_str = "+".join(desc)
        
        print(f"{m1:3d} {m2:3d} {m3:3d} {m4:3d} | {Fx:5.1f} {Fy:5.1f} {tau:10.1f} | {b_str}")
        
        if abs(Fy) < 1e-4 and abs(tau) < 1e-4 and abs(Fx) > 1e-4:
            pure_strafe.append((signs, Fx))
        if abs(Fx) < 1e-4 and abs(Fy) < 1e-4 and abs(tau) > 1e-4:
            pure_turn.append((signs, tau))
        if abs(Fx) < 1e-4 and abs(tau) < 1e-4 and abs(Fy) > 1e-4:
            pure_drive.append((signs, Fy))
            
    print("\n--- Summary ---")
    print("Pure Drive (Tiến/Lùi thuần túy):", pure_drive)
    print("Pure Strafe (Đi ngang thuần túy):", pure_strafe)
    print("Pure Turn (Quay tại chỗ thuần túy):", pure_turn)

# 1. P1: Slide 7 Top View is 'X' -> Bottom Contact Rollers form 'O'
# FL contact roller slope dy/dx = +1 -> F_FL = (-1, +1)
# FR contact roller slope dy/dx = -1 -> F_FR = (+1, +1)
# RL contact roller slope dy/dx = -1 -> F_RL = (+1, +1)
# RR contact roller slope dy/dx = +1 -> F_RR = (-1, +1)
run_sim("P1: Slide 7 Standard (Top 'X' -> Ground 'O')", [
    np.array([-1.0, 1.0]),
    np.array([ 1.0, 1.0]),
    np.array([ 1.0, 1.0]),
    np.array([-1.0, 1.0])
])

# 2. P2: Ground Contact Rollers form 'X' (Top 'O')
# FL contact roller slope dy/dx = -1 -> F_FL = (+1, +1)
# FR contact roller slope dy/dx = +1 -> F_FR = (-1, +1)
# RL contact roller slope dy/dx = +1 -> F_RL = (-1, +1)
# RR contact roller slope dy/dx = -1 -> F_RR = (+1, +1)
run_sim("P2: Inverted (Top 'O' -> Ground 'X')", [
    np.array([ 1.0, 1.0]),
    np.array([-1.0, 1.0]),
    np.array([-1.0, 1.0]),
    np.array([ 1.0, 1.0])
])
