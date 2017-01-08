var levelsArea = document.getElementById("levelsArea");

var displayLevels = function() {
    var columns = ["Level", "Target", "Cycles", "Excess"];
    var rows = [];
    for(var i=0; i<levels.length; i++) {
        var level = levels[i];
        row = [level.number + ": " + level.name,
               level.cycleTarget];
        if(level.cycleBest < Infinity) {
            if(level.cycleBestNew) {
                row.push(level.cycleBest + "*");
            } else {
                row.push(level.cycleBest);
            }
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

var resetButton = document.getElementById("resetButton");
resetButton.onclick = function() {
    resetLevels();
    displayLevels();
}
resetLevels();

var loadInput = document.getElementById("loadInput");
loadInput.onchange = function() {
    loadFromFile(loadInput.files[0], function(rows) {
        mergeIntoLevels(rows);
        displayLevels();
    });
}
