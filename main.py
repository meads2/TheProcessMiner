from flask import Flask, send_file
import pm4py
import pandas as pd
from pathlib import Path

app = Flask(__name__)

def load_data(process):
    df = pd.read_csv('data/process.csv')
    event_log = pm4py.format_dataframe(df, case_id='case_id', activity_key='activity',timestamp_key='timestamp')
    event_log = event_log[event_log['process'] == process]
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_alpha_plus(event_log)
    pm4py.save_vis_petri_net(petri_net, initial_marking, final_marking, 'my-process.png')

@app.route('/')
def index():
    return 'Welcome To Process Miner', 200

@app.route('/<process>')
def proc(process):
    if process is None:
        process = 'online_order'
    
    # Load Process Data
    load_data(process)
    
    return send_file(
        'my-process.png',
        mimetype='image/png',
        attachment_filename='my-process.png',
        cache_timeout=0
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)