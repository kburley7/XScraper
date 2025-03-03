// 1) Load Google Charts 'corechart' package
google.charts.load('current', { packages: ['corechart'] });

// 2) Once loaded, call our initialize function
google.charts.setOnLoadCallback(initialize);

function initialize() {
  // Fetch the data from our JSON file (data.json)
  fetch('tweets.json')
    .then(response => response.json())
    .then(jsonData => {
      // Once data is loaded, convert it and draw the chart
      drawChart(jsonData);
    })
    .catch(error => {
      console.error('Error fetching JSON data:', error);
    });
}

function drawChart(jsonData) {
  // 3) Convert JSON data to an array format accepted by Google Charts

  // Build the header row (column labels).
  // First column is 'Timestamp', followed by each attribute we want to plot.
  const chartData = [
    ['Timestamp', '3WR', '4WR', 'CM', 'SPIN', 'WO']
  ];

  // Loop through each JSON object, pushing rows of data:
  // [Timestamp (as a Date), 3WR, 4WR, CM, SPIN, WO]
  jsonData.forEach(item => {
    chartData.push([
      // Convert the timestamp string to a Date
      new Date(item.timestamp),
      item['3WR'],
      item['4WR'],
      item['CM'],
      item['SPIN'],
      item['WO']
    ]);
  });

  // Convert the array to DataTable
  const data = google.visualization.arrayToDataTable(chartData);

  // 4) Define options for the line chart
  const options = {
    title: 'UWO Rec - Sample Counts Over Time',
    curveType: 'function',            // Smooth the lines (optional)
    legend: { position: 'bottom' },
    hAxis: {
      title: 'Time',
      format: 'MMM dd, HH:mm',        // Example date/time format
      gridlines: { count: 5 }
    },
    vAxis: {
      title: 'Count',
      minValue: 0
    }
  };

  // Create and draw the LineChart
  const chart = new google.visualization.LineChart(document.getElementById('myChart'));
  chart.draw(data, options);
}
