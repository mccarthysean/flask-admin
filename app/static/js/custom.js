var count = 0;
var td_id=0;
var current_id;
$("td").click(function(){
if(count == 0){
$(".actions-nav").append(`
<li class="d-flex">
    <i class="fa fa-font mt-custom" aria-hidden="true"></i>
    <div class="form-group">
<input type="color" class="form-control w-200 ml-custom" id="color" onchange="fillcolor1(this)">
</div>
<div class="form-group">
</li>
<li class="d-flex ml-5">
<i class="fa fa-fill mt-custom"></i>
<div class="form-group">
<input type="color" class="form-control w-200 ml-custom" id="color" onchange="fillcolor2(this)">
</div>
<div class="form-group">

</li>
`) 
count++;

}
$("td").css("border","1px solid #ddd")
$(this).css("border","2px solid black")
$(this).attr("id","focus"+td_id)
current_id = $(this).attr("id");
td_id++;

})
function fillcolor1(val){
$("#"+current_id+">a").css({
"color":val.value,
"border-bottom":"dashed 1px "+val.value
})

}
function fillcolor2(val){

$("#"+current_id).css("background",val.value)

}
