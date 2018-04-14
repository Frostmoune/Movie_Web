// 将登出请求发送到后端
function postLogOut(){
    $.ajax({
        url:"logOut",
        type:"get",
        dataType:"json",
        data:{'logOut':true},
        async:false,
        success:function(response){
            if(response['logOut']==true){
                alert("注销成功！");
                window.location.reload();
            }
            else{
                alert("注销失败！");
            }
        },
        error:function(){
            alert("注销失败！");
        }
    });
}