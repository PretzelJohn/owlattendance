
var cols = document.getElementsByName("columns");
var checkboxes = document.getElementById("columns");

function countChecks() {
    "use strict";

    var count = 0;
    for(var i = 0; i < cols.length; i++) {
        if(document.getElementById("columns-"+i).checked) {
            count++;
        }
    }
    return count;
}

function onCheck() {
    "use strict";

    if(countChecks() === 0) {
        checkboxes.classList.add("checkbox-invalid");
    } else {
        checkboxes.classList.remove("checkbox-invalid");
    }
}

(function() {
    "use strict";

    for(var i = 0; i < cols.length; i++) {
        document.getElementById("columns-"+i).addEventListener("change", onCheck);
    }
    onCheck();
})();