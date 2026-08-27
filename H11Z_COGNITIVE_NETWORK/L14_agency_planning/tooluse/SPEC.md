# H11-TOOLUSE

## Architecture
- **Tool Registry with Semantic Discovery:** Uses keyword/TF-IDF indexing to discover tools based on agent intent. Ready for dense embedding extensions.
- **Toolformer Integration:** Parses text for embedded tool calls `[ToolName(arg1=val)]` and enables self-supervised tool usage generation.
- **Dependency Chaining:** Evaluates Directed Acyclic Graphs (DAGs) of tools where outputs of previous tools can be routed into inputs of subsequent tools using `$invocation_id.key` syntax.
- **Permission Management (RBAC):** Prevents automated execution of `DANGEROUS` tools, enforcing human-in-the-loop or supervisor authorization.
- **Resilience:** Implements retry mechanics, parameter validation via JSON Schemas, and traceback logging.
