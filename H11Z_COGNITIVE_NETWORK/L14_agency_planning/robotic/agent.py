import numpy as np
import math
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
import random

@dataclass
class Pose:
    x: float
    y: float
    z: float
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0

@dataclass
class Obstacle:
    center: np.ndarray
    radius: float

class KinematicChain:
    """
    Represents a serial kinematic chain for a robotic arm.
    """
    def __init__(self, link_lengths: List[float]):
        self.links = link_lengths
        self.num_joints = len(link_lengths)
        
    def forward_kinematics(self, joint_angles: np.ndarray) -> np.ndarray:
        """
        Computes the end-effector position given joint angles (Planar N-link).
        """
        x, y = 0.0, 0.0
        theta = 0.0
        for i in range(self.num_joints):
            theta += joint_angles[i]
            x += self.links[i] * math.cos(theta)
            y += self.links[i] * math.sin(theta)
        # Extending to pseudo-3D by keeping Z constant for planar simplicity
        return np.array([x, y, 0.0])

    def jacobian(self, joint_angles: np.ndarray) -> np.ndarray:
        """
        Computes the Jacobian matrix for the current joint configuration.
        """
        J = np.zeros((3, self.num_joints))
        theta = 0.0
        angles_sum = []
        for i in range(self.num_joints):
            theta += joint_angles[i]
            angles_sum.append(theta)
            
        # J = [dx/dtheta; dy/dtheta; dz/dtheta]
        for i in range(self.num_joints):
            dx_dtheta_i = 0.0
            dy_dtheta_i = 0.0
            for j in range(i, self.num_joints):
                dx_dtheta_i += -self.links[j] * math.sin(angles_sum[j])
                dy_dtheta_i += self.links[j] * math.cos(angles_sum[j])
            J[0, i] = dx_dtheta_i
            J[1, i] = dy_dtheta_i
            J[2, i] = 0.0  # Pseudo-planar
            
        return J

class InverseKinematicsSolver:
    """
    Solves inverse kinematics using Damped Least Squares (Levenberg-Marquardt).
    """
    def __init__(self, chain: KinematicChain, max_iters: int = 100, tolerance: float = 1e-3):
        self.chain = chain
        self.max_iters = max_iters
        self.tolerance = tolerance
        self.damping = 0.1

    def solve(self, start_joints: np.ndarray, target_pos: np.ndarray) -> Tuple[np.ndarray, bool]:
        q = start_joints.copy()
        
        for _ in range(self.max_iters):
            current_pos = self.chain.forward_kinematics(q)
            error = target_pos - current_pos
            
            if np.linalg.norm(error) < self.tolerance:
                return q, True
                
            J = self.chain.jacobian(q)
            # Damped least squares: J_T * (J * J_T + lambda^2 * I)^-1
            J_T = J.T
            J_J_T = J @ J_T
            I = np.eye(J.shape[0])
            
            J_pseudo = J_T @ np.linalg.inv(J_J_T + (self.damping ** 2) * I)
            
            delta_q = J_pseudo @ error
            q += delta_q
            
            # Wrap angles to [-pi, pi]
            q = (q + np.pi) % (2 * np.pi) - np.pi
            
        return q, False

class RRTPlanner:
    """
    Rapidly-exploring Random Tree for configuration space path planning.
    """
    class Node:
        def __init__(self, q: np.ndarray):
            self.q = q
            self.parent: Optional['RRTPlanner.Node'] = None

    def __init__(self, chain: KinematicChain, joint_limits: Tuple[float, float], max_step: float = 0.1):
        self.chain = chain
        self.joint_limits = joint_limits
        self.max_step = max_step
        
    def check_collision(self, q: np.ndarray, obstacles: List[Obstacle]) -> bool:
        """
        Check if any point on the arm collides with obstacles.
        """
        x, y = 0.0, 0.0
        theta = 0.0
        
        # Simple point collision for each joint
        for i in range(self.chain.num_joints):
            theta += q[i]
            x += self.chain.links[i] * math.cos(theta)
            y += self.chain.links[i] * math.sin(theta)
            pos = np.array([x, y, 0.0])
            
            for obs in obstacles:
                if np.linalg.norm(pos[:2] - obs.center[:2]) < obs.radius:
                    return True
        return False
        
    def plan(self, q_start: np.ndarray, q_goal: np.ndarray, obstacles: List[Obstacle], max_nodes: int = 1500) -> Optional[List[np.ndarray]]:
        start_node = self.Node(q_start)
        tree = [start_node]
        
        for _ in range(max_nodes):
            # Sample random configuration or bias towards goal
            if random.random() < 0.1:
                q_rand = q_goal
            else:
                q_rand = np.random.uniform(self.joint_limits[0], self.joint_limits[1], self.chain.num_joints)
                
            # Find nearest node
            nearest_node = min(tree, key=lambda n: np.linalg.norm(n.q - q_rand))
            
            # Step towards q_rand
            direction = q_rand - nearest_node.q
            dist = np.linalg.norm(direction)
            if dist > self.max_step:
                q_new = nearest_node.q + (direction / dist) * self.max_step
            else:
                q_new = q_rand
                
            if not self.check_collision(q_new, obstacles):
                new_node = self.Node(q_new)
                new_node.parent = nearest_node
                tree.append(new_node)
                
                # Check if we reached goal
                if np.linalg.norm(q_new - q_goal) < self.max_step:
                    goal_node = self.Node(q_goal)
                    goal_node.parent = new_node
                    tree.append(goal_node)
                    
                    # Backtrack path
                    path = []
                    curr = goal_node
                    while curr is not None:
                        path.append(curr.q)
                        curr = curr.parent
                    return path[::-1]
                    
        return None

class TrajectoryOptimizer:
    """
    Generates minimum jerk trajectories from a sequence of waypoints.
    """
    @staticmethod
    def generate_minimum_jerk(waypoints: List[np.ndarray], duration: float, dt: float = 0.05) -> List[np.ndarray]:
        if len(waypoints) < 2:
            return waypoints
            
        t_total = duration
        steps = int(t_total / dt)
        trajectory = []
        
        segment_duration = t_total / (len(waypoints) - 1)
        segment_steps = max(1, int(segment_duration / dt))
        
        for i in range(len(waypoints) - 1):
            q0 = waypoints[i]
            qf = waypoints[i+1]
            
            for t_idx in range(segment_steps):
                t = t_idx / segment_steps
                # Minimum jerk polynomial: 10t^3 - 15t^4 + 6t^5
                s = 10 * (t ** 3) - 15 * (t ** 4) + 6 * (t ** 5)
                q_t = q0 + (qf - q0) * s
                trajectory.append(q_t)
                
        trajectory.append(waypoints[-1])
        return trajectory

class RoboticAgent:
    """
    Main orchestration class for the H11-ROBOTIC agent.
    Responsible for solving IK, planning paths using RRT, and optimizing trajectories.
    """
    def __init__(self):
        # 3-link planar arm
        self.chain = KinematicChain([1.0, 1.0, 1.0])
        self.ik_solver = InverseKinematicsSolver(self.chain)
        self.planner = RRTPlanner(self.chain, (-np.pi, np.pi))
        
    def execute_task(self, task_config: Dict[str, Any]) -> Dict[str, Any]:
        try:
            action = task_config.get('action_type')
            current_joints = np.array(task_config['current_joints'])
            
            if action == 'reach':
                target_pos = np.array(task_config['target_pose'])[:3]
                obstacles_data = task_config.get('obstacles', [])
                obstacles = [Obstacle(np.array(o['center']), o['radius']) for o in obstacles_data]
                
                # 1. Solve IK for target
                goal_joints, ik_success = self.ik_solver.solve(current_joints, target_pos)
                if not ik_success:
                    return {"success": False, "error": "IK failed to converge"}
                    
                # 2. Plan path
                path = self.planner.plan(current_joints, goal_joints, obstacles)
                if path is None:
                    return {"success": False, "error": "Path planning failed (No collision-free path found)"}
                    
                # 3. Optimize trajectory
                trajectory = TrajectoryOptimizer.generate_minimum_jerk(path, duration=5.0)
                
                return {
                    "success": True,
                    "trajectory": [q.tolist() for q in trajectory],
                    "estimated_duration": 5.0
                }
            else:
                return {"success": False, "error": f"Unsupported action type: {action}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    agent = RoboticAgent()
    req = {
        "action_type": "reach",
        "target_pose": [1.5, 1.5, 0.0, 0, 0, 0],
        "current_joints": [0.0, 0.0, 0.0],
        "obstacles": [
            {"center": [1.0, 0.5, 0.0], "radius": 0.2}
        ]
    }
    res = agent.execute_task(req)
    print(f"Task Result: {res['success']}")
    if res["success"]:
        print(f"Generated trajectory with {len(res['trajectory'])} steps.")
