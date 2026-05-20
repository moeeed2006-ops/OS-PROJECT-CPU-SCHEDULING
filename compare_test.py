from app import app

with app.test_client() as client:
    resp = client.post('/api/compare', json={
        'processes': [
            {'pid': 1, 'arrival_time': 0, 'burst_time': 5, 'priority': 1},
            {'pid': 2, 'arrival_time': 1, 'burst_time': 3, 'priority': 2}
        ],
        'time_quantum': 2
    })
    print('status', resp.status_code)
    print(resp.get_data(as_text=True))
