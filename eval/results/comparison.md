# Run comparison

| metric | baseline | agent_v1 | agent_v1cot | agent_v2 | agent_v3 | agent_final | agent_engine_only | baseline_glm |
|---|---|---|---|---|---|---|---|---|
| decision_accuracy | 0.8125 | 0.9062 | 0.875 | 1.0 | 1.0 | 1.0 | 1.0 | 0.9688 |
| exact_match | 0.75 | 0.7812 | 0.6875 | 0.9375 | 1.0 | 1.0 | 1.0 | 0.9062 |
| discrepancy_f1 | 0.7895 | 0.8444 | 0.7727 | 0.9565 | 1.0 | 1.0 | 1.0 | 0.9091 |
| discrepancy_precision | 0.9375 | 0.8261 | 0.7727 | 0.9167 | 1.0 | 1.0 | 1.0 | 0.9091 |
| discrepancy_recall | 0.6818 | 0.8636 | 0.7727 | 1.0 | 1.0 | 1.0 | 1.0 | 0.9091 |
| false_hold_rate | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| missed_defect_rate | 0.3 | 0.15 | 0.2 | 0.0 | 0.0 | 0.0 | 0.0 | 0.05 |
| est_cost_usd_per_invoice | 0.0279 | 0.0092 | 0.0204 | 0.019 | 0.0196 | 0.02 | 0.0039 | 0.0427 |
| avg_latency_s | 4.43 | 8.12 | 14.14 | 13.68 | 13.57 | 15.05 | 3.51 | 18.82 |
