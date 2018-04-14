// 发送请求到后端，请求后端发送电影信息，此函数用于跳转时

// 根据后端发来的Json信息改变当前页面的电影信息
function changeMovieList(obj){
    path = "../static/items/";
    pre = "movie_show_";
    for(var i=1;i<13;++i){
        nowpath = path + obj[pre + i.toString()].toString();
        $("#" + pre + i.toString()).attr("src", nowpath)
        $("#" + pre + i.toString()).attr("title", obj[pre + i.toString() + "_title"].toString())
        $("#" + pre + i.toString() + "_id").attr("href", "../movie/" + obj[pre + i.toString() + "_id"].toString())
        $("#" + pre + i.toString() + "_title").text(obj[pre + i.toString() + "_title"].toString())
        $("#" + pre + i.toString() + "_score").text("豆瓣评分：" + obj[pre + i.toString() + "_score"].toString())
        $("#" + pre + i.toString() + "_type").text("类型：" + obj[pre + i.toString() + "_type"].toString())
        $("#" + pre + i.toString() + "_country").text("国家/地区：" + obj[pre + i.toString() + "_country"].toString())
    }
}

// 发送请求到后端，请求后端发送电影信息，此函数用于跳转后的页面（页面每10s发送一个请求）
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
},10000) // 10000表示10000毫秒

