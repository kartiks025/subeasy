function loadHome(){
    var url = $("#detailsForm").attr('data-loadUrl');
    alert(url);
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

                    frm.attr('action',frm.attr('action').replace('0',data.assign_id));
                    $("#detailsForm").attr('data-loadUrl',$("#detailsForm").attr('data-loadUrl').replace('0',data.assign_id));

                    if(data.to_redirect){
                        window.location.href=data.url;
                    }
                    else{
                        if(pid=="#details")loadHome();
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

function addNewProblem(url){
    var problem_no = $("#problemSubMenu").children().length;
    $('<li/>').append($('<a/>',{
        id : "link"+problem_no,
        href : "#prob"+problem_no,
        "class" : "side-nav-link",
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
        "class" : "panel panel-primary nav-content",
        html : $("#problem-form").html()
    }).appendTo($("#content"));

    $("#prob"+problem_no+" .edit-btn").on("click", function(){
        EditButtonClick($(this));
    });

    $("#list-nav .active").toggleClass("active");
    $("#link"+problem_no).parent().toggleClass("active");
}
