
var filterBy = document.getElementById("filterBy");
var filterByRank = document.getElementById("filterByRank");
var filterByMajor = document.getElementById("filterByMajor");
var filterByDepartment = document.getElementById("filterByDepartment");

function update() {
    "use strict";
    if(filterBy.value === "") {
        filterBy.style.marginBottom = "10px";
        filterBy.style.borderBottomLeftRadius = "5px";
        filterBy.style.borderBottomRightRadius = "5px";
        filterByRank.parentElement.style.display = "none";
        filterByMajor.parentElement.style.display = "none";
        filterByDepartment.parentElement.style.display = "none";
    } else {
        filterBy.style.marginBottom = "-1px";
        filterBy.style.borderBottomLeftRadius = "0";
        filterBy.style.borderBottomRightRadius = "0";
        if(filterBy.value === "ClassRank") {
            filterByRank.parentElement.style.display = "inherit";
            filterByMajor.parentElement.style.display = "none";
            filterByDepartment.parentElement.style.display = "none";
        } else if(filterBy.value === "MajorName") {
            filterByRank.parentElement.style.display = "none";
            filterByMajor.parentElement.style.display = "inherit";
            filterByDepartment.parentElement.style.display = "none";
        } else if(filterBy.value === "Department") {
            filterByRank.parentElement.style.display = "none";
            filterByMajor.parentElement.style.display = "none";
            filterByDepartment.parentElement.style.display = "inherit";
        }
    }
}


filterBy.addEventListener("change", update);
update();