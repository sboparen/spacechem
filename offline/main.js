var levelsArea = document.getElementById("levelsArea");

var displayLevels = function() {
    var columns = ["Level", "Target", "Cycles", "Excess"];
    var rows = [];
    for(var i=0; i<levels.length; i++) {
        var level = levels[i];
        row = [level.number + ": " + level.name,
               level.cycleTarget];
        if(level.cycleBest < Infinity) {
            row.push(level.cycleBest);
            row.push(level.cycleExcessPercent + "%");
        } else {
            row.push("unsolved");
            row.push("");
        }
        rows.push(row);
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
