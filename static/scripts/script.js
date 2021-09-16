const burger = document.querySelector(".menu-btn");
const menu = document.querySelector(".buttonCollection");

const bugList = document.querySelectorAll(".label")

burger.addEventListener("click", function(){
    burger.classList.toggle("menu-btn_active");
    menu.classList.toggle("showMenu")
});


for (bug of bugList){
    if (bug.innerHTML === 'High'){
        console.log(bug.innerHTML)
    }
    
}


//-----------Bar Chart JS -------------------------------------------------//

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
//-----------Bar Chart JS -------------------------------------------------//  


