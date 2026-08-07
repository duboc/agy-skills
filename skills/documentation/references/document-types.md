# Document Type Templates

Use these structures to ensure comprehensive and consistent documentation.

## 1. README
The front page of your project. It must answer "What is this?" and "How do I use it quickly?"
- **Introduction:** What this is and why it exists (the problem it solves).
- **Quick Start:** The absolute shortest path (< 5 minutes) to getting the project running locally or executing a basic command.
- **Configuration:** Environment variables, flags, or config files required.
- **Usage:** Common commands or code examples.
- **Contributing:** How to run tests, build from source, and submit PRs.

## 2. API Documentation
The contract for consumers of your service.
- **Overview:** Base URL, authentication method, rate limits, and pagination strategy.
- **Endpoints:** For each endpoint provide:
  - Method and Path (e.g., `POST /v1/users`).
  - Description of what it does.
  - Request parameters/body with a realistic example (e.g., a cURL command).
  - Response payload with a realistic JSON example.
- **Errors:** A list of standard error codes and what they mean in this context.
- **SDK/Code Examples:** (Optional) Snippets in popular languages like Python, JS, or Go.

## 3. Runbook
The operational guide for handling specific tasks or incidents. Safety and clarity are paramount.
- **Context:** When to use this runbook (and when NOT to).
- **Prerequisites:** What access, tools, or approvals are needed before starting.
- **Procedure:** Step-by-step, unambiguous instructions. Include exact CLI commands to run.
- **Validation:** How to verify the procedure worked.
- **Rollback:** Exact steps to undo the changes if things go wrong.
- **Escalation Path:** Who to ping (Slack channel, on-call rotation) if this runbook fails.

## 4. Architecture Doc
The blueprint for how a system is built and why.
- **Context & Goals:** What the system does and the business requirements driving the design.
- **High-Level Design:** Described diagram or ASCII flow showing major components.
- **Data Flow & Integrations:** How data moves through the system and interacts with external services.
- **Key Decisions & Trade-offs:** The "Why" behind the architecture (e.g., "We chose DynamoDB over Postgres because of X, trading off Y").

## 5. Onboarding Guide
The roadmap for a new team member.
- **Welcome & Context:** High-level mission of the team.
- **Environment Setup:** Step-by-step guide to getting the local dev environment running (cloning repos, installing dependencies, seeding databases).
- **Architecture Overview:** High-level explanation of key systems and how they connect.
- **Common Tasks:** Walkthroughs for day-1 tasks (e.g., "How to run the test suite", "How to deploy to staging").
- **People & Pointers:** Who to ask for what, important Slack channels, and links to broader documentation.