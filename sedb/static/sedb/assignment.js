function addNewProblem(url){
    alert(url);
    $.get(url,
        function(data, status){
            if(status == "success"){
                $('<li/>').append($('<a/>',{
                    href : "#prob"+data.problem_no,
                    text : "Problem "+data.problem_no
                })).insertBefore($("#add-button"));
            }
    })
}
