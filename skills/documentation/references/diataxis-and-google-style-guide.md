# Diátaxis Documentation Architecture & Google Developer Style Guide

Use this reference to structure documentation repositories using the 4-quadrant **Diátaxis Framework** and enforce the **Google Developer Documentation Style Guide**.

---

## 1. The Diátaxis 4-Quadrant Matrix

Never mix all four modes in a single document. Choose the primary quadrant based on the reader's state:

| Quadrant | User Intent | Orientation | Must Include | Must Avoid |
|----------|-------------|-------------|--------------|------------|
| **1. Tutorials** (`Getting Started`) | Learning by doing (Acquiring skill) | **Action + Guided Study** | Deterministic end-to-end steps, immediate visible success within 5 minutes | Deep architectural theory, optional branches, edge-case configurations |
| **2. How-To Guides** (`Recipes`) | Solving a specific task (Applying skill) | **Action + Goal** | Exact prerequisites, numbered task steps, copy-pasteable commands, verification check | Teaching basic concepts from scratch |
| **3. Reference** (`API / CLI Spec`) | Looking up exact facts (Applying knowledge) | **Information + Accuracy** | Parameter tables (Name, Type, Default, Constraints), status codes, deterministic return schemas | Conversational prose, opinionated tutorials |
| **4. Explanation** (`Architecture / ADRs`) | Understanding *why* (Acquiring knowledge) | **Understanding + Context** | Trade-offs, sequence diagrams, alternatives rejected, design rationale | Step-by-step installation instructions |

---

## 2. Google Developer Documentation Style Rules

1. **Voice & Tense**:
   - Use **second person** (`"You configure the service..."`) rather than `"we"` or `"the user"`.
   - Use **active voice** and **present tense** (`"The API returns a 201 status code"`, not `"A 201 status code will be returned by the API"`).
2. **Task-Oriented Headings**:
   - Start procedural headings with imperative verbs (`"Configure OAuth credentials"`, `"Verify the webhook signature"`).
3. **Code Sample Hygiene**:
   - Every code snippet must be **complete, runnable, and safe** (`shell=False`, `set -euo pipefail`).
   - Use RFC 2606 placeholders (`example.com`, `user@example.com`, `<YOUR_PROJECT_ID>`) and never embed real tokens or `/Users/<name>` paths.
4. **Callout Discipline**:
   - Limit `Note:`, `Warning:`, and `Caution:` callouts to at most 1 per section so critical security warnings stand out.
