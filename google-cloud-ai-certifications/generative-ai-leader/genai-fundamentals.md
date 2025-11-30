# GenAI Fundamentals

_Last Updated: November 30, 2025_

This is a glossary and conceptual foundation for GenAI Leader candidates. Use it while working through Skills Boost courses and official documentation.

## Core Concepts

### Foundation Models and LLMs

**What they are:**  
Large Language Models (LLMs) are neural networks trained on vast amounts of text data (pre-training). They learn statistical patterns and can generate coherent text in response to prompts.

**Foundation models** are general-purpose LLMs (like Gemini, PaLM) that can be adapted for many downstream tasks.

**Key points:**
- Trained on billions of parameters using self-supervised learning
- Emerge with "in-context learning": they can perform tasks described in prompts without explicit fine-tuning
- Generative: they produce text token by token, making them useful for dialogue, summarisation, code, creative content

### Tokens

**What they are:** Text is broken into small units called tokens (roughly words, but not exactly). "Hello" might be 1 token; "contract" might be multiple.

**Why it matters:**
- Model input/output is measured in tokens; billing is often per token
- Context windows (max tokens a model can attend to at once) limit input + output size
- Longer contexts enable more complex reasoning but increase cost

### Context Windows

**What they are:** The maximum number of tokens a model can consider at once.

**Examples:**
- Older models: 2k–4k tokens (~1–2 pages of text)
- Modern Gemini: up to 32k or 100k+ tokens (~10–30+ pages)

**Implication:** Larger context windows allow longer documents, more examples in prompts, and more conversation history, but cost more.

### Prompting

**What it is:** The art and science of instructing a model to perform a task via text input.

**Techniques:**
- **System prompt:** Sets the tone and constraints (e.g., "You are a healthcare data analyst. Respond only in British English.")
- **Few-shot prompting:** Provide examples of the task before asking the model to perform it
- **Chain-of-thought:** Ask the model to "think step by step" to improve reasoning
- **Temperature:** Controls randomness; lower = more deterministic, higher = more creative

### Embeddings

**What they are:** Numerical representations of text (a list of numbers). Models convert text into embeddings so that similar texts have similar embeddings (close in vector space).

**Use case:** Comparing documents, semantic search, clustering.

### Retrieval-Augmented Generation (RAG)

**What it is:** A pattern where:
1. A user query comes in
2. Relevant documents are retrieved from a knowledge base (search or embedding-based)
3. The retrieval results are added to the prompt as context
4. The LLM generates an answer based on both the query and the retrieved context

**Why it's powerful:** Avoids hallucination (making up facts) by grounding responses in real data. Essential for healthcare, legal, and regulated workloads.

**Example:** A healthcare chatbot retrieves relevant clinical guidelines before answering a question, ensuring medical accuracy.

### Fine-tuning

**What it is:** Adapting a pre-trained model to a specific domain or task by training it on your own data.

**When to use:**
- You have domain-specific language or jargon
- Few-shot prompting + RAG don't achieve desired quality
- You want to reduce model size (distillation) for cost/latency

**Challenges:**
- Requires labelled training data
- Expensive (compute and data annotation)
- Risk of overfitting on small datasets

### Safety Filters and Guardrails

**What they are:** Systems that block harmful outputs (hate speech, violence, misinformation) or refuse certain requests.

**Google Cloud approach:**
- Gemini and other models have built-in safety filters
- Responsible AI toolkit provides bias and harm detection
- Custom guardrails can be layered on top via Vertex AI

**In healthcare context:** Critical for ensuring patient safety and regulatory compliance.

## How These Concepts Interconnect

User Query → Prompt → Foundation Model → (Optional) Retrieve Data → Generate Response → Apply Guardrails → Return Output

**For a leader's perspective:**
- Larger model = more capability but higher cost and latency
- Prompt engineering = free, quick wins for adaptation
- Fine-tuning = investment for domain excellence
- RAG = safer, more reliable for sensitive domains (healthcare, legal)
- Safety filters + guardrails = non-negotiable for regulated work

## Cross-references

See `vertex-ai-overview.md` for how Google Cloud products implement these concepts, and `responsible-ai.md` for governance and ethics.
