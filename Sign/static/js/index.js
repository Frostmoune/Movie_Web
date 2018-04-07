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

function changeMovieList(obj){
    path = "../static/items/";
    pre = "movie_show_";
    for(var i=1;i<13;++i){
        nowpath = path + obj[pre + i.toString()].toString();
        $("#" + pre + i.toString()).attr("src",nowpath)
        $("#" + pre + i.toString()).attr("title",obj[pre + i.toString() + "_title"].toString())
        $("#" + pre + i.toString() + "_title").text(obj[pre + i.toString() + "_title"].toString())
        $("#" + pre + i.toString() + "_score").text("豆瓣评分：" + obj[pre + i.toString() + "_score"].toString())
        $("#" + pre + i.toString() + "_type").text("类型：" + obj[pre + i.toString() + "_type"].toString())
        $("#" + pre + i.toString() + "_country").text("国家/地区：" + obj[pre + i.toString() + "_country"].toString())
    }
}

window.onload=setInterval(function(){
    nowtag = document.title
    if(nowtag=="Index"){
        $.ajax({
            url:"movie_list",
            type:"get",
            dataType:"json",
            data:{'tag':'All','isChange':'0'},
            async:false,
            success:function(result){
                changeMovieList(result);
            },
            error:function(){
                alert("Warning!");
            }
        });
    }
    else{
        $.ajax({
            url:"movie_list",
            type:"get",
            dataType:"json",
            data:{'tag':nowtag,'isChange':'0'},
            async:false,
            success:function(result){
                changeMovieList(result);
            },
            error:function(){
                alert("Warning!");
            }
        });
    }
},10000)

