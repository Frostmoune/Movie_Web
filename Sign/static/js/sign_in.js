// 根据请求决定是否跳转
function getSignInForm(response){
    if(response['isLogin']==false){
        alert("登录失败！");
        // location.reload();
    }
    else{
        window.location = "/signIn/jump";// 跳转到新地址
    }
}

// 将用户输入的登录信息发送到后端
function postFormData(){
    $.ajax({
        url:"sign_in_form",
        type:"post",
        dataType:"json",
        data:{'username':$("#Userid").val(),
                'password':$("#Password").val(),
            },
        async:false,
        success:function(response){
            getSignInForm(response);
        },
        error:function(){
            alert("登录失败！");
            // location.reload();
        }
    });
}

function jumpSignUp(){
    window.location="/signUp"
}