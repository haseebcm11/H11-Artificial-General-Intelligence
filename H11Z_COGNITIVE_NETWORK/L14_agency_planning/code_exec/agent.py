import os
import sys
import uuid
import time
import subprocess
import tempfile
import asyncio
from typing import Dict, Any, List, Optional, Protocol
from dataclasses import dataclass, field
from enum import Enum

class RuntimeLanguage(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    BASH = "bash"

@dataclass
class ExecutionRequest:
    code: str
    language: RuntimeLanguage
    timeout_sec: float = 30.0
    install_dependencies: List[str] = field(default_factory=list)
    environment_variables: Dict[str, str] = field(default_factory=dict)
    workspace_dir: Optional[str] = None

@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    duration_sec: float
    error: Optional[str] = None
    state_diff: Dict[str, Any] = field(default_factory=dict)

class IsolationProvider(Protocol):
    async def provision(self, workspace_id: str) -> str: ...
    async def execute(self, req: ExecutionRequest, container_id: str) -> ExecutionResult: ...
    async def cleanup(self, container_id: str) -> None: ...

class LocalSubprocessIsolation(IsolationProvider):
    """
    Local isolation provider that uses standard subprocesses but enforces timeouts
    and directory jails to simulate a sandboxed environment.
    """
    def __init__(self, base_workdir: str):
        self.base_workdir = base_workdir
        os.makedirs(self.base_workdir, exist_ok=True)

    async def provision(self, workspace_id: str) -> str:
        sandbox_path = os.path.join(self.base_workdir, f"sandbox_{workspace_id}")
        os.makedirs(sandbox_path, exist_ok=True)
        return sandbox_path

    async def _install_deps(self, language: RuntimeLanguage, deps: List[str], cwd: str) -> None:
        if not deps: 
            return
        if language == RuntimeLanguage.PYTHON:
            proc = await asyncio.create_subprocess_exec(
                sys.executable, "-m", "pip", "install", *deps,
                cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            await proc.communicate()
        elif language == RuntimeLanguage.JAVASCRIPT:
            proc = await asyncio.create_subprocess_exec(
                "npm", "install", *deps,
                cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            await proc.communicate()

    async def execute(self, req: ExecutionRequest, container_dir: str) -> ExecutionResult:
        start_time = time.monotonic()
        await self._install_deps(req.language, req.install_dependencies, container_dir)
        
        env = os.environ.copy()
        env.update(req.environment_variables)

        script_path = os.path.join(container_dir, f"script_{uuid.uuid4().hex[:8]}")
        
        if req.language == RuntimeLanguage.PYTHON:
            script_path += ".py"
            cmd = [sys.executable, script_path]
        elif req.language == RuntimeLanguage.JAVASCRIPT:
            script_path += ".js"
            cmd = ["node", script_path]
        else:
            script_path += ".sh"
            cmd = ["bash", script_path]

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(req.code)

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd, cwd=container_dir, env=env,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                proc.communicate(), timeout=req.timeout_sec
            )
            duration = time.monotonic() - start_time
            return ExecutionResult(
                stdout=stdout_bytes.decode('utf-8', errors='replace'),
                stderr=stderr_bytes.decode('utf-8', errors='replace'),
                exit_code=proc.returncode or 0,
                duration_sec=duration
            )
        except asyncio.TimeoutError:
            proc.kill()
            duration = time.monotonic() - start_time
            return ExecutionResult(
                stdout="", stderr="Execution timed out.", exit_code=-1,
                duration_sec=duration, error="TimeoutError"
            )
        except Exception as e:
            duration = time.monotonic() - start_time
            return ExecutionResult(
                stdout="", stderr=str(e), exit_code=-2,
                duration_sec=duration, error="SystemError"
            )

    async def cleanup(self, container_dir: str) -> None:
        import shutil
        if os.path.exists(container_dir):
            shutil.rmtree(container_dir, ignore_errors=True)

class StatefulSessionManager:
    """
    Manages long-lived execution sessions where state and file systems persist
    across multiple execution requests.
    """
    def __init__(self, isolation: IsolationProvider):
        self.isolation = isolation
        self.active_sessions: Dict[str, str] = {}

    async def start_session(self, session_id: str) -> None:
        container_path = await self.isolation.provision(session_id)
        self.active_sessions[session_id] = container_path

    async def run_in_session(self, session_id: str, req: ExecutionRequest) -> ExecutionResult:
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not active.")
        return await self.isolation.execute(req, self.active_sessions[session_id])

    async def end_session(self, session_id: str) -> None:
        if session_id in self.active_sessions:
            await self.isolation.cleanup(self.active_sessions[session_id])
            del self.active_sessions[session_id]

class CodeExecAgent:
    """
    Main agent endpoint for code execution logic.
    """
    def __init__(self):
        self.workdir = tempfile.mkdtemp(prefix="h11_code_exec_")
        self.provider = LocalSubprocessIsolation(self.workdir)
        self.session_manager = StatefulSessionManager(self.provider)

    async def handle_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        action = payload.get("action")
        session_id = payload.get("session_id", uuid.uuid4().hex)

        if action == "start_session":
            await self.session_manager.start_session(session_id)
            return {"status": "success", "session_id": session_id}
            
        elif action == "execute":
            if session_id not in self.session_manager.active_sessions:
                await self.session_manager.start_session(session_id)
                
            req = ExecutionRequest(
                code=payload["code"],
                language=RuntimeLanguage(payload.get("language", "python")),
                timeout_sec=payload.get("timeout_sec", 30.0),
                install_dependencies=payload.get("dependencies", []),
                environment_variables=payload.get("env", {})
            )
            result = await self.session_manager.run_in_session(session_id, req)
            return {
                "session_id": session_id,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.exit_code,
                "duration": result.duration_sec,
                "error": result.error
            }
            
        elif action == "end_session":
            await self.session_manager.end_session(session_id)
            return {"status": "success"}
            
        else:
            raise ValueError(f"Unknown action {action}")

if __name__ == "__main__":
    # Quick test harness
    async def test():
        agent = CodeExecAgent()
        res = await agent.handle_request({
            "action": "execute",
            "session_id": "test_1",
            "code": "print('Hello Sandboxed World')",
            "language": "python"
        })
        print("Result:", res)
        await agent.handle_request({"action": "end_session", "session_id": "test_1"})
        
    asyncio.run(test())
