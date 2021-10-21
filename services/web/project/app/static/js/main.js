$(function(){
    window.setInterval(function(){
        loadUpvote()
    }, 1000)
})

function loadUpvote(){
    $.ajax({
        URL:"/upvote",
        type = "POST",
        dataType = "json",
        success: function(data){
            $(numVote).replaceWith(data)
        }
    });
}