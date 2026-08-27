import uuid
from typing import List, Dict, Any, Optional, Set, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
import time

logger = logging.getLogger("H11_ETL_DATA")

class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"

class DagState(Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

@dataclass
class EtlConfig:
    max_retries: int = 3
    retry_delay_sec: int = 5
    default_batch_size: int = 1000

@dataclass
class DagTrigger:
    dag_id: str
    execution_date: str
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DagResult:
    dag_id: str
    state: DagState
    tasks_metrics: Dict[str, Any]
    duration_sec: float

class EtlTask:
    def __init__(self, task_id: str, operator: Callable, dependencies: List[str] = None):
        self.task_id = task_id
        self.operator = operator
        self.dependencies = dependencies or []
        self.state = TaskState.PENDING
        self.retries = 0

class EtlDag:
    def __init__(self, dag_id: str):
        self.dag_id = dag_id
        self.tasks: Dict[str, EtlTask] = {}
        
    def add_task(self, task: EtlTask):
        self.tasks[task.task_id] = task

class H11EtlAgent:
    """
    H11-ETL-DATA: Minimal DAG orchestrator and schema transformation engine.
    """
    def __init__(self, config: EtlConfig):
        self.config = config
        self.dags: Dict[str, EtlDag] = {}
        logger.info("Initialized H11-ETL-DATA orchestrator.")

    def register_dag(self, dag: EtlDag):
        # Validate topological sort to ensure no cycles
        self._topological_sort(dag)
        self.dags[dag.dag_id] = dag
        logger.info(f"Registered DAG: {dag.dag_id}")

    def execute_dag(self, trigger: DagTrigger) -> DagResult:
        if trigger.dag_id not in self.dags:
            raise ValueError(f"DAG {trigger.dag_id} not found.")
            
        dag = self.dags[trigger.dag_id]
        logger.info(f"Starting DAG run for {trigger.dag_id} @ {trigger.execution_date}")
        start_time = time.time()
        
        # Reset task states
        for task in dag.tasks.values():
            task.state = TaskState.PENDING
            task.retries = 0
            
        execution_order = self._topological_sort(dag)
        metrics = {}
        
        for task_id in execution_order:
            task = dag.tasks[task_id]
            success = self._execute_task_with_retries(task, trigger)
            metrics[task_id] = task.state.value
            
            if not success:
                logger.error(f"DAG {trigger.dag_id} failed at task {task_id}")
                return DagResult(
                    dag_id=trigger.dag_id,
                    state=DagState.FAILED,
                    tasks_metrics=metrics,
                    duration_sec=time.time() - start_time
                )
                
        return DagResult(
            dag_id=trigger.dag_id,
            state=DagState.SUCCESS,
            tasks_metrics=metrics,
            duration_sec=time.time() - start_time
        )

    def _execute_task_with_retries(self, task: EtlTask, context: DagTrigger) -> bool:
        task.state = TaskState.RUNNING
        while True:
            try:
                logger.info(f"Executing task: {task.task_id}")
                # Execute the actual user-defined function
                task.operator(context)
                task.state = TaskState.SUCCESS
                return True
            except Exception as e:
                logger.warning(f"Task {task.task_id} failed: {e}")
                if task.retries < self.config.max_retries:
                    task.retries += 1
                    task.state = TaskState.RETRYING
                    logger.info(f"Retrying task {task.task_id} ({task.retries}/{self.config.max_retries})")
                    time.sleep(self.config.retry_delay_sec)
                else:
                    task.state = TaskState.FAILED
                    return False

    def _topological_sort(self, dag: EtlDag) -> List[str]:
        """Kahn's algorithm for topological sorting and cycle detection."""
        in_degree = {task_id: 0 for task_id in dag.tasks}
        graph = {task_id: [] for task_id in dag.tasks}
        
        for task_id, task in dag.tasks.items():
            for dep in task.dependencies:
                if dep not in in_degree:
                    raise ValueError(f"Dependency {dep} not found in DAG.")
                graph[dep].append(task_id)
                in_degree[task_id] += 1
                
        queue = [t for t, d in in_degree.items() if d == 0]
        sorted_tasks = []
        
        while queue:
            node = queue.pop(0)
            sorted_tasks.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        if len(sorted_tasks) != len(dag.tasks):
            raise ValueError(f"Cycle detected in DAG {dag.dag_id}")
            
        return sorted_tasks

# --- Example Operators ---
def extract_operator(context):
    print(f"[{context.dag_id}] Extracting data for {context.execution_date}")

def transform_operator(context):
    print(f"[{context.dag_id}] Transforming schemas (idempotent step)")

def load_operator(context):
    print(f"[{context.dag_id}] Loading to Snowflake DWH")

if __name__ == "__main__":
    agent = H11EtlAgent(EtlConfig(retry_delay_sec=1))
    
    my_dag = EtlDag("nightly_sales_load")
    my_dag.add_task(EtlTask("extract_sales", extract_operator))
    my_dag.add_task(EtlTask("transform_sales", transform_operator, dependencies=["extract_sales"]))
    my_dag.add_task(EtlTask("load_sales", load_operator, dependencies=["transform_sales"]))
    
    agent.register_dag(my_dag)
    
    trigger = DagTrigger(dag_id="nightly_sales_load", execution_date="2026-08-27")
    res = agent.execute_dag(trigger)
    print(f"Pipeline finished with state {res.state.value} in {res.duration_sec:.2f}s")
