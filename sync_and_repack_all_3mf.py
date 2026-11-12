"""
Sync & Repack Pipeline for Bambu Lab A1 3MF Packages
ORC K2 Robot - Sac Hoa Tri An
Runs integrity verification first, then regenerates all 3MF project packages.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import verify_plates
import generate_bambu_3mf

def run_sync():
    print("[1/2] Running Plate Integrity Audit...")
    verify_plates.main()
    print("\n[2/2] Generating / Updating Bambu Lab A1 3MF Files...")
    generate_bambu_3mf.main()
    print("\n>>> All Bambu Lab A1 3MF files are synced and ready!")

if __name__ == "__main__":
    run_sync()
