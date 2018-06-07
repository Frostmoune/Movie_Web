function updateMovie(str, movieList){
    var fatherDiv;
    if(str == "seen"){
        fatherDiv = $("#Seen_zone");
        fatherDiv.children("#Seen_list").remove();
        fatherDiv.children("#Seen_but").remove();
    }
    else if(str == "liked"){
        fatherDiv = $("#Favourite_zone");
        fatherDiv.children("#Liked_list").remove();
        fatherDiv.children("#Liked_but").remove();
    }
    else if(str == "changed"){
        fatherDiv = $("#Recommend_zone");
        fatherDiv.children("#Recommend_list").remove();
        fatherDiv.children("#Recommend_but").remove();
    }
    var num = 0, row_tag, col_tag;
    for(var i in movieList){
        var movie = movieList[i];
        if(num == 0){
            row_tag = $("<div></div>").attr("class", "row");
            if(str == "seen"){
                row_tag.attr("id", "Seen_list");
            }
            else if(str == "liked"){
                row_tag.attr("id", "Liked_list");
            }
            else if(str == 'changed'){
                row_tag.attr("id", "Recommend_list");
            }
        }
        col_tag = $("<div></div>").attr("class", "col-sm-4 col-md-2");
        now_thum = $('<div class="thumbnail"></div>');
        now_a = $('<a></a>').attr('href', '../movie/' + movie.id.toString()).attr('id', 'movie_' + movie.id.toString() + '_id');
        now_img = $('<img></img>').attr('src', '../static/items/' + movie.picture.toString()).attr('alt', movie.id.toString()).attr('id', 'movie_' + movie.id.toString() + '_picture');
        now_a.append(now_img);
        now_thum.append(now_a);
        now_div = $('<div class="caption"></div>');
        now_a = $('<a></a>').attr('href', '../movie/' + movie.id.toString());
        now_strong = $('<strong class="info"></strong>').attr('id', 'movie_' + movie.id.toString() + '_title').text(movie.title.toString())
        now_a.append(now_strong);
        now_div.append(now_a);
        now_div.append($('<br>'));
        now_strong = $('<strong class="info"></strong>').attr('id', 'movie_' + movie.id.toString() + '_score').text('豆瓣评分：' + movie.score.toString())
        now_div.append(now_strong);
        now_div.append($('<br>'));
        now_p = $('<p class="info_2"></p>').attr("id", "movie_" + movie.id.toString() + '_type').text('类型：' + movie.type.toString())
        now_div.append(now_p)
        now_p = $('<p class="info_2"></p>').attr("id", "movie_" + movie.id.toString() + '_country').text('国家/地区：' + movie.country.toString())
        now_div.append(now_p)
        now_thum.append(now_div);
        col_tag.append(now_thum);
        row_tag.append(col_tag);
        num = (num + 1) % 6;
        if(num == 0){
            fatherDiv.append(row_tag);
        }
    }
    fatherDiv.append(row_tag);
    if(str == 'changed'){
        now_but = $('<button type="button" class="btn btn-link btn-sm" id = "Recommend_but"></button>').attr("onclick", "getMoreMovie('changed')").text("换一批");
        fatherDiv.append(now_but);
    }
}

function getMoreMovie(str){
    $.ajax({
        url:str,
        type:"get",
        async:false,
        success:function(response){
            if(str == 'changed'){
                updateMovie(str, response['Changed']);
            }
            else updateMovie(str, response['More']);
        },
        error:function(){
            alert("error");
        }
    });
}
