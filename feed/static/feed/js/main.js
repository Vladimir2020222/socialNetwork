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

function show_img_change_arrows(post_pk) {
    let [i, e] = determine_active_image(post_pk)

    let show_last_arrow = i !== 0
    let show_next_arrow = document.getElementById(post_pk + '_' + (i + 1)) !== null

    if (show_last_arrow) {
        let last_arrow = document.getElementById(post_pk + '_last_img')
        last_arrow.style.opacity = '0.01';

        let last_arrow_interval = setInterval(function () {
            if (last_arrow.style.opacity === '0') {
                clearInterval(last_arrow_interval)
            }
            last_arrow.style.opacity = String(Number(last_arrow.style.opacity) + 0.05)

        }, 50)
        setTimeout(function () {clearInterval(last_arrow_interval)}, 750)
    }

    if (show_next_arrow) {
        let next_arrow = document.getElementById(post_pk + '_next_img')
        next_arrow.style.opacity = '0.01';

        let next_arrow_interval = setInterval(function () {
            if (next_arrow.style.opacity === '0') {
                clearInterval(next_arrow_interval)
            }
            next_arrow.style.opacity = String(Number(next_arrow.style.opacity) + 0.05)

        }, 50)
        setTimeout(function () {clearInterval(next_arrow_interval)}, 750)
    }
}

function hide_img_change_arrows(post_pk) {
    let next_arrow = document.getElementById(post_pk + '_next_img')
    let last_arrow = document.getElementById(post_pk + '_last_img')
    last_arrow.style.opacity = '0';
    next_arrow.style.opacity = '0';



}
