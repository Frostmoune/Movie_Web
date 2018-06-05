function moreInfo(obj){
    $(obj).parent().children("span").attr("style", "display:inline;");
    $(obj).attr("style","display:none;");
}

function getSignInForm(response){
    if(response['isPost']==false){
        alert("评论失败！");
        // location.reload();
    }
    else{
        window.location.reload();// 刷新当前页面
    }
}

function postComment(){
    $.ajax({
        url:"#",
        type:"post",
        dataType:"json",
        data:{
                'post_comment':$("#comment").val()
            },
        async:false,
        success:function(response){
            //alert("评论成功");
            location.reload();
        },
        error:function(response){
            location.reload();
            //alert("评论失败！");
        }
    });
}

function post_movieLike(){
    $.ajax({
        url:"logOut",
        type:"get",
        dataType:"json",
        data:{'this_movie_id':true},
        async:false,
    });
}

function post_movieSeen(){
    $.ajax({
        url:"logOut",
        type:"get",
        dataType:"json",
        data:{'this_movie_id':true},
        async:false,
    });
}
