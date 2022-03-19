const one = document.getElementById('satr1');
const two = document.getElementById('satr2');
const three = document.getElementById('satr3');
const four = document.getElementById('satr4');
const five = document.getElementById('satr5');

const form = document.querySelector('.rate-form');
const confmBox = document.getElementById('confirm-box');

const csrf = document.getElementsByName('csrfmiddlewaretoken')

const  handleStartSelect = (size) =>{
    const children = form.children;
    for(let i = 0; i < children.length; i++){
        if(i <= size){
            children[i].classList.add('checked')
        }else{
            children[i].classList.remove('check')
        }
    }
};

const handleSelect = (selection) =>{
    switch (selection) {
        case 'satr1':
            handleStartSelect(1);
            return
         case 'satr2':
            handleStartSelect(2);
            return
         case 'satr3':
            handleStartSelect(3);
            return
         case 'satr4':
            handleStartSelect(4);
            return
         case 'satr5':
            handleStartSelect(5);
            return

    }
};

const getNumberValue = (stringValue) =>{
    let numberValue;
    if(stringValue === 'star1'){
        numberValue = 1
    }
    else if(stringValue === 'star2'){
         numberValue = 2
    }
     else if(stringValue === 'star3'){
         numberValue = 3
    }
      else if(stringValue === 'star4'){
         numberValue = 4
    }
       else if(stringValue === 'star5'){
         numberValue = 5
    }
       else{
           numberValue = 0
    }
       return numberValue
}

if (one){
    const arr = [one, two, three, four, five]

    arr.forEach(item => item.addEventListener('mouseover', (event) => {
        handleSelect(event.target.id)
    }))

    arr.forEach(item => item.addEventListener('click', (event) => {
        const val = event.target.id
        console.log(val)
        form.addEventListener('submit', e =>{
            e.preventDefault()
            const id = e.target.id
            console.log(id)
            const val_num = getNumberValue(val)
        })
    }))
}

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
                if($('#rate').val()==='0'){
                    var rating_html = data['pk'] + data['val'] + data['csrfmiddlewaretoken']
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
    $('#reply_comment_id').val(reply_comment_id)
    var html = $('#comment_' + reply_comment_id).html()
    $('#reply_content').html(html)
    $('#reply_content_container').show();

    $('html').animate({scrollTop: $('#comment_form').offset().top - 60}, 300, function(){
        CKEDITOR.instances['id_text'].focus();
    });
    }
