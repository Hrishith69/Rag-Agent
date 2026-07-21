import json
import time
from agent import build_triage_agent
from dotenv import load_dotenv
load_dotenv()

# Initialize the agent executor once at the top of eval.py
agent_executor = build_triage_agent()

DATASET_FILE = "eval_dataset.json"
RESULTS_FILE = "eval_results.json"

def run_benchmark():
    print("🚀 Starting Agent Evaluation Benchmark...\n")
    
    with open(DATASET_FILE, "r") as f:
        dataset = json.load(f)

    results = []
    correct_routes = 0
    total_latency = 0.0

    print(f"{'ID':<4} | {'Category':<15} | {'Expected Tool':<20} | {'Actual Tool':<20} | {'Status':<6} | {'Time (s)':<8}")
    print("-" * 82)

    for item in dataset:
        item_id = item["id"]
        question = item["question"]
        expected_route = item["expected_route"]
        category = item["category"]

        start_time = time.time()
        
        # Execute agent
        try:
            response = agent_executor.invoke({"input": question})
            elapsed = round(time.time() - start_time, 2)
            total_latency += elapsed

            # Extract which tool was called from intermediate steps
            intermediate_steps = response.get("intermediate_steps", [])
            if intermediate_steps:
                actual_route = intermediate_steps[0][0].tool
            else:
                actual_route = "direct_answer"

            # Check if routing was correct
            is_correct = (actual_route == expected_route)
            if is_correct:
                correct_routes += 1

            status = "PASS" if is_correct else "FAIL"

            print(f"{item_id:<4} | {category:<15} | {expected_route:<20} | {actual_route:<20} | {status:<6} | {elapsed:<8}")

            results.append({
                "id": item_id,
                "question": question,
                "category": category,
                "expected_route": expected_route,
                "actual_route": actual_route,
                "passed": is_correct,
                "latency_seconds": elapsed,
                "answer": response.get("output", "")
            })

        except Exception as e:
            print(f"{item_id:<4} | {category:<15} | {expected_route:<20} | ERROR: {str(e)[:15]:<20} | FAIL   | 0.00")

    # Compute Final Summary Metrics
    total_tests = len(dataset)
    accuracy = round((correct_routes / total_tests) * 100, 2) if total_tests > 0 else 0
    avg_latency = round(total_latency / total_tests, 2) if total_tests > 0 else 0

    print("-" * 82)
    print(f"\n📊 BENCHMARK SUMMARY:")
    print(f" Total Test Cases : {total_tests}")
    print(f" Passed           : {correct_routes}")
    print(f" Failed           : {total_tests - correct_routes}")
    print(f" Routing Accuracy : {accuracy}%")
    print(f" Avg Latency      : {avg_latency} seconds")

    # Save results to JSON
    summary_data = {
        "metrics": {
            "total_tests": total_tests,
            "passed": correct_routes,
            "failed": total_tests - correct_routes,
            "accuracy_percent": accuracy,
            "avg_latency_seconds": avg_latency
        },
        "details": results
    }

    with open(RESULTS_FILE, "w") as f:
        json.dump(summary_data, f, indent=2)

    print(f"\n💾 Results saved to '{RESULTS_FILE}'.")

if __name__ == "__main__":
    run_benchmark()