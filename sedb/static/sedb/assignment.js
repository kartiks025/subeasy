function loadHome(){
    var url = $("#detailsForm").attr('data-loadUrl');
    $.get(url,
    function(data, status){
        if(status == "success"){
            if (!data.new_assign){
                var obj = data.assign;
                var deadline = data.deadline;
                $("#assign_num").val(obj.assignment_no);
                $("#title").val(obj.title);
                if(obj.visibility == "1"){
                    $("#visible").attr('checked',true);
                }
                else{
                    $("#hidden").attr('checked',true);
                }
                $("#pub_time").val(obj.publish_time);
                $("#soft_deadline").val(deadline.soft_deadline);
                $("#hard_deadline").val(deadline.hard_deadline);
                $("#freeze_deadline").val(deadline.freezing_deadline);
                $("#crib_deadline").val(obj.crib_deadline);
                $("#description").val(obj.description);
            }
        }
        else{
            console.log("Some Error Occurred");
        }
    });
}

function updateProblem(prob_id, prob_obj, resource_obj){
    $(prob_id+" input[name=prob_num]").val(prob_obj.problem_no);
    $(prob_id+" input[name=prob_title]").val(prob_obj.title);
    $(prob_id+" textarea[name=description]").val(prob_obj.description);
    $(prob_id+" input[name=files_to_submit]").val(prob_obj.files_to_submit);
    $(prob_id+" input[name=compile_cmd]").val(prob_obj.compile_cmd);
    $(prob_id+" input[sol_visibility][value="+prob_obj.sol_visibility+"]").attr('checked',true);
}

function loadProblems(){
    var url = $("#problemSubMenu").attr("data-loadUrl");
    alert(url);
    $.get(url,
    function(data, status){
        if(status == "success"){
            $(".problems, .problems-link").remove();
            console.log(data);
            var ps = data.problems
            for(var i in ps){
                var prob_obj = ps[i].problem;
                console.log(prob_obj.title);
                appendProb(prob_obj.problem_no);
                var prob_id = "#prob"+prob_obj.problem_no;
                updateProblem(prob_id, prob_obj, ps[i].resource);
                var s = $(prob_id+" .loadUrl").attr('data-loadUrl').replace('0',prob_obj.problem_id);
                $(prob_id+" .loadUrl").attr('data-loadUrl', s);
                s = $(prob_id+" form").attr('action').replace('0',prob_obj.problem_id);
                $(prob_id+" form").attr('action', s);
            }
        }
        else{
            console.log("Some Error Occurred");
        }
    });
}

function reloadProblem(elem){
    var url = elem.parent().parent().attr('data-loadUrl');
    alert(url);
    $.get(url,
    function(data, status){
        if(status == "success"){
            var prob_id = "#"+data.problem.problem_no;
            updateProblem(prob_id, data.problem, data.resource);
        }
        else{
            console.log("Some Error Occurred");
        }
    });
}

function EditButtonClick(elem){
    var pid = "#"+elem.parent().parent().parent().attr('id');
    var rval = $(pid+" input").prop('disabled');

    var elem = elem.find("> span");
    if (elem.hasClass('glyphicon-pencil')){
        elem.removeClass('glyphicon-pencil');
        elem.addClass('glyphicon-ok');

        $(pid+" input").attr('disabled',!rval);
        $(pid+" textarea").attr('disabled',!rval);
    }
    else{
        var frm = $(pid+" form");
        frm.validate();
        if(frm.valid()){
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                success: function (data) {
                    console.log('Submission was successful.');
                    console.log(data);

                    frm.attr('action',frm.attr('action').replace('0',data.r_id));
                    var div = frm.parent().parent();
                    div.attr('data-loadUrl',div.attr('data-loadUrl').replace('0',data.r_id));

                    if(data.to_redirect){
                        window.location.href=data.url;
                    }
                    else{
                        if(pid=="#details"){
                            loadHome();
                        }
                        else{
                            reloadProblem(elem);
                        }
                    }
                },
                error: function (data) {
                    console.log('An error occurred.');
                    console.log(data);
                },
            });

            elem.removeClass('glyphicon-ok');
            elem.addClass('glyphicon-pencil');

            $(pid+" input").attr('disabled',!rval);
            $(pid+" textarea").attr('disabled',!rval);
        }
    }
}

function SideNavClick(elem){
    $("#list-nav .active").toggleClass("active");
    $(this).parent().toggleClass("active");

    var vis = $("#content :visible");
    vis.addClass('hidden');

    var toShowDiv = elem.attr("href");
    $(toShowDiv).find("*").removeClass('hidden');
    $(toShowDiv).removeClass('hidden');
}

function appendProb(problem_no){
    $('<li/>').append($('<a/>',{
        id : "link"+problem_no,
        href : "#prob"+problem_no,
        "class" : "side-nav-link problems-link",
        text : "Problem "+problem_no,
        on : {
            click : function(){
                SideNavClick($(this));
            }
        }
    })).insertBefore($("#add-button"));

    var vis = $("#content :visible");
    vis.addClass('hidden');

    $('<div/>',{
        id: "prob"+problem_no,
        "class" : "panel panel-primary nav-content problems",
        html : $("#problem-form").html()
    }).appendTo($("#content"));

    $("#prob"+problem_no+" .edit-btn").on("click", function(){
        EditButtonClick($(this));
    });

    $("#list-nav .active").toggleClass("active");
    $("#link"+problem_no).parent().toggleClass("active");
}

function addNewProblem(url){
    var problem_no = $("#problemSubMenu").children().length;
    appendProb(problem_no);
}
