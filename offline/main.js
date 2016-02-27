var levelsArea = document.getElementById("levelsArea");

var displayLevels = function() {
    var columns = ["Level", "Target", "Cycles", "Excess"];
    var rows = [];
    for(var i=0; i<levels.length; i++) {
        var level = levels[i];
        if(level.cycleBest < Infinity) {
            rows.push([level.name,
                       level.cycleTarget,
                       level.cycleBest,
                       level.cycleExcessPercent + "%"]);
        } else {
            rows.push([level.name,
                       level.cycleTarget,
                       "unsolved",
                       ""]);
        }
    }
    levelsArea.innerHTML = "";
    levelsArea.appendChild(tableCreate(columns, rows));
}

var loadInput = document.getElementById("loadInput");
loadInput.onchange = function() {
    loadFromFile(loadInput.files[0], function(rows) {
        mergeIntoLevels(rows);
        displayLevels();
    });
}

resetLevels();
