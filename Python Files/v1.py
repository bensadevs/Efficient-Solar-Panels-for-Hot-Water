import base64
import matplotlib
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template_string

app = Flask(__name__)
matplotlib.use('Agg')

df = pd.read_csv('log.csv', names=['time', 'voltage', 'current', 'temperature'])

def generate_graph_html(title, xlabel, ylabel, xdata, ydata):
    fig, ax = plt.subplots()
    ax.plot(xdata, ydata)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_string = base64.b64encode(buffer.getvalue()).decode()
    html = '''
    <div class="graph-container">
        <h3>{title}</h3>
        <img src="data:image/png;base64,{image_string}">
    </div>
    '''
    return html.format(title=title, image_string=image_string)

@app.route('/')
def display_page():
    graphs_html = [
        generate_graph_html('Voltage vs Time', 'Time (s)', 'Voltage (V)', df['time'], df['voltage']),
        generate_graph_html('Current vs Time', 'Time (s)', 'Current (A)', df['time'], df['current']),
        generate_graph_html('Temperature vs Time', 'Time (s)', 'Temperature (C)', df['time'], df['temperature'])
    ]

    template_string = '''
    <html>
    <head>
        <title>Measurement Data</title>
        <style>
            .graph-container {
                display: inline-block;
                width: 49%;
                margin: 1%;
            }
        </style>
    </head>
    <body>
        <h1>Measurement Data</h1>
        {{ graphs_html|safe }}
    </body>
    </html>
    '''
    return render_template_string(template_string, graphs_html=''.join(graphs_html))

if __name__ == '__main__':
    app.run(debug=True)
