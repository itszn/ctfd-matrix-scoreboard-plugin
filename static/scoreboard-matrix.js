function updatescores () {
    $.get(script_root + '/scores', function( data ) {
        teams = $.parseJSON(JSON.stringify(data));
        $('#scoreboard > tbody').empty()
        for (var i = 0; i < teams['standings'].length; i++) {
            row = "<tr><td>{0}</td><td><a href='/team/{1}'>{2}</a></td><td>{3}</td>".format(i+1, teams['standings'][i].id, htmlentities(teams['standings'][i].team), teams['standings'][i].score);
            for (var j = 0; j < challenges.length; j++) {
                if (teams['standings'][i].solves.indexOf(challenges[j].id) != -1) {
                    row += '<td class="chalmark">✔</td>';
                } else {
                    row += '<td class="chalmark"></td>';
                }
            }
            row += '</tr>';
            $('#scoreboard > tbody').append(row)
        };
    });
}

function cumulativesum (arr) {
    var result = arr.concat();
    for (var i = 0; i < arr.length; i++){
        result[i] = arr.slice(0, i + 1).reduce(function(p, i){ return p + i; });
    }
    return result
}

function UTCtoDate(utc){
    var d = new Date(0)
        d.setUTCSeconds(utc)
        return d;
}

function update(){
    updatescores();
}

setInterval(update, 300000); // Update scores every 5 minutes



