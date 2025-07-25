# Cheat Sheet: OpenAI Agents SDK & Related Topics

This simplified Markdown guide explains each topic in your syllabus in a clear, logical order—no code, just concise definitions and benefits.

---

## 1. Swarm (Legacy Multi-Agent Framework)

- **What:** An experimental OpenAI framework for orchestrating multiple AI agents.
- **Core Ideas:**

  - **Agents:** Independent units with specific instructions and tools.
  - **Handoffs:** Mechanism for transferring control and context between agents.

- **Why It Matters:**

  - Demonstrated how to coordinate specialized agents (e.g., billing vs. support) in a lightweight, testable way.
  - Served as the foundation for the production-ready Agents SDK.

- **Key Takeaway:** Swarm introduced “Agents” and “Handoffs” as core abstractions; modern Agent SDK builds on these principles.

---

## 2. UV Package Manager

- **What:** A modern Python package manager written in Rust.
- **Why Use UV over Traditional Tools:**

  - **Speed & Parallelism:** Downloads and installs many packages at once, much faster than pip/Poetry/Conda.
  - **Automatic Conflict Resolution:** Handles different versions and compatibility automatically.
  - **Easy Migration:** Can adopt UV from Poetry, Conda, etc., without major changes.
  - **Locking:** Ensures reproducible installs by fixing exact versions.
  - **Global Efficiency:** Installs dependencies in a shared global store; multiple projects reuse the same packages.

- **Key Takeaway:** UV streamlines environment setup and dependency management—ideal for fast iteration in AI projects.

---

## 3. OpenRouter

- **What:** A unified API platform that lets you access over 200 large language models (LLMs) from multiple providers.
- **How It Works:**

  - Acts as a proxy: routes your API call to the best model based on price, latency, and uptime.
  - Compatible with OpenAI Chat Completion API format—swap a few settings to switch providers.

- **Why It Matters:**

  - **One Endpoint, Many Models:** Call commercial (OpenAI, Anthropic) and open-source (Mistral, LLaMA) LLMs without changing your code.
  - **Cost & Performance Optimization:** Automatically picks the cheapest or fastest provider.
  - **Function-Calling Support:** Lets agents suggest function/tool use in a standardized way across models.

- **Key Takeaway:** OpenRouter simplifies multi-model development, so you can experiment with different LLMs seamlessly.

---

## 4. LiteLLM

- **What:** A Python library that provides a unified interface to dozens of local and hosted LLMs (100+ supported).
- **Why It Matters:**

  - Allows you to run or call models from different vendors (OpenAI, Anthropic, local LLaMA, Mistral, etc.) in the same codebase.
  - Provides consistent methods for chat, completions, and function calling.

- **Benefits:**

  - **Vendor Flexibility:** Easily switch between hosted APIs and local models.
  - **Cost Control:** Run smaller, open-source models locally when budget or privacy is a concern.
  - **Future-Proof:** As new models emerge, LiteLLM often adds support quickly.

- **Key Takeaway:** LiteLLM gives you “one API to rule them all” for large language models.

---

## 5. Introduction to OpenAI Agents SDK

- **What:** A Python-first framework for building AI agents with:

  - **Agents:** LLMs configured with instructions and optional tools.
  - **Tools:** Actions (web search, database fetch, function calls) that agents can invoke.
  - **Handoffs:** Delegation mechanism to route tasks between agents.
  - **Guardrails & Tracing:** Built-in safety checks and execution logs.

- **Why It Matters:**

  - Simplifies multi-step, tool-augmented AI workflows.
  - Handles the “agent loop” (LLM calls → tool calls → repeat) automatically.
  - Lightweight and production-ready (unlike the older Swarm).

- **Key Takeaway:** Agents SDK is your go-to for orchestrating complex AI assistants without reinventing wheels.

---

## 6. Chainlit (UI Framework)

- **What:** An open-source Python library for building web-based chat interfaces for LLM and agent applications.
- **Why Use Chainlit:**

  - **Instant Chat UI:** Quickly create a browser-based chat page to interact with your agents.
  - **Event Visualization:** Shows each LLM call, tool invocation, and intermediate steps in real time.
  - **Minimal Setup:** Install via pip and add a few functions; Chainlit handles the rest (routing, authentication, UI).

- **Key Takeaway:** Use Chainlit to prototype and demonstrate your agent workflows in a user-friendly web interface.

---

## 7. Streaming Responses & Agent SDK

- **What:** Streaming lets you receive incremental updates while an agent is generating a response.
- **How It Works:**

  - Instead of waiting for a full reply, you subscribe to _stream events_ (token-by-token or higher-level items).
  - **Raw Events:** Individual tokens or model events (e.g., `response.output_text.delta`).
  - **Item Events:** Higher abstractions like “tool called,” “tool output returned,” or “message chunk completed.”

- **Why It Matters:**

  - **Real-Time Feedback:** Users see progress as it happens (important for long answers).
  - **Progress Indicators:** You can display “tool X ran” or “agent switched” messages in your UI.

- **Key Takeaway:** Streaming APIs improve user experience by showing partial responses and intermediate steps.

---

## 8. Tools in OpenAI Agents SDK

- **What:** Actions or utilities that an agent can invoke during its run:

  1. **Hosted Tools:** Prebuilt by OpenAI (e.g., web search, file search, code interpreter, image generation, computer control, local shell).
  2. **Function Tools:** Any Python function turned into a tool by adding a decorator—SDK auto-generates JSON schemas and extracts docstrings.
  3. **Agents-as-Tools:** One agent used as a tool inside another, enabling nested or orchestrated workflows.

- **Why It Matters:**

  - **Flexibility:** Agents can fetch data, run code, or call external services seamlessly.
  - **Extensibility:** Add custom logic without changing core agent code (just write a function).
  - **Modularity:** Reuse specialized agents as tools in larger systems.

- **Key Takeaway:** Tools expand an agent’s capabilities beyond pure text generation.

---

## 9. Agents as Tools (Advanced Orchestration)

- **What:** A pattern where one agent calls another agent as if it were a tool (instead of a handoff).
- **Why Use It:**

  - **Inline Delegation:** Orchestrator agent can invoke a sub-agent’s functionality without formally transferring entire conversation context.
  - **Composable Workflows:** Build a “master” agent that calls specialized agents in sequence or parallel.

- **Key Takeaway:** Agents-as-tools enable flexible, layered orchestration when you need one agent to request another’s service directly.

---

## 10. Handoffs (Agent Delegation)

- **What:** A built-in mechanism to transfer conversation control from one agent to another during a run.
- **How It Works:**

  - When an agent’s LLM output triggers a handoff tool, the Runner switches the “current agent” to the specified sub-agent, preserving context.
  - You declare handoffs when creating an agent:

    - Pass other agent objects or use `handoff()` wrappers if you need custom names/descriptions or input schemas.

- **Why It Matters:**

  - **Task Routing:** Automatically send specialized queries (e.g., billing, support, FAQ) to the right expert agent.
  - **Modularity:** Each agent focuses on one domain; the triage agent delegates accordingly.

- **Key Takeaway:** Handoffs keep conversations seamless while leveraging multiple specialized agents.

---

## 11. Structured Output with Pydantic

- **What:** Pydantic models let you define clear, typed schemas for agent outputs or handoff inputs.
- **How It Works:**

  - Set an agent’s `output_type` to a Pydantic `BaseModel`. The agent is prompted to return JSON matching that schema.
  - On handoff, you can specify an `input_type` model so the LLM provides structured data for the next agent.

- **Why It Matters:**

  - **Type Safety:** Ensures the agent’s output conforms to expected fields (e.g., `name: str`, `age: int`).
  - **Automatic Validation:** If the model diverges from JSON structure, the SDK raises an error.
  - **Consistent Data:** Downstream code can rely on parsed objects rather than raw text.

- **Key Takeaway:** Pydantic enforces well-formed, machine-readable outputs and inputs.

---

## 12. Guardrails (Input/Output Checks)

- **What:** User-defined rules (guardrail functions) that run alongside agents to validate inputs or outputs.
- **Types:**

  1. **Input Guardrails:** Inspect the user’s prompt before running the agent (e.g., block disallowed content).
  2. **Output Guardrails:** Inspect the agent’s final response (e.g., ensure length limits or format).

- **How It Works:**

  - Decorate an async function with `@input_guardrail` or `@output_guardrail`. The function returns a “tripwire” flag if a rule fails.
  - If `tripwire_triggered=True`, the SDK aborts the run and raises a specific exception (e.g., `InputGuardrailTripwireTriggered`).

- **Why It Matters:**

  - **Safety:** Prevents harmful or unwanted content from being processed or returned.
  - **Quality Control:** Enforces format or domain constraints automatically.

- **Key Takeaway:** Guardrails help you catch unwanted behavior early, ensuring compliance and safety.

---

## 13. Tracing & Lifecycle Hooks

- **Tracing:**

  - **What:** Automatically records each step of the agent workflow—LLM calls, tool calls, handoffs—into a trace log or UI.
  - **Why:** Aids debugging, performance monitoring, and auditing.
  - **How:** Easily enabled by default in the SDK; can be disabled with a single call if needed.

- **Lifecycle Hooks:**

  - **What:** Custom callback methods triggered at key events (e.g., model start/end, tool start/end, handoff start/end).
  - **Why:** Useful for logging, telemetry, or injecting additional side effects (e.g., metrics, user notifications).
  - **How:** Subclass `AgentHooks` and override methods like `on_start`, `on_tool_start`, `on_handoff`, etc. Then assign your hook instance to `agent.hooks`.

- **Key Takeaway:** Use tracing and hooks for deep visibility into agent behavior and easy integration with monitoring tools.

---

## 14. Run Lifecycle & Agent Lifecycle

- **Run Lifecycle:** Each `Runner.run` or `run_sync` call goes through:

  1. **Start:** Send system prompt, tools, and user message to the LLM.
  2. **Tool/Handoff Check:** Model output is parsed. If it calls a tool or triggers a handoff, Runner executes that step and loops again.
  3. **Repeat:** Steps 1–2 continue until the model returns a final answer (no tool/handoff).
  4. **End:** Runner returns `RunResult` with full history, final output, and metadata.

- **Agent Lifecycle:** Each agent object persists its configuration (instructions, tools, handoffs, guardrails). You can clone or modify an agent to create variants. Hooks allow you to tap into the agent’s start/end events each run.
- **Why It Matters:** Understanding this flow helps you predict when tools/handoffs occur, where to insert guardrails, and how to handle errors.
- **Key Takeaway:** The SDK automates iterative model/tool calls; your job is to configure agents and interpret results.

---

## 15. Memory & Agentic RAG

- **Memory:**

  - **What:** A persistent store of past interactions or external knowledge that agents can retrieve at runtime.
  - **How to Integrate:**

    - Store conversation history or user-specific data in a vector database (e.g., Chroma, FAISS).
    - Use the `FileSearchTool` or a custom retrieval function as a tool. The agent calls this tool to fetch relevant documents or past messages.

  - **Why It Matters:** Provides context beyond a single run—useful for personalized assistants or long-term projects.

- **Agentic RAG (Retrieval-Augmented Generation):**

  - **What:** Combines retrieval (fetching documents) with generation (LLM output).
  - **How It Works:** Agent calls a retrieval tool to get relevant context, then supplies that text in the prompt for the LLM to generate an answer.
  - **Why It Matters:** Ensures up-to-date, factual, or domain-specific information without retraining the model.

- **Key Takeaway:** Memory and RAG let your agents “remember” and stay current by pulling in external data at runtime.

---

## 16. Stripe Payments Toolkit

- **What:** A set of prebuilt “tools” and hooks that integrate Stripe’s payment API into Agents SDK applications.
- **Core Components:**

  - **Payment Link Tools:** Create or manage Stripe payment links.
  - **Product/Price Tools:** Create products, set prices, and retrieve product info.
  - **Billing Hook:** Automatically charges users based on token usage or tool calls.

- **Why It Matters:**

  - **Seamless Commerce:** Agents can collect payments, issue invoices, or handle subscriptions without leaving the chat flow.
  - **Monetize Services:** Ideal for pay-per-use LLM applications or SaaS products that charge based on agent interactions.

- **Key Takeaway:** Stripe toolkit transforms your agent into a revenue-generating service by embedding payment logic directly in the workflow.

---

## 17. AI Agents for Microsaas Founders (DACA Overview)

- **What:** DACA (Dapr Agentic Cloud Ascent) is a design pattern for building planet-scale AI agent systems.
- **Core Layers:**

  1. **Presentation:** Next.js, Chainlit, Streamlit for user interfaces.
  2. **Business Logic:** Python, FastAPI, Agents SDK, Dapr sidecars.
  3. **Infrastructure:** Kubernetes, Dapr, microservices, databases.

- **Why It Matters:**

  - **Scalability:** Dapr sidecars handle state, pub/sub, and service-to-service calls, making containers “stateful” even when they’re stateless by default.
  - **Portability:** Run on any cloud or on-premises without vendor lock-in.
  - **Modularity:** Agents SDK sits in the business logic layer, orchestrating AI components.

- **Key Takeaway:** DACA provides best practices for architecting robust, scalable AI services—agents and microservices working together.

---

## 18. Kubernetes & Dapr for Agentic AI

- **Kubernetes (K8s):**

  - Orchestrates containers across a cluster of nodes.
  - Manages scaling, fault tolerance, networking, and deployments.

- **Dapr (Distributed Application Runtime):**

  - Lightweight “sidecar” that provides building blocks for microservices: state management, pub/sub messaging, service invocation, and secrets.
  - Makes containers stateful by abstracting calls to external stores (databases, caches).

- **Why It Matters for Agents:**

  - **Scaling Agents:** Use Kubernetes to autoscale agent pods based on load.
  - **Stateful Agent Services:** Dapr keeps conversation state, memory, or metadata outside the container.
  - **Inter-Service Calls:** Agents can call microservices via Dapr’s service invocation APIs without worrying about networking details.

- **Key Takeaway:** Combine Kubernetes + Dapr to deploy, scale, and manage complex agent-based microservices reliably.

---

## 19. Agent Delegation Patterns (Triage & Handoff)

- **Triage Agent:**

  - Acts as an entry point, classifies or understands user intent.
  - Decides which specialized sub-agent (billing, shipping, FAQ) should handle the request.

- **Handoff Agent:**

  - The specialized agent that receives the delegated task.
  - Focuses on a narrow domain (e.g., “RefundAgent” only processes refunds).

- **Extended Response:**

  - Variation where the triage agent collects results from sub-agents and synthesizes a unified answer.

- **Why It Matters:**

  - **Separation of Concerns:** Each agent has one responsibility—easier to maintain and test.
  - **Scalability:** You can add new sub-agents without rewriting the triage logic.

- **Key Takeaway:** Use delegation to build modular, maintainable multi-agent systems.

---

## 20. Agent Loop (Detailed Flow)

- **Core Steps in Each Run:**

  1. **System Prompt & Tools Metadata:** Sent to LLM along with any context or user message.
  2. **LLM Output:** Model replies—either plain text, a tool call request, or a handoff request.
  3. **Tool Execution:** If a tool is called, the Runner runs that tool and appends its output to the conversation.
  4. **Handoff Execution:** If a handoff is triggered, the Runner switches to the designated sub-agent and continues.
  5. **Loop:** Steps 1–4 repeat until the agent produces a final answer (no further actions).
  6. **Return:** The Runner returns the full history and final result.

- **Why It Matters:**

  - Understanding this loop helps you configure max turns, debug tool calls, and ensure your prompts lead to the desired behavior.

- **Key Takeaway:** The Agent SDK automates iterative LLM/tool calls—just define agents and let the Runner handle the rest.

---

## 21. Agents’ Life Cycle

- **Agent Creation:** Define `name`, `instructions`, `tools`, `handoffs`, `guardrails`, etc.
- **Agent Run Initialization:** On first run, system prompt is sent to LLM; guardrails are checked.
- **Agent Execution:** Model calls, tool calls, and handoffs happen in cycles.
- **Agent Completion:** Runner stops when a final answer is reached or max turns exceeded.
- **Agent Reuse/Cloning:** You can clone an existing agent (modify instructions or tools) to create a variant.
- **Key Takeaway:** Agents persist configuration—each `run` is a fresh execution of that agent’s workflow.

---

## 22. Memory (Context Management)

- **Short-Term Context:**

  - **Conversation History:** Maintained automatically in a single `Runner.run` session.
  - **Dynamic Instructions & Context Injection:** Pass a context object (e.g., user profile) so instructions adapt at runtime.

- **Long-Term Memory:**

  - **RAG via Vector Stores:** Store documents or prior messages in a vector database; use a retrieval tool to fetch relevant context.
  - **External Memory Libraries:** Integrate with solutions like LangChain or mem0 for persistent user/session memory.

- **Why It Matters:**

  - Agents can “remember” personalization or relevant facts beyond one turn.
  - Ensures continuity across sessions and long-lived applications.

- **Key Takeaway:** Combine built-in short-term context with external RAG pipelines for robust memory.

---

## 23. Agentic RAG (Retrieval-Augmented Generation)

- **What:** A technique where an agent first retrieves external documents or data (via a retrieval tool), then uses that content to generate a more accurate and up-to-date response.
- **Flow:**

  1. **User Query** → 2. **Retrieve Relevant Docs** (tool call) → 3. **Append Docs to LLM Prompt** → 4. **LLM Generates Answer**

- **Why It Matters:**

  - Access real-time or large knowledge bases without fine-tuning the model.
  - Provides factual grounding and reduces hallucinations on niche topics.

- **Key Takeaway:** RAG combines retrieval and generation for reliable, context-rich answers.

---

## 24. Payments Integration (Stripe Toolkit)

- **What:** A toolkit that exposes Stripe’s payment operations as agent tools.
- **Capabilities:**

  - Create products, prices, and payment links.
  - Charge customers or record usage automatically.
  - Billing hooks track LLM usage (tokens, tool calls) and bill via your Stripe account.

- **Why It Matters:**

  - Turn your agent into a revenue-generating interface.
  - Seamlessly integrate commerce (subscriptions, pay-per-use) directly in the conversation.

- **Key Takeaway:** Use Stripe Toolkit to embed payments in your agent workflows.

---

## 25. Anthropic Design Patterns (Agent SDK Alignment)

- **Prompt Chaining:** Break tasks into ordered steps—Agents SDK handles sequential agent calls to follow a chain of prompts.
- **Routing:** Direct each task to the best agent or tool—achieved by defining handoffs or agent-as-tool logic.
- **Parallelization:** Run multiple agent calls simultaneously (e.g., with async) and combine results.
- **Orchestrator-Workers:** One orchestrator agent decomposes tasks for worker agents—supported via handoffs or agent-as-tool.
- **Evaluator-Optimizer:** Use a dedicated “evaluator” agent or guardrail to assess and refine the output of another agent.
- **Key Takeaway:** The Agents SDK makes it straightforward to apply Anthropic’s recommended design patterns for multi-agent systems.

---

## 26. DACA (Dapr Agentic Cloud Ascent)

- **High-Level Concept:** Architectural pattern for building planet-scale AI agent systems using microservices.
- **Key Layers:**

  1. **Presentation:** Next.js, Chainlit, Streamlit for UI.
  2. **Business Logic:** Python, FastAPI, OpenAI Agents SDK, Dapr sidecars.
  3. **Infrastructure:** Kubernetes, Dapr, microservices, state stores, messaging.

- **Why It Matters:**

  - **Scalable & Portable:** Dapr sidecars manage state and inter-service calls, while Kubernetes manages containers.
  - **Modular:** Agents SDK handles AI workflows; Dapr handles stateful operations; front-end frameworks handle UI.

- **Key Takeaway:** DACA combines Agents SDK with cloud-native best practices to deploy resilient, scalable AI services.

---

## 27. Kubernetes & Dapr Refresher

- **Kubernetes (K8s):**

  - Schedules containers (pods) across a cluster.
  - Handles autoscaling, rolling updates, and networking.

- **Dapr (Distributed Application Runtime):**

  - Runs as a sidecar next to your container.
  - Provides state management (key-value stores), pub/sub messaging, service invocation, and input/output bindings.

- **Why It Matters:**

  - **Stateful Agents:** Dapr sidecars store agent state externally (e.g., conversation history, memory).
  - **Service Invocation:** Agents can call other microservices seamlessly through Dapr.
  - **Reliability:** Kubernetes + Dapr ensure your agent services remain available and scalable.

- **Key Takeaway:** Use Kubernetes to deploy agent microservices; use Dapr for state and communication.

---

## 28. Putting It All Together: Development Workflow

1. **Set Up Dependencies:** Use UV (or pip/Poetry) to install Python, Agents SDK, and any tools (e.g., Stripe toolkit).
2. **Define Agents & Tools:** Write clear instructions for each agent; register function tools or hosted tools as needed.
3. **Configure Guardrails & Tracing:** Add safety checks and enable tracing for debugging.
4. **Build UI with Chainlit:** Create a chat interface to visualize streaming events and user interactions.
5. **Add Memory/RAG:** Connect a vector store (e.g., Chroma) and use a retrieval tool to provide context.
6. **Integrate Payments (Optional):** Include Stripe toolkit tools if monetization is required.
7. **Deploy on Kubernetes + Dapr:** Package each agent service in a container, let Dapr sidecars handle state, and use Kubernetes for scaling.
8. **Monitor & Iterate:** Use tracing logs, guardrail alerts, and user feedback to refine prompts, guardrails, and agent logic.

---

## 29. Quick-reference Glossary

- **Agent:** An LLM-based unit with instructions and optional tools/guardrails.
- **Tool:** Any action (Python function or hosted service) that an agent can invoke.
- **Handoff:** Mechanism for transferring control from one agent to another.
- **Agent-as-Tool:** Wrapping an entire agent so it can be called like a function.
- **Guardrail:** Input/output validator that can abort an agent run if a constraint is violated.
- **Tracer:** Records each step of the agent’s execution for debugging.
- **Streaming:** Receiving partial outputs as the LLM generates tokens or events.
- **Pydantic:** Library for defining and validating structured data models (used for tool arguments, outputs, and handoffs).
- **Chainlit:** UI library for building chat apps around LLMs and agents.
- **LiteLLM / OpenRouter:** Libraries/platforms for accessing multiple LLM providers through a unified interface.
- **RAG:** Retrieval-Augmented Generation—combining document retrieval with LLM generation for up-to-date or factual answers.
- **Stripe Toolkit:** Prebuilt agent tools for handling payments, products, and billing via Stripe.
- **Dapr:** Sidecar runtime that adds state management, pub/sub, and service invocation to microservices.
- **Kubernetes:** Container orchestration platform for deploying and scaling agent services.

---
