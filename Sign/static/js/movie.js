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
                'post_comment':$("#comment").val(),
                'comment_flag':'t'
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

function postLike(movie_title){
    $.ajax({
        url:"#",
        type:"post",
        dataType:"json",
        data:{'movie_title':movie_title,
                'tag':'liked',
                'comment_flag':'f'
            },
        async:false,
        success:function(response){
            //alert("评论成功");
            //location.reload();
        },
        error:function(response){
            //location.reload();
            //alert("评论失败！");
        }
    });
}

function postSeen(movie_title){
    $.ajax({
        url:"#",
        type:"post",
        dataType:"json",
        data:{'movie_title':movie_title,
                'tag':'seen',
                'comment_flag':'f'
            },
        async:false,
        success:function(response){
            //alert("评论成功");
            //location.reload();
        },
        error:function(response){
            //location.reload();
            //alert("评论失败！");
        }
    });
}
