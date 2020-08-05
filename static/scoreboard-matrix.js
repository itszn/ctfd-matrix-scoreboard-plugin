const $ = CTFd.lib.$;

function htmlentities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function updatescores() {
    $.get(CTFd.config.urlRoot + '/score', function (data) {
        teams = $.parseJSON(JSON.stringify(data));
        $('#scoreboard > tbody').empty()
        for (var i = 0; i < teams['standings'].length; i++) {
            row = `<tr>
                <td>${i + 1}</td>
                <td><a href='/${mode}/${teams['standings'][i].id}'>${
                    htmlentities(teams['standings'][i].team)
                }</a></td>
                <td>${teams['standings'][i].score}</td>
            `;
            for (var j = 0; j < challenges.length; j++) {
                if (teams['standings'][i].solves.indexOf(challenges[j].id) != -1) {
                    row += '<td class="chalmark">✔</td>';
                } else {
                    row += '<td class="chalmark"></td>';
                }
            }
            row += '</tr>';
            $('#scoreboard > tbody').append(row)
        }
    });
}

setInterval(updatescores, 300000); // Update scores every 5 minutes



