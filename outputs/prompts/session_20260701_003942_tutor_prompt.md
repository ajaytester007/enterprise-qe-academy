# ChatGPT Tutor Prompt

Act as my Enterprise Quality Engineering interview coach.

Use the practice session below. For each question:
1. Ask me to answer first.
2. Do not reveal the answer immediately.
3. Provide Hint 1 only if I ask for a clue.
4. Provide Hint 2 if I am still stuck.
5. Reveal the model answer only when I ask.
6. Score my answer out of 100 using the embedded rubric.
7. Ask follow-up interview questions.
8. Give improvement notes.

Start with Question 1 only.

---

# Tutor Practice Session: session_20260701_003942

## How to Practice

1. Answer first without opening hints.
2. Open Hint 1 only if stuck.
3. Open Hint 2 if still stuck.
4. Reveal the model answer.
5. Score yourself and write improvement notes.

## 1. SEC-03867 — PII for Banking data governance program

- Difficulty: Hard
- Category: SECURITY_PRIVACY
- Concept: PII
- Domain: Banking
- Role: Lead Quality Engineer

**Problem:** Design, implement, test, or whiteboard a hard solution involving PII for Banking data governance program. Explain assumptions, edge cases, validation strategy, quality risks, evidence expected, complexity, and production-readiness considerations.

### Your Answer Notes

- 

<details><summary>Hint 1</summary>

Clarify the scope, business grain, inputs, outputs, and risk for PII in Banking.

</details>

<details><summary>Hint 2</summary>

Structure the answer using approach, edge cases, validation strategy, evidence, CI/CD readiness, and follow-up risks.

</details>

<details><summary>Model Answer</summary>

Use the Enterprise QE answer framework: clarify scope, propose approach, define test strategy, cover edge cases, describe evidence, and explain production readiness.

</details>

### Follow-up Questions

- How would you automate this?
- How would you prove readiness?
- What risks remain?

### Scorecard

| Dimension | Score | Notes |
|---|---:|---|
| Problem understanding | ___ / 15 | |
| Technical approach | ___ / 20 | |
| Edge cases and risks | ___ / 15 | |
| Testing strategy | ___ / 20 | |
| Evidence and observability | ___ / 10 | |
| Communication | ___ / 20 | |

**Total:** ___ / 100

### Improvement Notes

- 

## 2. PER-07556 — SLA validation for Banking API-first transformation

- Difficulty: Hard
- Category: PERFORMANCE_RELIABILITY
- Concept: SLA validation
- Domain: Banking
- Role: Lead Quality Engineer

**Problem:** Design, implement, test, or whiteboard a hard solution involving SLA validation for Banking API-first transformation. Explain assumptions, edge cases, validation strategy, quality risks, evidence expected, complexity, and production-readiness considerations.

### Your Answer Notes

- 

<details><summary>Hint 1</summary>

Clarify the scope, business grain, inputs, outputs, and risk for SLA validation in Banking.

</details>

<details><summary>Hint 2</summary>

Structure the answer using approach, edge cases, validation strategy, evidence, CI/CD readiness, and follow-up risks.

</details>

<details><summary>Model Answer</summary>

A strong SLA validation answer defines the SLA/SLO first: latency, throughput, error rate, availability, and recovery behavior. For API-first banking transformation, I would test peak load, sustained load, spike load, failover, retries, throttling, and downstream dependency behavior.

Evidence includes response-time percentiles, throughput, error rates, saturation metrics, logs, traces, and capacity recommendations. I would validate p95/p99 latency and ensure business-critical workflows stay within agreed thresholds.

</details>

### Follow-up Questions

- Which metric matters most?
- How do you test failover?
- How do you identify bottlenecks?
- How do you define pass/fail?

### Scorecard

| Dimension | Score | Notes |
|---|---:|---|
| Problem understanding | ___ / 15 | |
| Technical approach | ___ / 20 | |
| Edge cases and risks | ___ / 15 | |
| Testing strategy | ___ / 20 | |
| Evidence and observability | ___ / 10 | |
| Communication | ___ / 20 | |

**Total:** ___ / 100

### Improvement Notes

- 

## 3. JAV-09254 — Normalization for Banking CI/CD quality gate adoption

- Difficulty: Hard
- Category: JAVA_STRINGS
- Concept: Normalization
- Domain: Banking
- Role: Lead Quality Engineer

**Problem:** Design, implement, test, or whiteboard a hard solution involving Normalization for Banking CI/CD quality gate adoption. Explain assumptions, edge cases, validation strategy, quality risks, evidence expected, complexity, and production-readiness considerations.

### Your Answer Notes

- 

<details><summary>Hint 1</summary>

Clarify the scope, business grain, inputs, outputs, and risk for Normalization in Banking.

</details>

<details><summary>Hint 2</summary>

Structure the answer using approach, edge cases, validation strategy, evidence, CI/CD readiness, and follow-up risks.

</details>

<details><summary>Model Answer</summary>

A strong Java string answer clarifies case sensitivity, whitespace, punctuation, null handling, and expected output. For regex validation, I define the exact business rule first, then create positive and negative tests around boundary conditions.

For example, email or identifier validation should avoid overly broad regexes and should be backed by test cases:
```java
private static final Pattern ACCOUNT_ID = Pattern.compile("^[A-Z]{3}-\\d{6}$");

public static boolean isValidAccountId(String value) {
    return value != null && ACCOUNT_ID.matcher(value).matches();
}
```

Testing should include null, empty, malformed, valid, lowercase, extra spaces, special characters, and length boundaries. Complexity is usually O(n) where n is string length.

</details>

### Follow-up Questions

- When is regex the wrong tool?
- How do you prevent catastrophic backtracking?
- How would you test international characters?
- How do you keep validation rules maintainable?

### Scorecard

| Dimension | Score | Notes |
|---|---:|---|
| Problem understanding | ___ / 15 | |
| Technical approach | ___ / 20 | |
| Edge cases and risks | ___ / 15 | |
| Testing strategy | ___ / 20 | |
| Evidence and observability | ___ / 10 | |
| Communication | ___ / 20 | |

**Total:** ___ / 100

### Improvement Notes

-
