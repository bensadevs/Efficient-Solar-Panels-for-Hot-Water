import base64
import matplotlib
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template_string

app = Flask(__name__)
matplotlib.use('Agg')

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('log.csv', names=['time', 'voltage', 'current', 'temperature'])

def generate_graph_html(title, xlabel, ylabel, xdata, ydata):
    fig, ax = plt.subplots()
    ax.plot(xdata, ydata)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Save the graph as a PNG image and encode it as a Base64 string
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_string = base64.b64encode(buffer.getvalue()).decode()

    # Generate the HTML code for the graph
    html = '''
    <div class="graph-container">
        <h3>{title}</h3>
        <img src="data:image/png;base64,{image_string}">
    </div>
    '''
    return html.format(title=title, image_string=image_string)

def panel_summary(power_generated, cost):
    return ["Panel "+str(i+1) + ": Generated" +str(power_generated[i]) +"W today. Cost: "+"${:.2f}".format(cost[i]) for i in range(0,len(power_generated))]

# Define a Flask route to display the webpage
@app.route('/')
def display_page():
    # Generate the HTML code for each graph
    graphs_html = [
        generate_graph_html('Temperature vs Time', 'Time (s)', 'Temperature (C)', df['time'], df['temperature']),
        generate_graph_html('Voltage vs Time', 'Time (s)', 'Voltage (V)', df['time'], df['voltage']),
        generate_graph_html('Current vs Time', 'Time (s)', 'Current (A)', df['time'], df['current'])
    ]

    panel_list = panel_summary([200,300,100],[20,30,10])
    print(panel_list)
    
    boston_temp = 45

    template_string = '''
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
        /* Add a hover effect */
        transition: box-shadow 0.3s ease-in-out;
        }

        /* Styles for the graph and list on the right */
        .right-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 500px;
        width: 50%;
        margin: 20px;
        background-color: #A9A9A9;
        /* Add a hover effect */
        transition: box-shadow 0.3s ease-in-out;
        }
        .right-container:hover {
        box-shadow: 3px 3px #333;
        }

        /* Styles for the list and weather on the left */
        .left-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 1600px;
        width: 50%;
        margin: 20px;
        background-color: #A9A9A9;
        /* Add a hover effect */
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

        /* Styles for the rectangle on the bottom left */
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
    return render_template_string(template_string, graphs=''.join(graphs_html),temp = boston_temp, panel_data = '<br></br>'.join(panel_list))

if __name__ == '__main__':
    app.run(debug=True)
