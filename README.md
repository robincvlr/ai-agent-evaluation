# ai-agent-evaluation
Generative AI application evaluation with Foundry

## Motivations
Numerous applications are now being developed with embedded generative AI capabilities. This is a quick test designed to monitor the outputs from generative pipelines.

## Install
```
poetry install --with dev
eval $(poetry env activate)
python -m pytest
```

## Evaluators

| **Evaluator** | **Description** | **Use Case** |
|----------------|-----------------|---------------|
| `IntentResolutionEvaluator` | Evaluates how well a model correctly interprets and fulfills a user’s intent. | Useful for intent classification, conversational AI, and task-oriented bots. |
| `TaskAdherenceEvaluator` | Measures how accurately a model adheres to the given instructions or completes a task. | Ideal for prompt following, procedural responses, and step-by-step reasoning tasks. |
| `ToolCallAccuracyEvaluator` | Assesses whether the model calls external tools (APIs, functions) correctly and appropriately. | Suitable for function calling agents, retrieval-augmented systems, or tool-using LLMs. |
| `RelevanceEvaluator` | Evaluates the relevance of model outputs with respect to a query, prompt, or context. | Commonly used for information retrieval, summarization, and search quality. |
| `CoherenceEvaluator` | Measures the logical consistency and flow of the generated text. | Useful for story generation, summarization, and dialogue coherence. |
| `CodeVulnerabilityEvaluator` | Detects potential vulnerabilities or security issues in generated code. | Ideal for AI-assisted code generation and secure software development. |
| `ContentSafetyEvaluator` | Checks generated text for unsafe or harmful content such as hate speech, violence, or adult material. | Essential for content moderation and responsible AI deployment. |
| `IndirectAttackEvaluator` | Evaluates model susceptibility to indirect prompt injection or malicious inputs. | Used to test model robustness and security against adversarial attacks. |
| `FluencyEvaluator` | Measures the grammatical correctness, readability, and fluency of the text. | Useful for text generation, translation, and summarization tasks. |
