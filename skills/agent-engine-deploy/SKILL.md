---
name: agent-engine-deploy
description: Deploy, update, query and manage Google ADK agents on Vertex AI Agent Engine. Use for runtime packaging, exact deployed-resource lifecycle, A2A deployment, streaming and scaling configuration; not local-only agent development.
---

# Agent Engine deployment

## Establish the runtime contract

Read the project dependency lockfile and installed `google-adk` and
`google-cloud-aiplatform` versions. Consult the matching official SDK/API docs
before constructing create, update or query calls. Legacy `vertexai.agent_engines`
and client-based APIs may use different parameter/config structures; do not mix
them. Snippets in supporting references describe patterns and must be reconciled
with the installed version before execution.

Identify project, location, authenticated deployer, runtime identity, artifact
source and requested target. Use the existing resource's full name for updates;
a display name is not a unique resource identifier. Preserve the user's chosen
environment. Model IDs, package extras, supported locations and scaling fields
are version-dependent and need current verification.

Start from the [official runtime documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview).
If a link redirects to a product landing page, navigate to the specific current
guide; a successful HTTP response is not proof that an API example is current.

## Prepare a reviewable deployment

1. Run the local agent's relevant tests and a representative request.
2. Build a reproducible dependency set and package only required code/assets.
3. Confirm runtime identity permissions at the smallest required resource scope.
   Separate deployer permission, service-agent permission and tool access.
4. Prepare explicit environment configuration with secret references. Do not print
   credentials or embed user data in build artifacts.
5. Record the existing resource/configuration and rollback artifact before update.
   Identify incompatible session/state changes that code rollback cannot undo.
6. Execute the requested create/update against the exact target. Await operation
   completion and read the deployed resource back before reporting success.

Use [deployment patterns](references/deployment-patterns.md) for packaging and
staging concerns. A staging bucket holds artifacts; it is not a staging runtime.
Authorization to produce scripts is not authorization to deploy them. Reuse
deployment authorization already provided instead of asking again.

## Verify the deployed behavior

Use the query methods exposed by the deployed application and current SDK.
Do not assume every wrapper has both `query` and `async_stream_query`, that
events are objects rather than dictionaries, or that `session_id=None` creates
a session. Create/retrieve a session through the supported contract when needed.

Check a representative response, tool call, error case and session isolation.
Read deployment/resource status and inspect logs without exposing request data.
Report resource identity, artifact/version, checks run and unresolved limits.
Local tests and operation submission alone are not a deployment smoke test.

## Streaming and A2A

One submitted message followed by many response events is server streaming.
True bidirectional streaming requires supported concurrent input/output and
connection lifecycle APIs; it is not enabled by renaming an async query loop.
Verify interruption, cancellation and disconnect cleanup in the real transport.

For A2A, read [A2A patterns](references/a2a-agent-engine.md), validate the installed
protocol/SDK types, AgentCard schema, endpoint and authentication. Do not assume
a wrapper class or generated card exists in every SDK version.

## Scaling and lifecycle

Read [performance and scaling](references/performance-scaling.md) only when
relevant. Set measured latency/concurrency goals, verify supported replica and
container fields, and read them back after deployment. Minimum replicas can
reduce cold starts at a cost; maximum replicas do not cap all model/tool charges.

Before deletion, resolve the exact resource and affected sessions/dependencies.
Operate within the requested deletion scope; never select a target by a partial
display-name match or clean up unrelated agents.
