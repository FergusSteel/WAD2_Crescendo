$("#comment_form").submit(function() {

    // check none

    $("#comment_error").text('');
    if (CKEDITOR.instances["id_text"].document.getBody().getText().trim() === '') {
        $("#comment_error").text('Comment can not empty');
        return false;
    }

    // updata textarea
    CKEDITOR.instances['id_text'].updateElement();

    //AJAX
    $.ajax({
        url: myUrl,
        type: 'POST',
        data: $(this).serialize(),
        cache: false,
        success: function (data) {
            console.log(data);

            // insert data
            if (data['status'] === "SUCCESS") {

                // comment
                if ($('#reply_comment_id').val() === '0') {
                    var comment_html = '<div id="root_' + data['pk'] + '" class="comment"><span>' + data['username'] + '</span><span> (' + data['comment_time'] + ')：</span><div id="comment_' + data['pk'] + '">' + data['text'] + '</div><a href="javascript:reply(' + data['pk'] + ');">Reply</a></div>';
                    $('#comment_list').prepend(comment_html);
                } else {
                    // reply
                    var reply_html = '<div class="reply"><span>' + data['username'] + '</span><span> (' + data['comment_time'] + ')</span><span> 回复 </span><span>' + data['reply_to'] + '：</span><div id="comment_' + data['pk'] + '">' + data['text'] + '</div><a href="javascript:reply(' + data['pk'] + ');">Reply</a></div>';
                    $('#root_' + data['root_id']).append(reply_html)
                }

                // clean textarea
                CKEDITOR.instances['id_text'].setData('');
                //clean reply
                $('#reply_content_container').hide();
                $('#reply_comment_id').val('0');
                $('#no_comment').remove();
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

    $('html').animate({scrollTop: $('#comment_form').offset().top - 60}, 300, function(){
        CKEDITOR.instances['id_text'].focus();
    });
    }
