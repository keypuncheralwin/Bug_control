
//-----------Bar Chart JS -------------------------------------------------//
//----Some elements taken from--- https://codepen.io/chartjs/pen/YVWZbz ---//


let bug_count = JSON.parse(document.getElementById("bug_count").textContent)

let user = []
let count = []
for( bug of bug_count){
    user.push(bug[0])
    count.push(bug[1])

}



var data = {
    labels: user,
    datasets: [{
      label: "Amount of bugs reported",
      color: "white",
      backgroundColor: "rgba(255,99,132,0.2)",
      borderColor: "rgba(255,99,132,1)",
      borderWidth: 2,
      hoverBackgroundColor: "rgba(255,99,132,0.4)",
      hoverBorderColor: "rgba(255,99,132,1)",
      data: count,
    }]
  };
  
  var options = {
    maintainAspectRatio: false,
    plugins: {
      responsive: true,
        legend: {
            labels: {
                color: "white",
                // This more specific font property overrides the global property
                font: {
                    size: 14
                }
            }
        }
    },
    scales: {
      y: {
        stacked: true,
        ticks: {
            color: "white"
          },
        grid: {
          display: true,
          color: "rgba(255,99,132,0.2)"
        }
      },
      x: {
        ticks: {
            color: "white"
          },
        grid: {
          display: false
        }
      }
    }
  };
  
  new Chart('chart', {
    type: 'bar',
    options: options,
    data: data
  });

//-----------Doughnut Chart JS -------------------------------------------------//  

let priority_count = JSON.parse(document.getElementById("priority_count").textContent)
console.log(priority_count)

var ctx = document.getElementById("chart2").getContext('2d');

var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ["Low",	"Moderate",	"High"],
        datasets: [{    
            data: priority_count, // Specify the data values array
          
            borderColor: ['#135390', '#D1913E', '#A92420'], // Add custom color border 
            backgroundColor: ['#135390', '#D1913E', '#A92420'], // Add custom color background (Points and Fill)

            borderWidth: 1 // Specify bar border width
        }]},         
    options: {
      responsive: true, // Instruct chart js to respond nicely.
      maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height 
      
    }
});

