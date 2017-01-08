resetLevels = function() {
    levels = levelData.slice();
    levelById = {}
    for(var i=0; i<levels.length; i++) {
        levels[i].cycleBest = Infinity;
        levelById[levels[i].id] = levels[i];
    }
}

var excessPercent = function(best, target) {
    var value = 100 * (best - target) / target;
    return (value > 0) ? Math.ceil(value) : Math.floor(value);
}

var computeStats = function() {
    for(var i=0; i<levels.length; i++) {
        levels[i].cycleExcessPercent = excessPercent(
            levels[i].cycleBest, levels[i].cycleTarget);
    }
}

mergeIntoLevels = function(rows) {
    for(var i=0; i<levels.length; i++) {
        levels[i].cycleBestNew = false;
    }
    for(var i=0; i<rows.length; i++) {
        var row = rows[i];
        if(!row.passed) continue;
        var level = levelById[row.id];
        if(!level) {
            if(!(/^custom-/.exec(row.id))) {
                console.log("Unknown level id '" + row.id + "'.");
            }
            continue;
        }
        if(row.best_cycles < level.cycleBest) {
            level.cycleBest = row.best_cycles;
            level.cycleBestNew = true;
        }
    }
    computeStats();
}
