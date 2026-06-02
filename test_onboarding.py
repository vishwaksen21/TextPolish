import sys
import argparse
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from settings import Settings
from main import AvelynApp

def test_onboarding_flow():
    # 1. Simulate fresh install by clearing settings
    settings = Settings()
    settings._config["first_run_completed"] = False
    settings.save()
    
    app = AvelynApp(argparse.Namespace())
    
    # 2. Setup a timer to simulate user interaction
    def simulate_user():
        onboarding = app._onboarding
        if not onboarding:
            print("❌ Onboarding window not found!")
            QApplication.quit()
            return
            
        print(f"\n[Test] Onboarding launched. Current step: {onboarding.step_label.text()}")
        
        # Step 1 -> 2
        print("[Test] Clicking Next (Welcome -> Accessibility)")
        onboarding.btn_next.click()
        print(f"[Test] Current step: {onboarding.step_label.text()}")
        
        # Simulate granting accessibility
        from permissions import PermissionManager
        PermissionManager.check_accessibility = lambda: True
        onboarding._poll_status()
        
        # Step 2 -> 3
        print("[Test] Clicking Next (Accessibility -> Input Monitoring)")
        onboarding.btn_next.click()
        print(f"[Test] Current step: {onboarding.step_label.text()}")
        
        # Step 3 -> 4
        print("[Test] Clicking Next (Input Monitoring -> Ollama Check)")
        onboarding.btn_next.click()
        print(f"[Test] Current step: {onboarding.step_label.text()}")
        
        # Skip actual installation for test, just mark as done
        onboarding._on_ol_done()
        
        # Step 4 -> 5
        print("[Test] Clicking Next (Ollama Check -> Model Check)")
        onboarding.btn_next.click()
        print(f"[Test] Current step: {onboarding.step_label.text()}")
        
        # Skip actual download for test
        onboarding._on_mod_done()
        
        # Step 5 -> 6
        print("[Test] Clicking Next (Model Check -> Complete)")
        onboarding.btn_next.click()
        print(f"[Test] Current step: {onboarding.step_label.text()}")
        
        # Finish
        print("[Test] Clicking Finish")
        onboarding.btn_next.click()
        
        # Verify startup resumed
        print(f"[Test] Onboarding instance exists? {app._onboarding is not None}")
        print(f"[Test] Settings first_run_completed: {app._settings.get('first_run_completed')}")
        
        QApplication.quit()
        
    QTimer.singleShot(500, simulate_user)
    app.run()

if __name__ == "__main__":
    print("=== Starting Onboarding Verification Test ===")
    test_onboarding_flow()
    print("=== Test Complete ===")
