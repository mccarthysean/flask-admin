

var count = 0;
var td_id = 0;
var current_id;

var settings = {
        "url": "/meta_data",
        "method": "GET",
        "timeout": 0,
        "headers": {
          "Authorization": "Token 8b0f89e987a20371bd5442c0550f0e12a22bbfbf",
          "Content-Type": "application/json"
        },
      };
      
      $.ajax(settings).done(function (response) {
              console.log(response)
        response.forEach(function(elem){
                if(elem.element == "font"){
                        if(document.querySelector("td[data-id='" + elem.id_cell +"']>a")){
                                $("td[data-id='" + elem.id_cell +"']>a").css({
                                        "color": elem.color,
                                        "border-bottom": "dashed 1px " + elem.color
                                })
                        }
                        else{
                                $("td[data-id='" + elem.id_cell +"']").css({
                                "color": elem.color,
                        })
                    }   
                } 
                else{
                        $("td[data-id='" + elem.id_cell +"']").css("background",elem.color);
                }
        })

      });


$("td").click(function () {
        if($(this).attr("class")=="list-buttons-column" || $(this).attr("class")=="list-checkbox-column"){
                console.log("done")
                return;
        }
        if (count == 0) {
                $(".actions-nav").append(`
<li class="d-flex">
    <i class="fa fa-font mt-custom" aria-hidden="true"></i>
    <div class="form-group">
<input type="color" class="form-control w-150 ml-custom" id="color" onchange="fillcolor1(this)" list="presetColors">
<datalist id="presetColors">
        <option>#0275d8</option>
        <option>#5cb85c</option>
        <option>#5bc0de</option>
        <option>#f0ad4e</option>
        <option>#d9534f</option>
        <option>#292b2c</option>
        <option>#f7f7f7</option>
        </datalist>
</div>
<div class="form-group">
</li>
<li class="d-flex ml-5">
<i class="fa fa-fill mt-custom"></i>
<div class="form-group">
<input type="color" class="form-control w-150 ml-custom" id="color" onchange="fillcolor2(this)" list="presetColors">
<datalist id="presetColors">
        <option>#0275d8</option>
        <option>#5cb85c</option>
        <option>#5bc0de</option>
        <option>#f0ad4e</option>
        <option>#d9534f</option>
        <option>#292b2c</option>
        <option>#f7f7f7</option>
        </datalist>
</div>
<div class="form-group">

</li>
`)
                count++;

        }
        $("td").css("border", "1px solid #ddd")
        $(this).css("border", "2px solid black")
        $(this).attr("id", "focus" + td_id)
        current_id = $(this).attr("id");
        td_id++;

})

function fillcolor1(val) {
        if(document.querySelector("#"+current_id+">a")){
                $("#" + current_id + ">a").css({
                        "color": val.value,
                        "border-bottom": "dashed 1px " + val.value
                })
        }
        else{
        $("#" + current_id).css({
                "color": val.value,
        })
}
        var settings = {
                "url": "/meta_data",
                "method": "POST",
                "timeout": 0,
                "headers": {
                        "Authorization": "Token 8b0f89e987a20371bd5442c0550f0e12a22bbfbf",
                        "Content-Type": "application/json"
                 },
                "data": JSON.stringify({"id_cell":$("#" + current_id).attr("data-id"),"element":"font","color":val.value}),
              };
              
              $.ajax(settings).done(function (response) {
                console.log(response);
              });
}

function fillcolor2(val) {
        $("#" + current_id).css("background",val.value)
        var settings = {
                "url": "/meta_data",
                "method": "POST",
                "timeout": 0,
                "headers": {
                        "Authorization": "Token 8b0f89e987a20371bd5442c0550f0e12a22bbfbf",
                        "Content-Type": "application/json"
                 },
                "data": JSON.stringify({"id_cell":$("#" + current_id).attr("data-id"),"element":"background","color":val.value}),
              };
              
              $.ajax(settings).done(function (response) {
                console.log(response);
              });
}

var class_arr = [];
 for(var i = 2 ; i<document.querySelectorAll("th").length;i++){
   class_arr.push(document.querySelectorAll("th")[i].getAttribute("class").split(" ")[1]);
 }

 console.log(class_arr)
 
 class_arr.forEach(function(class_elem){
         var temp=0;
         for(var i = 1 ;i<=document.querySelectorAll("."+class_elem).length-1;i++){
                 if(document.querySelectorAll("."+class_elem)[i].querySelector("a>strong")){
                        document.querySelectorAll("."+class_elem)[i].setAttribute("data-id",class_elem+"_"+document.querySelectorAll("."+class_elem)[i].querySelector("a>strong").innerText+"_row_"+document.querySelectorAll(".elem")[temp].querySelector("a").innerText)
                 }
                 else{
                         if(document.querySelectorAll(".elem")[temp].querySelector("a")) {
                                document.querySelectorAll("."+class_elem)[i].setAttribute("data-id",class_elem+"_"+document.querySelectorAll("."+class_elem)[i].innerText+"_row_"+document.querySelectorAll(".elem")[temp].querySelector("a").innerText)
                         }
                         else{
                        document.querySelectorAll("."+class_elem)[i].setAttribute("data-id",class_elem+"_"+document.querySelectorAll("."+class_elem)[i].innerText+"_row_"+document.querySelectorAll(".elem")[temp].innerText)
                         } 
                }
                 temp++;
        }
         
 })
