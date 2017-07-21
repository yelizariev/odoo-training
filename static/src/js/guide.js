/**
 * Created by summerrain on 2017/7/21.
 */



function onTransfer(target) {
    if (target == 1) {
        window.location.href = 'http://10.20.113.90:8069/ws_training/list'
    }
    else if (target == 2) {
        window.location.href = 'http://10.20.113.90:8069/ws_training/person?user_id=1'
    }
}
