import base64
import matplotlib
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template_string

app = Flask(__name__)

matplotlib.use('Agg')
filename= 'PANELLOG.csv'
# filename = '/Volumes/SOLAR PANEL/LOG.CSV'
df = pd.read_csv(filename, names=['time', 'voltage', 'current', 'temperature'])
print(df)

def generate_graph_html(title, xlabel, ylabel, xdata, ydata):
    fig, ax = plt.subplots()
    ax.plot(xdata, ydata)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue()).decode()

    html = '''
    <div class="graph-container">
        <h3>{title}</h3>
        <img src="data:image/png;base64,{encoded_image}">
    </div>
    '''
    return html.format(title=title, encoded_image=encoded_image)

def panel_summary(power_generated, cost):
    return ["Panel "+str(i+1) + ": Generated " +str(power_generated[i]) +"W today. Cost: "+"${:.2f}".format(cost[i]) for i in range(0,len(power_generated))]


@app.route('/')
def display_page():
    graphs_html = [
        generate_graph_html('Temperature vs Time', 'Time (s)', 'Temperature (C)', df['time'], df['temperature']),
        generate_graph_html('Voltage vs Time', 'Time (s)', 'Voltage (V)', df['time'], df['voltage']),
        generate_graph_html('Current vs Time', 'Time (s)', 'Current (A)', df['time'], df['current'])
    ]
    panel_list = panel_summary([200,300,100],[20,30,10])
    
    boston_temp = 45

    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        /* Set the background color */
        .main {
        display: flex;
        flex-direction: row;
        justify-content: center;
        height: 100%
        align-items: center;
        background-color: #494949;
        transition: box-shadow 0.3s ease-in-out;
        }

        .right-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 500px;
        width: 50%;
        margin: 20px;
        background-color: #A9A9A9;
        transition: box-shadow 0.3s ease-in-out;
        }
        .right-container:hover {
        box-shadow: 3px 3px #333;
        }

        .left-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 1600px;
        width: 50%;
        margin: 20px;
        background-color: #A9A9A9;
        transition: box-shadow 0.3s ease-in-out;
        }
        .graph-container:hover {
        box-shadow: 8px 8px #333;
        }
        .panel-list-container {
        width: 100%;
        height: 50%;
        border: 1px solid black;
        display: inline-block;
        margin-bottom: 20px;
        padding: 10px;
        background-color: #fff;
        }

        .weather-container {
        width: 100%;
        height: 50%;
        border: 1px solid black;
        display: inline-block;
        font-size: 20px;
        background-color: #fff;
        }
    </style>
    </head>
    <body>
    <div class="main">
        <div class="left-container">
                <div class="graphs">
                {{graphs | safe}}
                </div>
        </div>
        <div class="right-container">
            <div class="panel-list-container">
                Solar Panel List
                <br>
                {{panel_data | safe}}
            </div>
            <div class="weather-container">
                Weather in Boston, MA: {{temp}}º F and Sunny
            </div>
        </div>
    </div>
    </div>
    </div>
    </body>
    </html>

    '''
    return render_template_string(html_template, graphs=''.join(graphs_html),temp = boston_temp, panel_data = '<br></br>'.join(panel_list))

if __name__ == '__main__':
    app.run(debug=True)
