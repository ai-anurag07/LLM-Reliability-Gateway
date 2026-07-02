import json
import requests
import sys

API_URL = "http://127.0.0.1:8000/v1/chat"
TEST_FILE = "ci_eval/eval_suite.json"

def run_tests():
    print("🚀 Starting LLM Gateway Regression Suite...\n")
    
    with open(TEST_FILE, "r") as f:
        tests = json.load(f)

    passed = 0
    failed = 0

    for idx, test in enumerate(tests):
        print(f"Test {idx + 1}: {test['prompt']}")
        
        try:
            # We add a dummy parameter to bypass cache for the test
            payload = {"prompt": test["prompt"] + " (test)"}
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            actual_text = data["response"]
            latency = data["latency_ms"]

            # Assertions
            if test["expected_contains"].lower() not in actual_text.lower():
                print(f"❌ FAILED: Expected '{test['expected_contains']}', got '{actual_text}'")
                failed += 1
                continue
                
            if latency > test["max_latency_ms"]:
                print(f"❌ FAILED: Latency {latency}ms exceeded max {test['max_latency_ms']}ms")
                failed += 1
                continue

            print(f"✅ PASSED (Latency: {latency}ms, Provider: {data['provider']})\n")
            passed += 1

        except Exception as e:
            print(f"❌ FAILED: API Error - {e}")
            failed += 1

    print("--------------------------------------------------")
    print(f"🏁 Regression Run Complete: {passed} Passed, {failed} Failed")
    
    if failed > 0:
        sys.exit(1) # Tells GitHub Actions to fail the build!
    sys.exit(0)

if __name__ == "__main__":
    run_tests()