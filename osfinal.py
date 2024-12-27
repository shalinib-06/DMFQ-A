from collections import deque

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.waiting = 0
        self.turnaround = 0
        self.completed = False
        self.queue_level = 1  # Start in Queue 1 (high priority)
        self.age_counter = 0  # Aging counter
def gantt_chart(queue1, queue2, queue3, time_quantum, aging_threshold):
    time = 0
    gantt = []
    aging_info = []  # To store the aging information
    processes = sorted(queue1 + queue2 + queue3, key=lambda p: p.arrival)
    queue1, queue2, queue3 = deque(), deque(), deque()

    # Initialize queues based on process levels
    for p in processes:
        if p.queue_level == 1:
            queue1.append(p)
        elif p.queue_level == 2:
            queue2.append(p)
        else:
            queue3.append(p)

    while queue1 or queue2 or queue3:
        if queue1:
            process = queue1.popleft()
            execute_time = min(process.remaining, time_quantum)
        elif queue2:
            queue2 = deque(sorted(queue2, key=lambda x: x.remaining))  # Shortest Remaining Time First (SRTF)
            process = queue2.popleft()
            execute_time = process.remaining
        elif queue3:
            process = queue3.popleft()
            execute_time = process.remaining

        gantt.append((process.pid, time, time + execute_time))
        process.remaining -= execute_time
        time += execute_time

        # Aging logic
        for q in [queue1, queue2, queue3]:
            for proc in q:
                proc.age_counter += execute_time
                if proc.age_counter >= aging_threshold and proc.queue_level > 1:
                    # Log the aging process
                    aging_info.append((proc.pid, time))
                    proc.queue_level -= 1
                    proc.age_counter = 0  # Reset the aging counter

        # Check if the process is completed
        if process.remaining > 0:
            # Increase queue level (lower priority) when it is requeued
            process.queue_level = min(3, process.queue_level + 1)
            if process.queue_level == 1:
                queue1.append(process)
            elif process.queue_level == 2:
                queue2.append(process)
            else:
                queue3.append(process)
        else:
            process.completed = True
            process.turnaround = time - process.arrival
            process.waiting = process.turnaround - process.burst

    return gantt, processes, aging_info

def main():
    num_processes = int(input("Enter the number of processes: "))
    processes = []
    for i in range(num_processes):
        pid = f"P{i+1}"
        arrival = int(input(f"Enter arrival time for {pid}: "))
        burst = int(input(f"Enter burst time for {pid}: "))
        processes.append(Process(pid, arrival, burst))

    time_quantum = int(input("Enter time quantum for round robin (queue 1): "))
    aging_threshold = int(input("Enter aging threshold time: "))

    queue1 = [p for p in processes if p.queue_level == 1]
    queue2 = [p for p in processes if p.queue_level == 2]
    queue3 = [p for p in processes if p.queue_level == 3]

    gantt, final_processes, aging_info = gantt_chart(queue1, queue2, queue3, time_quantum, aging_threshold)

    print("\nGantt Chart:")
    for pid, start, end in gantt:
        print(f"{pid} [{start} - {end}]")

    total_turnaround = sum(p.turnaround for p in final_processes)
    total_waiting = sum(p.waiting for p in final_processes)

    print("\nProcess Information:")
    for p in final_processes:
        print(f"{p.pid}: Turnaround Time = {p.turnaround}, Waiting Time = {p.waiting}")

    print("\nAverage Turnaround Time:", total_turnaround / num_processes)
    print("Average Waiting Time:", total_waiting / num_processes)


if __name__ == "__main__":
    main()
