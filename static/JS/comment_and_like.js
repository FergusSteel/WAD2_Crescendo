    $("#comment_form").submit(function() {
    // check none
        $("#comment_error").text('');
        if (CKEDITOR.instances["id_text"].document.getBody().getText().trim() === '') {
            $("#comment_error").text('Comment can not be empty');
            return false;
    }

    // updata textarea
    CKEDITOR.instances['id_text'].updateElement();

    //AJAX
    $.ajax({
        url: CommentUrl,
        type: 'POST',
        data: $(this).serialize(),
        cache: false,
        success: function (data) {
            console.log(data);

            // insert data
            if (data['status'] === "SUCCESS") {
                // comment and like
                if ($('#reply_comment_id').val() === '0') {
                    var comment_html = '<div id="root_{0}" class="comment">' +'<span' + data['username'] + '>' + '<span>('+ data['comment_time'] + ')：</span>' + '<div id="comment_'+ data['pk'] + '">'+ data['text'] +'</div>' +'<div class="like" onclick="like_change(this,' +  data['content_type']  + ',' + data['pk'] + ')">' + '<span class="glyphicon glyphicon-thumbs-up"/>' + '<span class="liked-num">0</span>' +'<div>' +'<a href="javascript:reply('+ data['pk'] + ');">Reply</a>' +'</div>';
                    $("#comment_list").prepend(comment_html);
                } else {
                    // reply and like
                    var reply_html ='<div class="reply">' + '<span' + data['username'] + '>' + '<span> ('+ data['comment_time'] + ')</span>' + '<span>Reply </span>' + '<span>' + data['reply_to'] + '：</span>' + '<div id="comment_' + data['pk'] + '">'+ data['text'] + '</div>' + '<div class="like" onclick="like_change(this,'+  data['content_type'] + ',' + data['pk'] + ')">' + '<span class="glyphicon glyphicon-thumbs-up"/> ' + '<span class="liked-num">0</span>' + '</div>' + '<a href="javascript:reply(' + data['pk'] + ');">Reply</a>' + '</div>';
                    $("#root_" + data['root_id']).append(reply_html);
                }

                // clean textarea
                CKEDITOR.instances['id_text'].setData('');
                //clean reply
                $('#reply_content_container').hide();
                $('#reply_comment_id').val('0');
                $('#no_comment').remove();
                $("#comment_error").text("Comment Successfully")
            } else {
                // show error message
                $("#comment_error").text(data['message']);
            }
        },
        error: function (xhr) {
            console.log(xhr);
        }
    });
    return false;
});

    function reply(reply_comment_id){
        $('#reply_comment_id').val(reply_comment_id);
        var html = $('#comment_' + reply_comment_id).html();
        $('#reply_content').html(html);
        $('#reply_content_container').show();

        $('html').animate({scrollTop: $('#comment_form').offset().top - 70}, 300, function(){
        CKEDITOR.instances['id_text'].focus();
        });
        }

    function like_change(obj, content_type, object_id){
            var is_like = obj.getElementsByClassName('active').length === 0;
            $.ajax({
                url: likeUrl,
                type: 'GET',
                data: {
                    content_type: content_type,
                    object_id: object_id,
                    is_like: is_like
                },
                cache: false,
                success: function(data){
                    console.log(data);
                    if(data['status']==='SUCCESS'){
                        // update like status
                        var element = $(obj.getElementsByClassName('glyphicon'));
                        if(is_like){
                            element.addClass('active');
                        }else{
                            element.removeClass('active');
                        }
                        // update like number
                        var liked_num = $(obj.getElementsByClassName('liked-num'));
                        liked_num.text(data['liked_num']);
                    }
                },
                error: function(xhr){
                    console.log(xhr)
                }
            });
        }
