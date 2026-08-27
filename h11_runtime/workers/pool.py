"""Worker pool concurrency executor."""
from __future__ import annotations

from dataclasses import dataclass
import inspect
from typing import Any, Dict

from .task import WorkerTask


class WorkerPool:
    """C02 Worker Pool: Dispatches agent tasks across concurrency worker slots (Section 45)."""

    def __init__(self, concurrency: int = 8) -> None:
        self.concurrency = concurrency
        self.active_tasks: Dict[str, WorkerTask] = {}
        self.completed_tasks: Dict[str, WorkerTask] = {}

    async def execute_task(self, task: WorkerTask) -> Any:
        task.status = "RUNNING"
        self.active_tasks[task.task_id] = task
        try:
            if inspect.iscoroutinefunction(task.func):
                res = await task.func(*task.args, **task.kwargs)
            else:
                res = task.func(*task.args, **task.kwargs)
            task.status = "COMPLETED"
            task.result = res
            return res
        except Exception as e:
            task.status = "FAILED"
            task.error = str(e)
            raise
        finally:
            self.active_tasks.pop(task.task_id, None)
            self.completed_tasks[task.task_id] = task
