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
    console.log('WAW WTF')
}
