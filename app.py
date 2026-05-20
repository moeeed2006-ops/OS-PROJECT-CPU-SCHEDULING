from flask import Flask, render_template, request, jsonify
from scheduler import CPUScheduler
import json
import os
import webbrowser
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/schedule', methods=['POST'])
def schedule():
    try:
        data = request.json
        processes = data.get('processes', [])
        algorithm = data.get('algorithm', 'fcfs')
        time_quantum = data.get('time_quantum', 2)
        
        # Validate input
        if not processes:
            return jsonify({'error': 'Please add at least one process'}), 400
        
        # Create scheduler and run algorithm
        scheduler = CPUScheduler(processes)
        
        if algorithm == 'fcfs':
            result = scheduler.fcfs()
        elif algorithm == 'sjf':
            result = scheduler.sjf()
        elif algorithm == 'priority':
            result = scheduler.priority_scheduling()
        elif algorithm == 'round_robin':
            result = scheduler.round_robin(time_quantum)
        else:
            return jsonify({'error': 'Invalid algorithm'}), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare():
    try:
        data = request.json
        processes = data.get('processes', [])
        time_quantum = data.get('time_quantum', 2)
        
        if not processes:
            return jsonify({'error': 'Please add at least one process'}), 400
        
        results = {}
        algorithms = ['fcfs', 'sjf', 'priority', 'round_robin']
        
        for algo in algorithms:
            scheduler = CPUScheduler(processes)
            
            if algo == 'fcfs':
                result = scheduler.fcfs()
            elif algo == 'sjf':
                result = scheduler.sjf()
            elif algo == 'priority':
                result = scheduler.priority_scheduling()
            elif algo == 'round_robin':
                result = scheduler.round_robin(time_quantum)
            
            results[algo] = result
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def open_in_chrome(url):
    chrome_locations = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    chrome_path = next((path for path in chrome_locations if os.path.exists(path)), None)

    if chrome_path:
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open_new(url)
        print(f'Opening in Chrome: {url}')
    else:
        webbrowser.open_new(url)
        print(f'Chrome not found, opening default browser: {url}')

if __name__ == '__main__':
    port = 5000
    url = f'http://127.0.0.1:{port}'
    threading.Timer(1.0, lambda: open_in_chrome(url)).start()
    app.run(debug=True, port=port, use_reloader=False)
