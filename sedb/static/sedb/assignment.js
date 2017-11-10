function addNewProblem(url){
    var problem_no = $("#problemSubMenu").children().length;
    $('<li/>').append($('<a/>',{
        href : "#prob"+problem_no,
        text : "Problem "+problem_no,
    })).insertBefore($("#add-button"));

    $('<div/>',{
        id: "prob"+problem_no,
        "class" : "panel panel-primary nav-content",
        html : $("#problem-form").html()
    }).appendTo($("#content"));
//    $("#prob"+problem_no).addClass("hidden");
}
