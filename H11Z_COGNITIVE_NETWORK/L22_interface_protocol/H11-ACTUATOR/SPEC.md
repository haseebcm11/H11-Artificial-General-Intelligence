# H11-ACTUATOR Specification

## Overview
The H11-ACTUATOR agent governs the lowest level of physical interaction, managing diverse types of actuators including servo motors, stepper motors, and soft/pneumatic actuators. It acts as the bridge between high-level trajectories and low-level physical forces, ensuring safety, compliance, and precise tracking.

## Core Responsibilities
1.  **Low-Level Control Loops**: Implementing Field-Oriented Control (FOC), PID, and impedance control loops to accurately track position, velocity, and torque setpoints.
2.  **Safety Enforcement**: Enforcing strict thermal, velocity, position, and torque limits to protect both the hardware and the environment.
3.  **Actuator Calibration**: Performing automated calibration routines (e.g., finding zero indexes, measuring friction, system identification) upon startup.
4.  **Compliance and Soft Robotics**: Managing variable stiffness and compliance for soft actuators, enabling safe human-robot interaction and adaptable manipulation.

## Technical Mechanisms
-   **Impedance Control**: Regulating the dynamic relationship between position and force at the actuator level to achieve desired stiffness and damping properties.
-   **Feedforward Compensation**: Using dynamic models (gravity, Coriolis, friction) to generate feedforward torques, reducing the burden on feedback controllers and improving tracking bandwidth.
-   **Thermal Management**: Estimating coil temperatures using observer models and automatically derating maximum torque limits to prevent overheating.
-   **Anti-Windup**: Implementing advanced anti-windup strategies in PI/PID controllers to prevent saturation-induced instability during aggressive maneuvers.
