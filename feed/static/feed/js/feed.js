function get_post_ajax_data(post_pk) {
    return {
        'type': 'POST',
        'data': {'post_pk': post_pk, 'csrfmiddlewaretoken': csrf_token }
    }
}

function get_comment_ajax_data(comment_pk) {
    return {
        'type': 'POST',
        'data': {'comment_pk': comment_pk, 'csrfmiddlewaretoken': csrf_token }
    }
}

function like_post(post_pk) {
    if (document.getElementById(post_pk + '_like_button').src.endsWith(staticfiles['inactive_like'])) {
        if (document.getElementById(post_pk + '_dislike_button').src.endsWith(staticfiles['active_dislike'])) {
            document.getElementById(post_pk + '_dislike_button').src = staticfiles['inactive_dislike']
            document.getElementById(post_pk + '_dislike_input').value =
                Number(document.getElementById(post_pk + '_dislike_input').value) - 1;

        }

        $.ajax(urls['like_post'], get_post_ajax_data(post_pk))
        document.getElementById(post_pk + '_like_input').value =
            Number(document.getElementById(post_pk + '_like_input').value) + 1;
        document.getElementById(post_pk + '_like_button').src = staticfiles['active_like']
    } else {
        unlike_post(post_pk)
        document.getElementById(post_pk + '_like_button').src = staticfiles['inactive_like']
    }
}

function dislike_post(post_pk) {
    if (document.getElementById(post_pk + '_dislike_button').src.endsWith(staticfiles['inactive_dislike'])) {
        if (document.getElementById(post_pk + '_like_button').src.endsWith(staticfiles['active_like'])) {
            document.getElementById(post_pk + '_like_button').src = staticfiles['inactive_like']
            document.getElementById(post_pk + '_like_input').value =
                Number(document.getElementById(post_pk + '_like_input').value) - 1;

        }
        $.ajax(urls['dislike_post'], get_post_ajax_data(post_pk))
        document.getElementById(post_pk + '_dislike_input').value =
            Number(document.getElementById(post_pk + '_dislike_input').value) + 1;
        document.getElementById(post_pk + '_dislike_button').src = staticfiles['active_dislike']
    } else {
        undislike_post(post_pk)
        document.getElementById(post_pk + '_dislike_button').src = staticfiles['inactive_dislike']
    }
}

function unlike_post(post_pk) {
    $.ajax(urls['unlike_post'], get_post_ajax_data(post_pk))
    document.getElementById(post_pk + '_like_input').value =
        Number(document.getElementById(post_pk + '_like_input').value) - 1;
}

function undislike_post(post_pk) {
    document.getElementById(post_pk + '_dislike_input').value =
        Number(document.getElementById(post_pk + '_dislike_input').value) - 1;
    $.ajax(urls['undislike_post'], get_post_ajax_data(post_pk))
}

function like_comment(comment_pk) {
    if (document.getElementById(comment_pk + '_comment_like_button').src.endsWith(staticfiles['inactive_like'])) {
        if (document.getElementById(comment_pk + '_comment_dislike_button').src.endsWith(staticfiles['active_dislike'])) {
            document.getElementById(comment_pk + '_comment_dislike_button').src = staticfiles['inactive_dislike']
            document.getElementById(comment_pk + '_comment_dislike_input').value =
                Number(document.getElementById(comment_pk + '_comment_dislike_input').value) - 1;

        }

        $.ajax(urls['like_comment'], get_comment_ajax_data(comment_pk))
        document.getElementById(comment_pk + '_comment_like_input').value =
            Number(document.getElementById(comment_pk + '_comment_like_input').value) + 1;
        document.getElementById(comment_pk + '_comment_like_button').src = staticfiles['active_like']
    } else {
        unlike_comment(comment_pk)
        document.getElementById(comment_pk + '_comment_like_button').src = staticfiles['inactive_like']
    }
}

function dislike_comment(comment_pk) {
    if (document.getElementById(comment_pk + '_comment_dislike_button').src.endsWith(staticfiles['inactive_dislike'])) {
        if (document.getElementById(comment_pk + '_comment_like_button').src.endsWith(staticfiles['active_like'])) {
            document.getElementById(comment_pk + '_comment_like_button').src = staticfiles['inactive_like']
            document.getElementById(comment_pk + '_comment_like_input').value =
                Number(document.getElementById(comment_pk + '_comment_like_input').value) - 1;
        }

        $.ajax(urls['dislike_comment'], get_comment_ajax_data(comment_pk))
        document.getElementById(comment_pk + '_comment_dislike_input').value =
            Number(document.getElementById(comment_pk + '_comment_dislike_input').value) + 1;
        document.getElementById(comment_pk + '_comment_dislike_button').src = staticfiles['active_dislike']
    } else {
        undislike_comment(comment_pk)
        document.getElementById(comment_pk + '_comment_dislike_button').src = staticfiles['inactive_dislike']
    }
}

function unlike_comment(comment_pk) {
    $.ajax(urls['unlike_comment'], get_comment_ajax_data(comment_pk))
    document.getElementById(comment_pk + '_comment_like_input').value =
        Number(document.getElementById(comment_pk + '_comment_like_input').value) - 1;
}

function undislike_comment(comment_pk) {
    document.getElementById(comment_pk + '_comment_dislike_input').value =
        Number(document.getElementById(comment_pk + '_comment_dislike_input').value) - 1;
    $.ajax(urls['undislike_comment'], get_comment_ajax_data(comment_pk))
}

function send_comment(post_pk) {
    let form = document.getElementById(post_pk + '_comment_form')
    const formData = new FormData(form);

    let data = {};

    for (let [key, value] of formData) {
        data[key] = value
    }
    $.ajax(urls['send_comment'], {
        'type': "POST",
        'data': data
    })
    setTimeout(update_post_comments, 100, post_pk)
}

function send_answer(comment_pk, post_pk) {
    let form = document.getElementById(comment_pk + '_answer_form')
    const formData = new FormData(form);

    let data = {};

    for (let [key, value] of formData) {
        data[key] = value
    }
    $.ajax(urls['send_answer_to_comment'], {
        'type': "POST",
        'data': data
    })
    setTimeout(update_post_comments, 100, post_pk)
}

function update_post_comments(post_pk) {
    $.ajax(urls['get_post_comments'], {
        'type': "POST",
        'data': {'post_pk': post_pk, "csrfmiddlewaretoken": csrf_token},
        'success': function (data) {
            document.getElementById(post_pk + '_comments').innerHTML = data;
        }
    })
}