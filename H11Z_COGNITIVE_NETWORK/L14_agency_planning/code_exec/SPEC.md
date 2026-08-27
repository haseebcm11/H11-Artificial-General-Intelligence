# H11-CODE-EXEC

## Overview
The Code Execution Agent (`H11-CODE-EXEC`) manages secure, sandboxed code execution environments for the H11 Cognitive Substrate. It handles executing dynamic code in multiple languages, managing dependencies, and providing a persistent execution state (stateful execution) across multiple steps.

## Architecture
- **Isolation Providers**: Abstractions to isolate code environments. Initially implements a directory-jailed local subprocess executor, with an interface designed to swap in Docker or E2B for true containerized isolation.
- **StatefulSessionManager**: Maintains active sessions, bridging multiple requests into a shared workspace so files and variables persist.
- **Execution Engine**: Manages asynchronous I/O, output capture, strict timeout enforcement, and environment setup.

## Features
- **Multi-language Support**: Python, JS, Bash out of the box.
- **Dynamic Dependency Installation**: Automatic installation of PIP/NPM packages prior to run.
- **Strict Execution Timeouts**: Mitigates runaway loops and resource exhaustion.
- **Workspace Jailing**: Each session operates in its own dedicated directory.
