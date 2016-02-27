var loadInput = document.getElementById('loadInput');
var loadDebug = document.getElementById('loadDebug');

var tableCreate = function () {
    function valconcat(vals, tagName) {
        if (vals.length === 0) return '';
        var open = '<'+tagName+'>', close='</'+tagName+'>';
        return open + vals.join(close + open) + close;
    }
    return function (columns, values){
        var tbl  = document.createElement('table');
        var html = '<thead>' + valconcat(columns, 'th') + '</thead>';
        var rows = values.map(function(v){ return valconcat(v, 'td'); });
        html += '<tbody>' + valconcat(rows, 'tr') + '</tbody>';
        tbl.innerHTML = html;
        return tbl;
    }
}();

loadInput.onchange = function() {
    var f = loadInput.files[0];
    var r = new FileReader();
    var db;
    r.onload = function() {
        var Uints = new Uint8Array(r.result);
        db = new SQL.Database(Uints);
    }
    r.onloadend = function() {
        if(r.error) {
            console.log(r.error.message);
            return;
        }
        var raw = db.exec("select * from Level order by id;");
        if(window.location.href.indexOf("?debug") > -1) {
            loadDebug.innerHTML = "";
            loadDebug.appendChild(tableCreate(raw[0].columns, raw[0].values));
        }
        var rows = [];
        for(var i=0; i<raw[0].values.length; i++) {
            var row = {};
            for(var j=0; j<raw[0].columns.length; j++) {
                row[raw[0].columns[j]] = raw[0].values[i][j];
            }
            rows.push(row);
        }
        console.log("Got " + rows.length + " rows.");
    }
    r.readAsArrayBuffer(f);
}
