function getSignUpForm(response){
    if(response['isLogin']==false){
        if(response['userExist']==true){
            alert("账户已存在");
        }
        else{
            alert("注册失败!");
        }
        location.reload();
    }
    else{
        window.location = "/signUp/jump";
    }
}

function postFormData(){
    password = $("#Password").val();
    confirm = $("#ConfirmPassword").val();
    if(password!=confirm){
        alert("两次输入的密码不相符");
        location.reload();
    }
    else{
        $.ajax({
            url:"sign_up_form",
            type:"post",
            dataType:"json",
            data:{'username':$("#Userid").val(),
                    'password':password,
                    'email':$("#Email").val(),
                    'confirm':confirm
                },
            async:false,
            success:function(response){
                getSignUpForm(response);
            },
            error:function(){
                alert("注册失败！");
                location.reload();
            }
        });
    }
}

function jumpSignIn(){
    window.location="/signIn"
}