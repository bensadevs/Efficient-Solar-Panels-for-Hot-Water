
import pandas as pd
import serial
from flask import Flask, render_template_string, request

app = Flask(__name__)

filename= 'PANELLOG.csv'
# filename = '/Volumes/SOLAR PANEL/LOG.CSV'
recorded_data = pd.read_csv(filename, names=['time', 'voltage', 'current', 'temperature'])

ser = serial.Serial('/dev/ttyUSB0', 9600) # Change to the appropriate port
live_data = pd.DataFrame(columns=['time', 'voltage', 'voltage_control_exp', 'temperature'])

def read_serial_data():
    data = ser.readline().decode().rstrip().split(",")
    if len(data) == 4:
        return {'time': float(data[0]), 'voltage': float(data[1]), 'voltage_control_exp': float(data[2]), 'temperature': float(data[3])}
    return None

def generate_graphs_html(graphs):
	cards = ''
	for i in range(len(graphs)):
		cards += '''
		<div class="card">
			<div class="card-header">
				<h3>'''+graphs[i]['title']+'''</h3>
			</div>
			<div class="card-body">
				<div class="chart-container">
					<canvas class="chart" id="chart_'''+str(i)+'''"></canvas>
				</div>
			</div>
		</div>
		'''
				
	script = '''
	<script>
		graphs = {graphs};
	'''
	script =  script.format(graphs=graphs,qty=len(graphs))

	script += '''
	for (var i = 0; i < graphs.length; i++) {
			var ctx = document.getElementById("chart_"+i).getContext("2d");
			var chart = new Chart(ctx, {
				type: "scatter",
				data: {
					datasets: [{
						label: graphs[i]['title'],
						data: graphs[i]['data'],
						borderColor: 'rgba(255, 255, 255, 0.25)',
						backgroundColor: 'rgba(255, 99, 132, 0.2)',
					}]
				},
				options: {
					scales: {
						xAxes: [{
							type: 'linear',
							position: 'bottom',
							scaleLabel: {
								display: true,
								labelString: graphs[i]['xlabel']
							}
						}],
						yAxes: [{
							type: 'linear',
							position: 'left',
							scaleLabel: {
								display: true,
								labelString: graphs[i]['ylabel']
							}
						}]
					},
					responsive: true,
					legend: {
						labels: {
							fontColor: "#FFFFFF"
						}
					},
					tooltips: {
						callbacks: {
							labelColor: function(tooltipItem, chart) {
								return {
									borderColor: "#FFFFFF",
									backgroundColor: "#FFFFFF"
								};
							}
						}
					}
				}
			});
		}
	</script>
	'''
	return cards, script

def generate_metrics(labels, data, suffix):
	card = '''
	<div class="card">
		<div class="card-header">
			<h3>{titles[0]}</h3>
		</div>
		<div class="card-body">
			<div class="row">
				<div class="column-2">
					<h4>{titles[1]}</h4>
					<p>{data[0]}{suffix[0]}</p>
				</div>
				<div class="column-2">
					<h4>{titles[2]}</h4>
					<p>{data[1]}{suffix[1]}</p>
				</div>
				<div class="column-2">
					<h4>{titles[3]} </h4>
					<p>{data[2]}{suffix[2]}</p>
				</div>
			</div>
		</div>
	</div>
	'''
	return card.format(titles = labels, data = data , suffix = suffix )
	# return ["Panel "+str(i+1) + ": Generated " +str(power_generated[i]) +"W today. Cost: "+"${:.2f}".format(cost[i]) for i in range(0,len(power_generated))]



@app.route('/')
def display_page():
	
	# RUNS
	StartTimes= [0,5500,12100]
	EndTimes = [5000,10000,18000]


	# get url parameters
	run = int(request.args.get('run', 0))
	if run == -1:
		df = live_data
		a = 0
		b = len(df)
	else:
		df = recorded_data
		a = StartTimes[run-1]
		b = EndTimes[run-1]
	

	if live_data:
		data = read_serial_data()
		live_data = df.append(data, ignore_index=True)
		live_data.to_csv('live_data.csv', index=False)

	#energy is integrate voltage over time
	solar = round(sum(df['voltage'][a:b])/(b-a)*1.93,2)
	pump = round(24*(b-a)/3600,2)
	net = round(solar-pump,2)


	graph_data = [{
		'title': 'Temperature vs Time',
		'xlabel': 'Time (s)',
		'ylabel': 'Temperature (C)',
		'data': [{'x': df['time'][i], 'y': df['temperature'][i]} for i in range(a,b)]
	},	{
		'title': 'Voltage vs Time (Heated)',
		'xlabel': 'Time (s)',
		'ylabel': 'Voltage (V)',
		'data': [{'x': df['time'][i], 'y': df['voltage'][i]} for i in range(a,b)]
	}]
	
	if run == 0:
		graph_data.append({	
		'title': 'Voltage vs Time (Unheated)',
		'xlabel': 'Time (s)',
		'ylabel': 'Voltage (V)',
		'data': [{'x': df['time'][i], 'y': df['voltage_control_exp'][i]} for i in range(a,b)]
	})
	else:
		graph_data.append({	
		'title': 'Temperature vs Voltage',
		'xlabel': 'Temperature (C)',
		'ylabel': 'Voltage (V)',
		'data': [{'x': df['temperature'][i], 'y': df['voltage'][i]} for i in range(a,b)]
	})

	
	graphs, script = generate_graphs_html(graph_data)

	metriclabels = ['Metrics','Energy Generated <br> </br>','Pump Power Consumption' ,'Net Energy <br> </br>']
	metrics = generate_metrics(metriclabels, [solar,pump,net],[' Wh', ' Wh',' Wh'])
	
	kpilabels = ['Cooling System KPIs', 'Temperature Outside','Water Tank Temperature','Solar Panel Temperature']
	kpis = generate_metrics(kpilabels, [20,38,df['temperature'][b]] ,['º', 'º','º'])


	dashboard_string = '''
<!DOCTYPE html>
<html>
<head>
	<title>Solar Power Dashboard</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
	<style type="text/css">
		body {
			background-color: #373E4C;
			color: #FFFFFF;
			font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
			font-size: 14px;
			line-height: 1.42857143;
			margin: 0;
			padding: 0;
		}
		.jumbotron {
			background-color: #373E4C;
			border-radius: 0;
			margin-bottom: 0;
			padding: 2rem;
			text-align: center;
		}
		.jumbotron h1 {
			font-size: 3rem;
			margin-bottom: 0;
		}
		.jumbotron p {
			font-size: 1.5rem;
			margin-bottom: 0;
		}
		.container {
			padding: 0;
			display: flex;
			flex-wrap: wrap;
			align-items: flex-start;
		}
		.column{
			flex: 1;
			align-self: flex-start;
			position: relative;
			max-width: 800px;
		}
		.row {
			padding: 0;
			display: flex;
			flex-wrap: wrap;
			align-items: flex-start;
		}
		.row h4 {
			font-size: 1.5rem;
		}
		.column-2{
			flex: 1;
			align-self: flex-start;
			position: relative;
			max-width: 400px;
			text-align: center;
		}

		.card {
			background-color: #373E4C;
			border: none;
			padding: 1rem;
		}
		.card-header {
			background-color: #282C35;
			border-radius: 5px;
			padding: .75rem 1.25rem;
		}
		.card-header h3 {
			color: #FFFFFF;
			font-size: 1.25rem;
			margin: 0;
		}
		.chart-container {
			position: relative;
			margin: auto;
			height: 40vh;
			min-height: 300px;
			width: 70vw;
			max-width: 600px;
		}
		.chart {
			height: 100%;
			width: 100%;
		}
		.button {
			flex: 1;
			margin: 0px 30px 0px 30px;
			background-color: #282C35;
			border: none;
			color: white;
			padding: 15px 32px;
			text-align: center;
			border-radius: 5px;
			font-size: 1rem;
			font-weight: bold;
		}
		@media (max-width: 767px) {
			.chart-container {
				height: 60vh;
				width: 90vw;
			}
		}
	</style>
</head>
<body>
	<div class="jumbotron">
		<h1>Solar Power Dashboard</h1>
		<p>Real-time solar power output tracking</p>
	</div>
	<div class="row" style="margin: 0px 300px 20px 300px ">
				<button class ="button" onclick="window.location.href = '/?run=1';">Run 1</button>
				<button class ="button" onclick="window.location.href = '/?run=2';">Run 2</button>
				<button class ="button" onclick="window.location.href = '/?run=3';">Run 3</button>
				<button class ="button" onclick="window.location.href = '/?run=-1';">Live Data</button>
	</div>
	<div class="container">
		<div class="column" >
			
			{{graphs | safe}}
		</div>
		<div class="column">
			{{metrics | safe}}
			{{kpis | safe}}
			</div>
		</div>
	</div>	
	{{script | safe}}
</body>
</html>
'''

	return render_template_string(dashboard_string, graphs=graphs, script = script, metrics = metrics, kpis = kpis)

if __name__ == '__main__':
	app.run(debug=True)
