$(document).ready(function() {
    $('#scoreboard').tablesorter();
});

$('#cat-selector').change(function() {

var cat = $(this).val();
var all_cat_elem1 = document.getElementsByClassName('chalname');
var all_cat_elem2 = document.getElementsByClassName('chalmark');
if('all'==cat){
    display_default(all_cat_elem1);
    display_default(all_cat_elem2);
    return;
}else{
    display_none(all_cat_elem1);
    display_none(all_cat_elem2);
}

var target_cat_elem = document.getElementsByClassName('class-'+cat);
display_default(target_cat_elem);
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
