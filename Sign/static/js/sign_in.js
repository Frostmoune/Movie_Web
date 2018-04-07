function getSignInForm(response){
    if(response['isLogin']==false){
        alert("登录失败！");
        // location.reload();
    }
    else{
        window.location = "/signIn/jump";
    }
}

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