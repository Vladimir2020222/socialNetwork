function like_post(post_pk) {
    if (document.getElementById(post_pk + '_like_button').src.endsWith(staticfiles['inactive_like'])) {
        if (document.getElementById(post_pk + '_dislike_button').src.endsWith(staticfiles['active_dislike'])) {
            document.getElementById(post_pk + '_dislike_button').src = staticfiles['inactive_dislike']
            document.getElementById(post_pk + '_dislike_input').value =
                Number(document.getElementById(post_pk + '_dislike_input').value) - 1;

        }

        ajax_data_POST(urls['like_post'], {'post_pk': post_pk})
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
        ajax_data_POST(urls['dislike_post'], {'post_pk': post_pk})
        document.getElementById(post_pk + '_dislike_input').value =
            Number(document.getElementById(post_pk + '_dislike_input').value) + 1;
        document.getElementById(post_pk + '_dislike_button').src = staticfiles['active_dislike']
    } else {
        undislike_post(post_pk)
        document.getElementById(post_pk + '_dislike_button').src = staticfiles['inactive_dislike']
    }
}

function unlike_post(post_pk) {
    ajax_data_POST(urls['unlike_post'], {'post_pk': post_pk})
    document.getElementById(post_pk + '_like_input').value =
        Number(document.getElementById(post_pk + '_like_input').value) - 1;
}

function undislike_post(post_pk) {
    document.getElementById(post_pk + '_dislike_input').value =
        Number(document.getElementById(post_pk + '_dislike_input').value) - 1;
    ajax_data_POST(urls['undislike_post'], {'post_pk': post_pk})
}

function like_comment(comment_pk) {
    if (document.getElementById(comment_pk + '_comment_like_button').src.endsWith(staticfiles['inactive_like'])) {
        if (document.getElementById(comment_pk + '_comment_dislike_button').src.endsWith(staticfiles['active_dislike'])) {
            document.getElementById(comment_pk + '_comment_dislike_button').src = staticfiles['inactive_dislike']
            document.getElementById(comment_pk + '_comment_dislike_input').value =
                Number(document.getElementById(comment_pk + '_comment_dislike_input').value) - 1;

        }

        ajax_data_POST(urls['like_comment'], {'comment_pk': comment_pk})
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

        ajax_data_POST(urls['dislike_comment'], {'comment_pk': comment_pk})
        document.getElementById(comment_pk + '_comment_dislike_input').value =
            Number(document.getElementById(comment_pk + '_comment_dislike_input').value) + 1;
        document.getElementById(comment_pk + '_comment_dislike_button').src = staticfiles['active_dislike']
    } else {
        undislike_comment(comment_pk)
        document.getElementById(comment_pk + '_comment_dislike_button').src = staticfiles['inactive_dislike']
    }
}

function unlike_comment(comment_pk) {
    ajax_data_POST(urls['unlike_comment'], {'comment_pk': comment_pk})
    document.getElementById(comment_pk + '_comment_like_input').value =
        Number(document.getElementById(comment_pk + '_comment_like_input').value) - 1;
}

function undislike_comment(comment_pk) {
    document.getElementById(comment_pk + '_comment_dislike_input').value =
        Number(document.getElementById(comment_pk + '_comment_dislike_input').value) - 1;
    ajax_data_POST(urls['undislike_comment'], {'comment_pk': comment_pk})
}

function send_comment(post_pk) {
    let form = document.getElementById(post_pk + '_comment_form')
    const formData = new FormData(form);

    let data = {};

    for (let [key, value] of formData) {
        data[key] = value
    }
    ajaxPOST(urls['send_comment'], {
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
    ajaxPOST(urls['send_answer_to_comment'], {
        'data': data
    })
    setTimeout(update_post_comments, 100, post_pk)
}

function update_post_comments(post_pk) {
    ajaxPOST(urls['get_post_comments'], {
        'data': {'post_pk': post_pk},
        'success': function (data) {
            document.getElementById(post_pk + '_comments').innerHTML = data;
        }
    })
}

let active_comment_answer_form_pk = null;

function determine_active_image(post_pk) {
    let i = 0;
    while (true) {
        let name = post_pk + '_' + i;
        var e = document.getElementById(name);
        if (!e.hidden){
            break;
        }
        if (i > 100){
            throw new Error('impossible to determine a img');
        }
        i++;
    }
    return [i, e];
}

function last_img(post_pk) {
    let [i, e] = determine_active_image(post_pk);

    if (i === 0) {
        return null
    }
    e.hidden = true;
    document.getElementById(post_pk + '_' + (i - 1)).hidden = false
}

function next_img(post_pk) {
    let [i, e] = determine_active_image(post_pk)

    if (document.getElementById(post_pk + '_' + (i + 1)) == null) {
        return null
    }
    e.hidden = true;
    document.getElementById(post_pk + '_' + (i + 1)).hidden = false
}

function smooth_arrow_showing(arrow) {
    arrow.style.opacity = '0.1';

        let arrow_interval = setInterval(function () {
            if (Number(arrow.style.opacity) <= 0) {clearInterval(arrow_interval)}
            arrow.style.opacity = String(Number(arrow.style.opacity) + 0.05);

        }, 50);
        setTimeout(function () {clearInterval(arrow_interval)}, 500);
}

function show_img_change_arrows(post_pk) {
    let [i, e] = determine_active_image(post_pk);

    let show_last_arrow = i !== 0;
    let show_next_arrow = document.getElementById(post_pk + '_' + (i + 1)) !== null;

    if (show_last_arrow) {
        let arrow = document.getElementById(post_pk + '_last_img');
        smooth_arrow_showing(arrow)
    }

    if (show_next_arrow) {
        let arrow = document.getElementById(post_pk + '_next_img');
        smooth_arrow_showing(arrow)

    }
}

function hide_img_change_arrows(post_pk) {
    let next_arrow = document.getElementById(post_pk + '_next_img');
    let last_arrow = document.getElementById(post_pk + '_last_img');
    last_arrow.style.opacity = '0';
    next_arrow.style.opacity = '0';
}

function hide_or_show_post_text(post_pk) {
    let hidden_text = document.getElementById(post_pk + '_hidden_text');
    let ellipsis = document.getElementById(post_pk + '_text_ellipsis');
    ellipsis.hidden = !ellipsis.hidden;
    hidden_text.hidden = !hidden_text.hidden;
}

function hide_or_show_comment_text(comment_pk) {
    let hidden_text = document.getElementById(comment_pk + '_comment_hidden_text');
    let ellipsis = document.getElementById(comment_pk + '_comment_text_ellipsis');
    ellipsis.hidden = !ellipsis.hidden;
    hidden_text.hidden = !hidden_text.hidden;}

function hide_or_show_comment_answers(comment_pk) {
    let hidden_answers = document.getElementById(comment_pk + '_comment_answers');
    let hide_or_show_answers_text = document.getElementById(comment_pk + '_hide_or_show_answers_text');
    hidden_answers.hidden = !hidden_answers.hidden;
    if (hide_or_show_answers_text.innerText === 'show answers') {
        hide_or_show_answers_text.innerText = 'hide answers';
    }
    else {
        hide_or_show_answers_text.innerText = 'show answers';
    }
}

function hide_or_show_comment_answer_form(comment_pk) {
    let form = document.getElementById(comment_pk + '_answer_form');

    if (active_comment_answer_form_pk != null) {
        document.getElementById(active_comment_answer_form_pk + '_answer_form').hidden = true;
    }

    if (form.style.display === 'none') {
        form.style.display = 'block';
        active_comment_answer_form_pk = comment_pk;
    }
    else {
        active_comment_answer_form_pk = null;
    }
}

function subscribe(user_pk) {
    ajax_data_POST(urls['subscribe'], {'user_pk': user_pk})
}

function unsubscribe(user_pk) {
    ajax_data_POST(urls['unsubscribe'], {'user_pk': user_pk })
}

function come(elem) {
    let docViewTop = $(window).scrollTop();
    let docViewBottom = docViewTop + $(window).height();
    let elemTop = $(elem).offset().top;
    let elemBottom = elemTop + $(elem).height();

  return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}
