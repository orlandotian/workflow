var socket = io.connect('http://' + document.domain + ':' + location.port);
enableSocketio();

function enableSocketio() {

    socket.on('response_update', function (data) {
        alert(data);
        rebindEvent($scope.weeks)
    });
    socket.on('response_message', function (data) {
        var msg = new String(data.msg);
        if (!document.hasFocus()) {
            msgNotice(msg);
        } else {
            createMessage(msg)
        }
    });
}

function sendMessage(msg) {
    socket.emit('event_message', {'msg': msg});
}

function createMessage(msg) {
    var height = Math.random() * 100
    $('#barrage').append('<div class="message" style="top: ' + height + 'px">' + msg + '</div>\n');
    setTimeout(removeChild, 10000)
}

function removeChild() {
    a = document.getElementById('barrage');
    a.removeChild(a.firstElementChild);
}

function msgNotice(msg) {
    if (window.Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function (status) {
            var notice_ = new Notification('新的消息', {body: msg});
            notice_.onclick = function () {
                window.focus();
            }
        });
    }
}