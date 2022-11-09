

const rb = JSON.parse(document.getElementById('redBugs').textContent);
const yb = JSON.parse(document.getElementById('yellowBugs').textContent);
const gb = JSON.parse(document.getElementById('greenBugs').textContent);


const data = {
    labels: [
      'High',
      'Medium',
      'Low'
    ],
    datasets: [{
      label: 'My First Dataset',
      data: [rb, yb, gb],
      backgroundColor: [
        '#303030',
        '#3b3b3b',
        '#484848'
      ],
      hoverOffset: 10,
      borderColor: ['#071a1f', '#071a1f', '#071a1f '],
      borderWidth: 1
    }]
  };


const config = {
    type: 'doughnut',
    data: data,
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
              display: false
            }
          },
          layout: {
            padding: {
                // Any unspecified dimensions are assumed to be 0                     
                top: 5,
                bottom: 5,
                left: 5,
                right: 5,
            }
        }
        }

  };

const cb = JSON.parse(document.getElementById('completedBugs').textContent);
const ob = JSON.parse(document.getElementById('uncompleteBugs').textContent);
const ub = JSON.parse(document.getElementById('totalBugs').textContent);
  const data2 = {
    labels: [
      'Closed',
      'Open',
    ],
    datasets: [{
      label: 'Bugs',
      data: [cb, ob, ub],
      backgroundColor: [
        '#333232',
        '#333232',
        '#333232  '
      ],
      hoverOffset: 5,
      borderColor: ['#073b42', '#073b42', '#073b42 '],
      borderWidth: 2
    }]
  };


  const config2 = {
    type: 'bar',
    data: data2,
    options: {
         maintainAspectRatio: false,
        plugins: {
            legend: {
              display: false
            }
          },
        scales: {
            x: {
              title: {
                display: false,
                text: 'Number'
              }
            },
            y: {
              title: {
                display: false,
                text: 'Value'
              },
              min: 0,
              max: cb.int,
              ticks: {
                suggestedMin: -10,    // minimum will be 0, unless there is a lower value.
                // OR //
                //beginAtZero: true   // minimum value will be 0.
                steps: 20,
                stepValue: 1,
                }

            }
        }
    },
  };
  

  const myChart = new Chart(document.getElementById('myChart'),config);






  const myChart2 = new Chart(document.getElementById('myChart2'),config2);


  console.log('helloworld') 