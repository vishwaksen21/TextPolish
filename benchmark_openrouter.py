#!/usr/bin/env python3
"""
OpenRouter Model Benchmark for Avelyn
Tests TTFT and total response time across multiple models.
"""

import json
import time
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from providers import OpenRouterProvider
from settings import Settings


# Models to benchmark
MODELS = [
    ("google/gemini-2.5-flash", "Gemini 2.5 Flash"),
    ("openai/gpt-4o-mini", "GPT-4o Mini"),
    ("anthropic/claude-3.5-haiku", "Claude 3.5 Haiku"),
    ("google/gemma-3-27b-it:free", "Gemma 3 27B (Free)"),
    ("z-ai/glm-4.5", "GLM 4.5 (Current)"),
    ("deepseek/deepseek-chat-v3-0324:free", "DeepSeek V3 (Free)"),
]

# Test prompts representative of Avelyn's workload
TEST_PROMPTS = [
    {
        "name": "Short Grammar Fix",
        "text": "Fix the grammar in this sentence: 'He dont know nothing about it.'",
        "mode": "grammar",
    },
    {
        "name": "Professional Rewrite",
        "text": "make this email more professional: hey john, can u send me the files by tomorrow? thx",
        "mode": "professional",
    },
    {
        "name": "Code Explanation",
        "text": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
        "mode": "explain_code",
    },
    {
        "name": "LinkedIn Post",
        "text": "I just got promoted to Senior Engineer! After 3 years of hard work, leading projects and mentoring juniors, it finally paid off.",
        "mode": "linkedin",
    },
]


def build_prompt(text: str, mode: str) -> str:
    """Build the exact prompt Avelyn would send."""
    from ai_processor import SYSTEM_PROMPT, MODE_PROMPTS, _build_prompt
    
    # Use the actual _build_prompt function
    return _build_prompt(text, mode)


def benchmark_model(api_key: str, model_id: str, model_name: str) -> dict:
    """Run benchmarks for a single model."""
    print(f"\n{'='*60}")
    print(f"Benchmarking: {model_name} ({model_id})")
    print(f"{'='*60}")
    
    provider = OpenRouterProvider(api_key=api_key, model=model_id)
    results = []
    
    for test in TEST_PROMPTS:
        prompt = build_prompt(test["text"], test["mode"])
        prompt_tokens = len(prompt) // 4
        
        print(f"\n  Test: {test['name']} ({test['mode']})")
        print(f"  Prompt tokens: ~{prompt_tokens}")
        
        # Run 3 times and take median
        times = []
        for run in range(3):
            try:
                ttft = None
                first_token_time = None
                total_time = None
                token_count = 0
                full_response = []
                
                start = time.perf_counter()
                
                for chunk in provider.generate(
                    prompt=prompt,
                    system_prompt="You are Avelyn. Output ONLY the finalized transformed text. No explanations, no introductions, no markdown, and preserve user intent.",
                    mode=test["mode"],
                ):
                    current = time.perf_counter()
                    if first_token_time is None:
                        first_token_time = current
                        ttft = (first_token_time - start) * 1000
                    
                    token_count += 1
                    full_response.append(chunk)
                
                total_time = (time.perf_counter() - start) * 1000
                
                # Only count if we got a reasonable response
                if token_count > 0:
                    times.append({
                        "ttft": ttft,
                        "total_time": total_time,
                        "tokens": token_count,
                        "tps": token_count / (total_time / 1000) if total_time > 0 else 0,
                        "response_len": len("".join(full_response)),
                    })
                    print(f"    Run {run+1}: TTFT={ttft:.0f}ms, Total={total_time:.0f}ms, TPS={token_count/(total_time/1000):.1f}")
                else:
                    print(f"    Run {run+1}: FAILED (no tokens)")
                    
            except Exception as e:
                print(f"    Run {run+1}: ERROR - {e}")
        
        if times:
            # Sort by TTFT and take median
            times.sort(key=lambda x: x["ttft"])
            median = times[len(times)//2]
            results.append({
                "test": test["name"],
                "mode": test["mode"],
                "prompt_tokens": prompt_tokens,
                "ttft_ms": median["ttft"],
                "total_ms": median["total_time"],
                "tokens": median["tokens"],
                "tps": median["tps"],
                "runs": len(times),
            })
            print(f"  → Median: TTFT={median['ttft']:.0f}ms, Total={median['total_time']:.0f}ms, TPS={median['tps']:.1f}")
        else:
            print(f"  → ALL RUNS FAILED")
            results.append({
                "test": test["name"],
                "mode": test["mode"],
                "prompt_tokens": prompt_tokens,
                "ttft_ms": None,
                "total_ms": None,
                "tokens": 0,
                "tps": 0,
                "runs": 0,
            })
    
    return {
        "model_id": model_id,
        "model_name": model_name,
        "results": results,
    }


def print_summary_table(all_results: list):
    """Print a formatted benchmark table."""
    print("\n" + "=" * 100)
    print("BENCHMARK SUMMARY TABLE")
    print("=" * 100)
    
    # Header
    print(f"{'Model':<30} | {'Test':<20} | {'Prompt Tok':>10} | {'TTFT (ms)':>10} | {'Total (ms)':>10} | {'TPS':>8}")
    print("-" * 100)
    
    for model_result in all_results:
        model_name = model_result["model_name"]
        model_id = model_result["model_id"]
        
        for i, r in enumerate(model_result["results"]):
            if i == 0:
                model_display = f"{model_name} ({model_id})"
            else:
                model_display = ""
            
            ttft = f"{r['ttft_ms']:.0f}" if r['ttft_ms'] else "FAILED"
            total = f"{r['total_ms']:.0f}" if r['total_ms'] else "FAILED"
            tps = f"{r['tps']:.1f}" if r['tps'] else "N/A"
            
            print(f"{model_display:<30} | {r['test']:<20} | {r['prompt_tokens']:>10} | {ttft:>10} | {total:>10} | {tps:>8}")
    
    print("-" * 100)
    
    # Overall ranking by average TTFT
    print("\nOVERALL RANKING (by median TTFT across all tests):")
    print("-" * 60)
    
    model_avgs = []
    for mr in all_results:
        valid_ttfts = [r["ttft_ms"] for r in mr["results"] if r["ttft_ms"]]
        if valid_ttfts:
            avg_ttft = sum(valid_ttfts) / len(valid_ttfts)
            model_avgs.append((mr["model_name"], mr["model_id"], avg_ttft, len(valid_ttfts)))
    
    model_avgs.sort(key=lambda x: x[2])
    
    for i, (name, model_id, avg_ttft, count) in enumerate(model_avgs, 1):
        print(f"  {i}. {name} ({model_id}): {avg_ttft:.0f}ms avg TTFT ({count} tests)")


def main():
    settings = Settings()
    api_key = settings.avelyn_cloud_api_key
    
    if not api_key:
        print("ERROR: No OpenRouter API key configured in settings.")
        print("Add your key in Settings → AI Provider → Avelyn Cloud.")
        return
    
    print(f"Using API key: {api_key[:4]}****{api_key[-4:] if len(api_key) > 8 else ''}")
    print(f"Testing {len(MODELS)} models with {len(TEST_PROMPTS)} test cases each (3 runs per test)")
    
    all_results = []
    
    for model_id, model_name in MODELS:
        try:
            result = benchmark_model(api_key, model_id, model_name)
            all_results.append(result)
        except Exception as e:
            print(f"\n  ERROR benchmarking {model_name}: {e}")
            all_results.append({
                "model_id": model_id,
                "model_name": model_name,
                "results": [],
                "error": str(e),
            })
    
    print_summary_table(all_results)
    
    # Save results to JSON
    output_file = Path.home() / ".avelyn" / "benchmark_results.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()