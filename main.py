from flask import Flask, send_file, render_template, send_from_directory, url_for
import pm4py
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import boto3
import os

app = Flask(__name__)

def load_data(process):
    df = pd.read_csv('data/process.csv')
    event_log = pm4py.format_dataframe(df, case_id='case_id', activity_key='activity',timestamp_key='timestamp')
    event_log = event_log[event_log['process'] == process]
    petri_net, initial_marking, final_marking = pm4py.discover_petri_net_alpha_plus(event_log)
    pm4py.save_vis_petri_net(petri_net, initial_marking, final_marking, 'my-process.png')
    s3 = boto3.client('s3',
                    region_name='nyc3',
                    endpoint_url='https://nyc3.digitaloceanspaces.com',
                    aws_access_key_id=os.getenv('SPACES_KEY'),
                    aws_secret_access_key=os.getenv('SPACES_SECRET'))
    res = s3.upload_file('my-process.png','process-miner','my-process.png',ExtraArgs={'ACL':'public-read'})
    return 'Success'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<process>')
def proc(process):    
    # Load Process Data
    load_data(process)
    

    return render_template('process.html')

if __name__ == '__main__':
    load_dotenv()
    app.run(host='0.0.0.0', port=5000, debug=False)