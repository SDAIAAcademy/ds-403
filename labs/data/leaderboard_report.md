# Watad configuration leaderboard, October 2026

Prepared by Khattab Al-Ruhaili, evaluation lead, Bunyan Building Permits Authority. Synthetic document for the DS-403 course.

All four configurations answered the 600 questions of the regulation task set at temperature 0.2, five samples per question, graded by the model grader.

| Rank | Configuration | Description | Pass rate |
|---|---|---|---|
| 1 | D | mid-size open-weight model, retrieved regulation in the prompt | 86.7% |
| 2 | C | mid-size open-weight model, plain prompt | 70.8% |
| 3 | B | small open-weight model, retrieved regulation in the prompt | 69.3% |
| 4 | A | small open-weight model, plain prompt | 62.7% |

Safety set (40 questions, greedy decoding): A 36/40, B 38/40, C 39/40, D 40/40.

The claims of this report are listed one per line in leaderboard_claims.csv.
