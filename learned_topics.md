# DACA Course: Structured Learning Summary

This document organizes your learning on DACA (Dapr Agentic Cloud Ascent) and related topics into a clear, hierarchical, and simple format.

---

## 1. Python Dependency Management (`UV`)

### 1.1 What is UV?

- A Rust-based tool for managing Python project files and dependencies.
- Converts dependency specs into fast, near-machine code for quick installs.

### 1.2 Key Benefits

1. **Speed & Parallel Downloads**: Written in Rust; can download many packages at once.
2. **Automatic Resolution**: Detects and fixes version conflicts.
3. **Easy Migration**: Switch from tools like Poetry or Conda smoothly.
4. **Locking**: Repeats exact versions each install, avoiding surprises.
5. **Global Efficiency**: Installs once globally; reuse across projects.

---

## 2. Agentic AI Design Patterns

### 2.1 Workflow System (Semi-Agentic)

- Defined steps: user interacts → LLM → tool calls.
- Follows a fixed path each time.

### 2.2 Fully Autonomous Agentic AI

- LLM decides when and how to call tools.
- Chooses its own steps dynamically.

---

## 3. Advanced Agentic Workflows

### 3.1 Augmented LLM

- Connect an LLM to tools, memory, or RAG.

### 3.2 Prompt Chaining

- Chain one LLM call to another based on the previous output.

### 3.3 Routing

- Direct tasks to different functions based on conditions.
- Use shared states (variables) across functions.

### 3.4 Parallelization

- **Sectioning**: Split a task into subtasks; run each in parallel; combine outputs.
- **Voting**: Run the same task in parallel; aggregate results by voting.

### 3.5 Orchestrator-Workers

- Central LLM breaks tasks into subtasks for worker LLMs; gathers final result.

### 3.6 Evaluator-Optimizer

- One LLM generates; another evaluates and gives feedback in a loop.

---

## 4. Context & Protocols for LLMs

### 4.1 Traditional Context Methods

1. Fine-tuning
2. Retrieval-Augmented Generation (RAG)
3. Tool calling
4. **MCP Servers** (Model Context Protocol)

### 4.2 Standard Protocols

- **MCP**: Standardizes tool calls.
- **Chat Completion API**: Basic LLM chat interface.
- **Responses API**: Alternative inference endpoint.

---

## 5. State Management: VMs vs Containers

- **VMs**: Keep state inside; long-lived.
- **Containers**: Stateless; reload state from a database when needed.
- **LLMs**: Always stateless; store any session data externally.

---

## 6. Agentia World & A2A

### 6.1 Legacy Pipeline

```
Client → API → Response
```

### 6.2 Agentic Pipeline

```
Client → Agent → API → Response
```

### 6.3 A2A Protocol (Agent-to-Agent)

- Human → Client Agent → Remote Agent

---

## 7. DACA Overview

### 7.1 Definition

DACA is a design pattern for building planet-scale AI agent systems using:

- Dapr sidecars (state, pub/sub, workflows)
- OpenAI Agents SDK
- MCP & A2A protocols
- Containers & Kubernetes

### 7.2 Layers

1. **Presentation**: Next.js, Chainlit, Streamlit
2. **Business Logic**: Python, FastAPI, SDKs, sidecars
3. **Infrastructure**: Dapr, Kubernetes, messaging, databases

---

## 8. Stateless Containers

1. **Event-Based**: Start on events; run; stop.
2. **Schedule-Based**: Run on a timer (cron).

---

## 9. Agent Delegation Patterns

- **Triage Agent**: Receives tasks, hands off to others.
- **Handoff Agent**: Completes subtasks, returns output.
- **Extended Response**: Triage agent also collects results and responds.

---

## 10. Agent Loop

1. Send: System prompt, user prompt, tool schema, tool message.
2. LLM decides: call tool or give final output.
3. If tool called: append result; repeat with updated messages.

---

## 11. Tool Calling in SDK

1. **Hosted Tools**: OpenAI built-in.
2. **Function Tools**: Use `@function_tool`.
3. **FastAPI**: Custom API endpoints as tools.

---

## 12. Streaming

- **Agent Loop Streaming**: Stream intermediate tool results.
- **LLM Streaming**: Stream LLM token generation.

---

## 13. Context & Memory Management

- **Local Context**: Store sensitive data locally; load on demand.
- **LLM Context**: Send needed info directly to LLM via system/user messages or tools.

---

## 14. Kubernetes & Dapr

- **Kubernetes**: Node → Pod → Containers (app + Dapr sidecar).
- **Dapr**: Makes containers stateful; handles retries and messaging.

---

## 15. AI Agents for Microsaas Founders

- Use micro-agents to automate small SaaS tasks.
- Scale with DACA pattern for cost efficiency.
