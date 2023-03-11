function subscribe(user_pk) {
    ajaxPOST(urls['subscribe'], {
        'data': {'user_pk': user_pk}
    })
    document.getElementById("sub_btn_inactive").style.display = 'none'
    document.getElementById("sub_btn_active").style.display = 'inline'
}

function unsubscribe(user_pk) {
    ajaxPOST(urls['unsubscribe'], {
        'data': {'user_pk': user_pk}
    })
    document.getElementById("sub_btn_inactive").style.display = 'inline'
    document.getElementById("sub_btn_active").style.display = 'none'
}

// let show_change_ava_button_process = false
//
// function show_change_ava_button() {
//     if (!show_change_ava_button_process) {
//         let pos = document.getElementById('user-ava').getBoundingClientRect()
//         let change_btn = document.getElementById("change_ava_btn")
//         change_btn.style.display = 'inline-block'
//         change_btn.style.left = String(pos.left)
//         change_btn.style.top = String(pos.top)
//
//         function tick() {
//             let style = getComputedStyle(change_btn);
//             let left = Number(style.top);
//             change_btn.style.top = String(1 + left);
//             let opacity = Number(style.opacity);
//             console.log('UP')
//             change_btn.style.opacity = String(opacity + 0.05) // total 20 ticks
//         }
//         let interval = setInterval(tick, 0.025) // total 0.5 sec
//         setTimeout(function () {
//             clearInterval(interval);
//             show_change_ava_button_process = false
//         }, 0.5)
//     }
// }
