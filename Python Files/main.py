
import pandas as pd
from flask import Flask, render_template_string

app = Flask(__name__)

filename= 'PANELLOG.csv'
# filename = '/Volumes/SOLAR PANEL/LOG.CSV'
df = pd.read_csv(filename, names=['time', 'voltage', 'current', 'temperature'])
# print(df)

def generate_graphs_html(titles, xlabels, ylabels, xdatas, ydatas):
	cards = ''
	for i in range(len(titles)):
		cards += '''
		<div class="card">
			<div class="card-header">
				<h3>'''+titles[i]+'''</h3>
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
		titles = {titles};
		xlabels = {xlabels};
		ylabels = {ylabels};
		xdatas = {xdatas};
		ydatas = {ydatas};
	'''
	script =  script.format(titles=titles,xlabels=xlabels,ylabels=ylabels,xdatas=xdatas,ydatas=ydatas,qty=len(titles))

	script += '''
	for (var i = 0; i < titles.length; i++) {
			var ctx = document.getElementById("chart_"+i).getContext("2d");
			console.log(titles);
			console.log(xlabels);
			console.log(ylabels);
			var chart = new Chart(ctx, {
				type: "line",
				data: {
					labels: xdatas[i],
					datasets: [{
						label: titles[i],
						data: ydatas[i],
						fill: false,
						borderColor: "#FFFFFF",
						pointBackgroundColor: "#FFFFFF"
					}]
				},
				options: {
					responsive: true,
					maintainAspectRatio: false,
					scales: {
						yAxes: [{
							ticks: {
								beginAtZero: true,
								fontColor: "#FFFFFF"
							},
							gridLines: {
								color: "rgba(255, 255, 255, 0.1)",
								zeroLineColor: "rgba(255, 255, 255, 0.1)"
							}
						}],
						xAxes: [{
							ticks: {
								fontColor: "#FFFFFF"
							},
							gridLines: {
								color: "rgba(255, 255, 255, 0.1)"
							}
						}]
					},
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
	graphlabels = [
		'Temperature vs Time', 
		'Voltage vs Time', 
		'Current vs Time'
	]
	xlabels = [
		'Time (s)',
		'Time (s)',
		'Time (s)'
	]
	ylabels = [
		'Temperature (C)',
		'Voltage (V)',
		'Current (A)'
	]
	graphs_data = [
		[df['time'], df['temperature']],
		[df['time'], df['voltage']],
		[df['temperature'], df['voltage']]
	]
	xdatas = [list(graphs_data[i][0])[6000:15000] for i in range(0,len(graphs_data))]
	ydatas = [list(graphs_data[i][1])[6000:15000] for i in range(0,len(graphs_data))]

	graphs, script = generate_graphs_html(graphlabels,xlabels,ylabels,xdatas,ydatas)

	metriclabels = ['Metrics','Total Power Generated','Heat Pump Power Consumption','Cost Savings <br> </br>']
	metrics = generate_metrics(metriclabels, [20,30,50],[' MWh', ' MWh','%'])
	
	kpilabels = ['Cooling System KPIs', 'Temperature Outside','Water Tank Temperature','Solar Panel Temperature']
	kpis = generate_metrics(kpilabels, [30,20,25] ,['º', 'º','º'])


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
