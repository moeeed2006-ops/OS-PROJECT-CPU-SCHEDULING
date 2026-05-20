// Global processes array
let processes = [];
let currentResult = null;

// Add a new process
function addProcess() {
    const pid = parseInt(document.getElementById('pid').value);
    const arrival = parseInt(document.getElementById('arrival').value);
    const burst = parseInt(document.getElementById('burst').value);
    const priority = parseInt(document.getElementById('priority').value);

    // Validation
    if (!pid || pid <= 0) {
        showError('Please enter a valid Process ID');
        return;
    }
    if (arrival < 0) {
        showError('Arrival time cannot be negative');
        return;
    }
    if (!burst || burst <= 0) {
        showError('Please enter a valid Burst Time');
        return;
    }

    // Check for duplicate PID
    if (processes.some(p => p.pid === pid)) {
        showError('Process ID already exists');
        return;
    }

    // Add process
    const process = {
        pid: pid,
        arrival_time: arrival,
        burst_time: burst,
        priority: priority
    };

    processes.push(process);
    clearInputs();
    updateProcessList();
    showSuccess('Process added successfully!');
}

// Update process list display
function updateProcessList() {
    const listDiv = document.getElementById('processList');

    if (processes.length === 0) {
        listDiv.innerHTML = '<p class="empty-state">No processes added yet</p>';
        return;
    }

    listDiv.innerHTML = processes
        .sort((a, b) => a.pid - b.pid)
        .map(p => `
            <div class="process-item">
                <div class="process-item-info">
                    <p><strong>P${p.pid}</strong> | AT: ${p.arrival_time} | BT: ${p.burst_time} | Priority: ${p.priority}</p>
                </div>
                <button class="btn-remove" onclick="removeProcess(${p.pid})">Remove</button>
            </div>
        `)
        .join('');
}

// Remove a process
function removeProcess(pid) {
    processes = processes.filter(p => p.pid !== pid);
    updateProcessList();
    showSuccess('Process removed!');
}

// Clear all processes
function clearAll() {
    if (processes.length === 0) {
        showError('No processes to clear');
        return;
    }
    if (confirm('Are you sure you want to clear all processes?')) {
        processes = [];
        updateProcessList();
        document.getElementById('ganttChart').innerHTML = '<p class="empty-state">Run scheduler to see Gantt chart</p>';
        document.getElementById('metrics').innerHTML = '<p class="empty-state">Run scheduler to see metrics</p>';
        document.getElementById('tableContainer').innerHTML = '<p class="empty-state">Run scheduler to see process details</p>';
        showSuccess('All processes cleared!');
    }
}

// Clear input fields
function clearInputs() {
    document.getElementById('pid').value = '';
    document.getElementById('arrival').value = '';
    document.getElementById('burst').value = '';
    document.getElementById('priority').value = '';
}

// Run selected scheduler
async function runScheduler() {
    if (processes.length === 0) {
        showError('Please add at least one process');
        return;
    }

    const algorithm = document.getElementById('algorithm').value;
    const timeQuantum = parseInt(document.getElementById('timeQuantum').value) || 2;

    try {
        const response = await fetch('/api/schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                processes: processes,
                algorithm: algorithm,
                time_quantum: timeQuantum
            })
        });

        if (!response.ok) {
            const error = await response.json();
            showError(error.error || 'Error running scheduler');
            return;
        }

        const result = await response.json();
        currentResult = result;

        displayGanttChart(result);
        displayMetrics(result);
        displayProcessTable(result);
        document.getElementById('comparisonSection').style.display = 'none';

        showSuccess(`${result.algorithm} executed successfully!`);
    } catch (error) {
        showError('Error: ' + error.message);
    }
}

// Display Gantt Chart
function displayGanttChart(result) {
    const ganttDiv = document.getElementById('ganttChart');

    if (!result.gantt_chart || result.gantt_chart.length === 0) {
        ganttDiv.innerHTML = '<p class="empty-state">No execution data</p>';
        return;
    }

    const maxTime = Math.max(...result.gantt_chart.map(g => g.end));
    const totalTime = maxTime || 1;

    let html = '<div class="gantt-container">';
    html += '<div class="gantt-bar-row">';

    result.gantt_chart.forEach(item => {
        const width = ((item.end - item.start) / totalTime) * 100;
        const left = (item.start / totalTime) * 100;
        const colorClass = `p${item.pid % 10}`;

        html += `
            <div class="gantt-bar ${colorClass}" style="width: ${width}%; left: ${left}%;" 
                 title="P${item.pid}: ${item.start}-${item.end} (${item.burst_time}ms)">
                <span>P${item.pid}</span>
            </div>
        `;
    });

    html += '</div>';
    html += '<div class="gantt-labels">';
    html += `<div class="gantt-label">0</div>`;
    html += `<div class="gantt-label">${maxTime}</div>`;
    html += '</div>';
    html += '</div>';

    ganttDiv.innerHTML = html;
}

// Display Metrics
function displayMetrics(result) {
    const metricsDiv = document.getElementById('metrics');

    if (!result.metrics) {
        metricsDiv.innerHTML = '<p class="empty-state">No metrics data</p>';
        return;
    }

    const metrics = result.metrics;

    let html = `
        <div class="metric-card waiting">
            <h4>Avg Waiting Time</h4>
            <div class="value">${metrics.avg_waiting_time}</div>
            <p>ms</p>
        </div>
        <div class="metric-card turnaround">
            <h4>Avg Turnaround Time</h4>
            <div class="value">${metrics.avg_turnaround_time}</div>
            <p>ms</p>
        </div>
        <div class="metric-card total">
            <h4>Total Time</h4>
            <div class="value">${metrics.total_time}</div>
            <p>ms</p>
        </div>
        <div class="metric-card utilization">
            <h4>CPU Utilization</h4>
            <div class="value">${metrics.cpu_utilization}%</div>
        </div>
    `;

    metricsDiv.innerHTML = html;
}

// Display Process Table
function displayProcessTable(result) {
    const tableContainer = document.getElementById('tableContainer');

    if (!result.processes || result.processes.length === 0) {
        tableContainer.innerHTML = '<p class="empty-state">No process data</p>';
        return;
    }

    let html = `
        <table>
            <tr>
                <th>PID</th>
                <th>AT</th>
                <th>BT</th>
                <th>Priority</th>
                <th>ST</th>
                <th>CT</th>
                <th>WT</th>
                <th>TT</th>
            </tr>
    `;

    result.processes.forEach(p => {
        html += `
            <tr>
                <td>P${p.pid}</td>
                <td>${p.arrival_time}</td>
                <td>${p.burst_time}</td>
                <td>${p.priority}</td>
                <td>${p.start_time}</td>
                <td>${p.completion_time}</td>
                <td>${p.waiting_time}</td>
                <td>${p.turnaround_time}</td>
            </tr>
        `;
    });

    html += '</table>';
    tableContainer.innerHTML = html;
}


    const waitingTimes = algorithms.map(algo => results[algo].metrics.avg_waiting_time);
    const turnaroundTimes = algorithms.map(algo => results[algo].metrics.avg_turnaround_time);
    const utilization = algorithms.map(algo => results[algo].metrics.cpu_utilization);

    const canvas = document.getElementById('comparisonCanvas');

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = '❌ ' + message;
    
    const container = document.querySelector('.main-content') || document.body;
    container.insertBefore(errorDiv, container.firstChild);

    setTimeout(() => errorDiv.remove(), 4000);
}

// Show success message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = '✅ ' + message;
    
    const container = document.querySelector('.main-content') || document.body;
    container.insertBefore(successDiv, container.firstChild);

    setTimeout(() => successDiv.remove(), 3000);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('CPU Scheduler Simulator loaded!');
});
