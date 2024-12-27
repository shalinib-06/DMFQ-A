1. In this project **DMFQ-A** I have created:

- A scheduling algorithm that incorporates multiple scheduling policies across various 
priority levels. 
- It ensures fairness and prevent starvation by promoting processes to higher-priority queues 
over time. 
- And balances system responsiveness for interactive tasks while managing long-running 
background processes efficiently. 
---
2. Key Concepts:

- ***Multilevel Queues***: Each queue uses a different scheduling algorithm: 
  - *Queue 1*: High priority with Round Robin scheduling. 
  - *Queue 2*: Medium priority with Shortest Remaining Time First (SRTF). 
  - *Queue 3*: Low priority with First-Come-First-Serve (FCFS). 
- ***Aging Mechanism***: Processes that spend a long time in a lower-priority queue are promoted 
to prevent them from being starved by aging threshold.
- ***Preemptive Scheduling***: Higher-priority processes can interrupt lower-priority ones, 
improving system responsiveness. 

