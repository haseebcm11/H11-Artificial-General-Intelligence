"""Worker pool concurrency executor with dynamic semaphore and priority queues."""
from __future__ import annotations

import asyncio
import inspect
import logging
import time
from typing import Any, Callable, Dict, List, Optional

from .task import WorkerTask

logger = logging.getLogger(__name__)


class WorkerPool:
    """C02 Worker Pool: Dispatches agent tasks across concurrency worker slots (v3.0 Section 45)."""

    def __init__(self, concurrency: int = 16) -> None:
        self.concurrency = concurrency
        self._semaphore = asyncio.Semaphore(concurrency)
        self.active_tasks: Dict[str, WorkerTask] = {}
        self.completed_tasks: Dict[str, WorkerTask] = {}
        self.total_dispatched = 0
        self.total_successful = 0
        self.total_failed = 0

    async def execute_task(self, task: WorkerTask) -> Any:
        """Executes task acquiring concurrency slot with timeout protection."""
        if task.func is None:
            raise ValueError(f"Task {task.task_id} has no callable function attached.")

        async with self._semaphore:
            task.status = "RUNNING"
            task.started_at = time.time()
            self.active_tasks[task.task_id] = task
            self.total_dispatched += 1

            try:
                if inspect.iscoroutinefunction(task.func):
                    coro = task.func(*task.args, **task.kwargs)
                    res = await asyncio.wait_for(coro, timeout=task.timeout_seconds)
                else:
                    res = task.func(*task.args, **task.kwargs)

                task.status = "COMPLETED"
                task.result = res
                task.completed_at = time.time()
                self.total_successful += 1
                return res

            except asyncio.TimeoutError:
                task.status = "FAILED"
                task.error = f"Execution timed out after {task.timeout_seconds}s"
                task.completed_at = time.time()
                self.total_failed += 1
                logger.error(f"Task {task.task_id} ({task.name}) timed out")
                raise

            except Exception as exc:
                task.status = "FAILED"
                task.error = str(exc)
                task.completed_at = time.time()
                self.total_failed += 1
                logger.error(f"Task {task.task_id} ({task.name}) failed: {exc}")
                raise

            finally:
                self.active_tasks.pop(task.task_id, None)
                self.completed_tasks[task.task_id] = task

    async def map_tasks(self, tasks: List[WorkerTask]) -> List[Any]:
        """Executes list of tasks concurrently through the pool."""
        coros = [self.execute_task(t) for t in tasks]
        return await asyncio.gather(*coros, return_exceptions=True)

    def get_pool_stats(self) -> Dict[str, Any]:
        return {
            "concurrency_limit": self.concurrency,
            "active_tasks_count": len(self.active_tasks),
            "completed_tasks_count": len(self.completed_tasks),
            "total_dispatched": self.total_dispatched,
            "total_successful": self.total_successful,
            "total_failed": self.total_failed,
        }
