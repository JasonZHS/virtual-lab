import subprocess
import sys
import os

def run_command(command, description):
    print(f"\n[EXEC] {description}...")
    try:
        # Run command and wait for it to complete. 
        # check=True raises CalledProcessError if return code is non-zero
        subprocess.run(command, shell=True, check=True, text=True)
        print(f"[✓] {description} Passed.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[X] {description} FAILED. Return Code: {e.returncode}")
        return False

def verify_system():
    print("=== AlzKB System Verification Suite ===")
    
    steps = [
        ("python alzkb/tests/verify_phase_1.py", "Phase I: Ontology & Scoring"),
        ("python alzkb/tests/verify_phase_2.py", "Phase II: Ingestion & Quarantine"),
        ("python alzkb/tests/verify_phase_3.py", "Phase III: Biology & Resolution"),
        ("python alzkb/tests/verify_phase_4.py", "Phase IV: RAG Architecture"),
        ("python alzkb/tests/verify_phase_5.py", "Phase V: UI Logic & Pruning")
    ]
    
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            print("\nCRITICAL: System Verification Failed. Aborting Launch.")
            sys.exit(1)
            
    print("\n=== All Systems Verified Successfully ===")

def launch_app():
    print("\n[LAUNCH] Starting AlzKB Discovery Dashboard...")
    print("Press Ctrl+C to stop the server.")
    
    # We use running from the current python executable to ensure environment consistency
    # But streamlit is a binary, so we call it directly assuming it's in path
    cmd = "streamlit run alzkb/src/alzkb/ui/app.py"
    
    try:
        subprocess.run(cmd, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n[STOP] Server stopped by user.")

if __name__ == "__main__":
    # Ensure raw output is flushed immediately
    sys.stdout.reconfigure(line_buffering=True)
    
    # 1. Run Verification
    verify_system()
    
    # 2. Launch UI
    launch_app()
