const burger = document.querySelector(".menu-btn");
const menu = document.querySelector(".buttonCollection");

const priorityList = document.querySelectorAll(".priority")

//toggle mobile menu on/off

burger.addEventListener("click", function(){
    burger.classList.toggle("menu-btn_active");
    menu.classList.toggle("showMenu")
});


//highlighting priority status with the appropriate color

for (priority of priorityList){
    if (priority.innerHTML === 'High'){
        console.log(priority.innerHTML)
        priority.classList.add("highColor")
    }
    if (priority.innerHTML === 'Moderate'){
        console.log(priority.innerHTML)
        priority.classList.add("moderateColor")
    }
    if (priority.innerHTML === 'low'){
        console.log(priority.innerHTML)
        priority.classList.add("lowColor")
    }
    
}
