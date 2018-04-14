$('.dropdown-toggle').dropdown()

function getMovieList(obj){
    nowtext = obj.text;
    $.ajax({
        url:"movie_list",
        type:"get",
        dataType:"json",
        data:{'tag':nowtext,'isChange':'1'},
        async:false,
    });
}