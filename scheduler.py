"""
CPU Scheduling Simulator
Implements: FCFS, SJF, Priority Scheduling, Round Robin
"""

class CPUScheduler:
    def __init__(self, processes):
        """
        Initialize scheduler with list of processes
        Each process: {'pid': 1, 'arrival_time': 0, 'burst_time': 8, 'priority': 2}
        """
        self.processes = self._copy_processes(processes)
        self.execution_order = []
        self.gantt_chart = []
        self.metrics = {}
    
    def _copy_processes(self, processes):
        """Create a deep copy of processes to avoid modifying original"""
        return [p.copy() for p in processes]
    
    def _calculate_metrics(self):
        """Calculate waiting time, turnaround time, and other metrics"""
        total_waiting_time = 0
        total_turnaround_time = 0
        
        for process in self.processes:
            turnaround_time = process.get('completion_time', 0) - process['arrival_time']
            waiting_time = turnaround_time - process['burst_time']
            
            process['turnaround_time'] = turnaround_time
            process['waiting_time'] = max(0, waiting_time)  # Ensure non-negative
            
            total_waiting_time += process['waiting_time']
            total_turnaround_time += turnaround_time
        
        n = len(self.processes)
        self.metrics = {
            'avg_waiting_time': round(total_waiting_time / n, 2),
            'avg_turnaround_time': round(total_turnaround_time / n, 2),
            'total_time': max(p.get('completion_time', 0) for p in self.processes),
            'cpu_utilization': round((sum(p['burst_time'] for p in self.processes) / 
                                      max(p.get('completion_time', 0) for p in self.processes)) * 100, 2) if max(p.get('completion_time', 0) for p in self.processes) > 0 else 0
        }
    
    def fcfs(self):
        """
        First Come First Served Scheduling
        Processes execute in the order they arrive
        """
        self.processes = sorted(self.processes, key=lambda x: x['arrival_time'])
        
        current_time = 0
        self.gantt_chart = []
        
        for process in self.processes:
            # Wait for process to arrive
            if current_time < process['arrival_time']:
                current_time = process['arrival_time']
            
            # Execute process
            start_time = current_time
            current_time += process['burst_time']
            
            process['completion_time'] = current_time
            process['start_time'] = start_time
            
            self.gantt_chart.append({
                'pid': process['pid'],
                'start': start_time,
                'end': current_time,
                'burst_time': process['burst_time']
            })
        
        self._calculate_metrics()
        return self._format_result('FCFS')
    
    def sjf(self):
        """
        Shortest Job First Scheduling
        Non-preemptive: Processes are executed in order of shortest burst time
        """
        current_time = 0
        remaining = self._copy_processes(self.processes)
        self.gantt_chart = []
        
        while remaining:
            # Find available processes (arrived by current_time)
            available = [p for p in remaining if p['arrival_time'] <= current_time]
            
            if not available:
                # Jump to next arrival time
                current_time = min(p['arrival_time'] for p in remaining)
                continue
            
            # Select process with shortest burst time
            process = min(available, key=lambda x: x['burst_time'])
            remaining.remove(process)
            
            start_time = current_time
            current_time += process['burst_time']
            
            process['completion_time'] = current_time
            process['start_time'] = start_time
            
            self.gantt_chart.append({
                'pid': process['pid'],
                'start': start_time,
                'end': current_time,
                'burst_time': process['burst_time']
            })
        
        # Update self.processes with completion times
        for p in remaining:
            for orig_p in self.processes:
                if orig_p['pid'] == p['pid']:
                    orig_p['completion_time'] = p['completion_time']
                    orig_p['start_time'] = p['start_time']
        
        # Fix: Make sure all processes have completion_time
        for p in self.processes:
            for gc in self.gantt_chart:
                if gc['pid'] == p['pid']:
                    p['completion_time'] = gc['end']
                    p['start_time'] = gc['start']
        
        self._calculate_metrics()
        return self._format_result('Shortest Job First (SJF)')
    
    def priority_scheduling(self):
        """
        Priority Scheduling (Non-preemptive)
        Lower priority number = higher priority (execute first)
        """
        current_time = 0
        remaining = self._copy_processes(self.processes)
        self.gantt_chart = []
        
        while remaining:
            # Find available processes
            available = [p for p in remaining if p['arrival_time'] <= current_time]
            
            if not available:
                current_time = min(p['arrival_time'] for p in remaining)
                continue
            
            # Select process with highest priority (lowest number)
            process = min(available, key=lambda x: x.get('priority', 0))
            remaining.remove(process)
            
            start_time = current_time
            current_time += process['burst_time']
            
            process['completion_time'] = current_time
            process['start_time'] = start_time
            
            self.gantt_chart.append({
                'pid': process['pid'],
                'start': start_time,
                'end': current_time,
                'burst_time': process['burst_time'],
                'priority': process.get('priority', 0)
            })
        
        # Update self.processes
        for p in self.processes:
            for gc in self.gantt_chart:
                if gc['pid'] == p['pid']:
                    p['completion_time'] = gc['end']
                    p['start_time'] = gc['start']
        
        self._calculate_metrics()
        return self._format_result('Priority Scheduling')
    
    def round_robin(self, time_quantum=2):
        """
        Round Robin Scheduling (Preemptive)
        Each process gets time_quantum time units to execute
        """
        if time_quantum <= 0:
            time_quantum = 2
        
        current_time = 0
        queue = []
        remaining = self._copy_processes(self.processes)
        self.gantt_chart = []
        processed = set()
        
        # Sort by arrival time
        remaining.sort(key=lambda x: x['arrival_time'])
        
        while queue or remaining:
            # Add newly arrived processes to queue
            arrived = [p for p in remaining if p['arrival_time'] <= current_time and p not in queue]
            queue.extend(arrived)
            
            if not queue:
                if remaining:
                    current_time = remaining[0]['arrival_time']
                    continue
                else:
                    break
            
            # Get first process in queue
            process = queue.pop(0)
            
            # Execute for time_quantum or remaining burst time
            execution_time = min(time_quantum, process.get('remaining_time', process['burst_time']))
            
            start_time = current_time
            current_time += execution_time
            
            self.gantt_chart.append({
                'pid': process['pid'],
                'start': start_time,
                'end': current_time,
                'burst_time': execution_time
            })
            
            # Update remaining time
            if 'remaining_time' not in process:
                process['remaining_time'] = process['burst_time']
            
            process['remaining_time'] -= execution_time
            
            # If process not finished, add back to queue
            if process['remaining_time'] > 0:
                queue.append(process)
            else:
                process['completion_time'] = current_time
                process['start_time'] = process.get('start_time', start_time)
                processed.add(process['pid'])
            
            # Add newly arrived processes to queue
            arrived = [p for p in remaining if p['arrival_time'] <= current_time and p not in queue and p['pid'] not in processed]
            queue.extend(arrived)
        
        # Update self.processes with completion times
        for p in self.processes:
            if p['pid'] in processed:
                # Find the last gantt entry for this process
                entries = [g for g in self.gantt_chart if g['pid'] == p['pid']]
                if entries:
                    p['completion_time'] = entries[-1]['end']
                    p['start_time'] = entries[0]['start']
        
        self._calculate_metrics()
        return self._format_result('Round Robin')
    
    def _format_result(self, algorithm_name):
        """Format the result for API response"""
        return {
            'algorithm': algorithm_name,
            'gantt_chart': self.gantt_chart,
            'processes': [
                {
                    'pid': p['pid'],
                    'arrival_time': p['arrival_time'],
                    'burst_time': p['burst_time'],
                    'priority': p.get('priority', '-'),
                    'start_time': p.get('start_time', 0),
                    'completion_time': p.get('completion_time', 0),
                    'waiting_time': p.get('waiting_time', 0),
                    'turnaround_time': p.get('turnaround_time', 0)
                } for p in sorted(self.processes, key=lambda x: x['pid'])
            ],
            'metrics': self.metrics
        }
