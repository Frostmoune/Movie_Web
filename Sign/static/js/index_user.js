function postLike(movie_id){
    $.ajax({
        url:"logOut",
        type:"get",
        dataType:"json",
        data:{'movie_id':movie_id},
        async:false,
    });
}

function postSeen(movie_id){
    $.ajax({
        url:"logOut",
        type:"get",
        dataType:"json",
        data:{'movie_id':movie_id},
        async:false,
    });
}