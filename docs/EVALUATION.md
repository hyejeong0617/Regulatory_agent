# Evaluation record

Frozen case: Türkiye-origin dried figs and aflatoxin B1, with concentration and shipment stage unspecified. Benchmark: Q1–Q10. Evaluation dimensions are Correct / Grounded / Complete, each Yes / Partial / No. **Yes-only** counts:

| Build | Correct | Grounded | Complete |
| --- | ---: | ---: | ---: |
| Prompt-only | 5 | 0 | 2 |
| Static RAG | 5 | 9 | 2 |
| Tools | 9 | 6 | 4 |
| Investigation v3 | 8 | 10 | 3 |

Baseline scores were independently reviewed by the project owner against a frozen [Verified Reference](https://app.notion.com/p/3fa695ed0f62819d96b6ee13706bdb3b). Do not interpret the numbers as independent regulatory cases or percentages of market accuracy.

Build04 v3 ran Q1–Q10 with 527,148 tokens, 69 LLM calls, 64 searches, and 2,232.93 s recorded. The Q5/Q9/Q10 pilot results for v4 Lean and Adaptive are in the historical `data/` and should not be substituted into final Build04 metrics.

The independently Codex-built Agent belongs in a separate repository and comparison note. It is not a fifth human-guided notebook build.
