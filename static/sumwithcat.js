score_cat_all = {};
$(document).ready(function() {
    $('#scoreboard').tablesorter();
    for(var i = 1;;i++){
        var target_team_id = i+'-team-score';
        var target_team = document.getElementById(target_team_id);
        if(null==target_team || undefined==target_team){
            break;
        }
        score_cat_all[target_team_id] = target_team.textContent;
    }
});

$('#cat-selector').change(function() {

var cat = $(this).val();
var all_cat_elem1 = document.getElementsByClassName('chalname');
var all_cat_elem2 = document.getElementsByClassName('chalmark');
if('all'==cat){
    display_default(all_cat_elem1);
    display_default(all_cat_elem2);
    for(var i = 1;;i++){
        var target_team_id = i+'-team-score';
        var target_team = document.getElementById(target_team_id);
        if(null==target_team || undefined==target_team){
            break;
        }
        target_team.textContent = score_cat_all[target_team_id];
        document.getElementById('score-category').textContent = 'Score-ALL';
    }
    return;
}else{
    display_none(all_cat_elem1);
    display_none(all_cat_elem2);
}

var target_cat_elem = document.getElementsByClassName('class-'+cat);
display_default(target_cat_elem);

for(var i = 1;;i++){
    var target_team_id = i+'-team-score';
    var target_team = document.getElementById(target_team_id);
    if(null==target_team || undefined==target_team){
        break;
    }
    var sum_cat_score = 0;
    var elems = document.getElementsByClassName(i+'-team-'+cat);
    for(var j = 0; j < elems.length; j++){
        sum_cat_score+=parseInt(elems.item(j).title);
    }
    target_team.textContent = sum_cat_score.toString(10);
}
document.getElementById('score-category').textContent = 'Score-'+cat;

});

function display_default(elems){
    for(var i = 0; i < elems.length; i++){
        elems.item(i).style.display='';
    }
}

function display_none(elems){
    for(var i = 0; i < elems.length; i++){
        elems.item(i).style.display='none';
    }
}
