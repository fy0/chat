
var conn = null;
var uid = null;
var username = null;

function get_user_str(user) {
    return user[1] + ' [' + user[0] + ']';
}

function connect(the_username) {
    disconnect();

    var transports = [
        "websocket", "xhr-streaming", "iframe-eventsource", "iframe-htmlfile", "xhr-polling", "iframe-xhr-polling", "jsonp-polling"
    ];

    conn = new SockJS('http://' + window.location.host + '/ws/api', transports);

    log('Connecting...');

    conn.onopen = function() {
        log('Connected.');
        if (the_username) {
            conn.send(JSON.stringify([
                ['set_username', the_username],
            ]));
        }
    };

    conn.onmessage = function(e) {
        var data = JSON.parse(e.data);
        for (var i in data) {
            var info = data[i];
            if (info[0] == 'user_info') {
                hide_topbox();
                uid = info[1][0];
                username = info[1][1];
                log("登录成功!");
            } else if (info[0] == 'enter_room') {
                if (info[2][0] == uid) {
                    enter_room(info[1]);
                } else {
                    add_msg([0, "系统消息"], get_user_str(info[2]) + " 进入房间");
                }
            } else if (info[0] == 'leave_room') {
                var user_info = info[2];
                if (user_info[0] == uid)
                    do_leave_room();
                else {
                    add_msg([0, "系统消息"], get_user_str(info[2]) + " 离开房间");
                }
            } else if (info[0] == 'say') {
                add_msg(info[1], info[2]);
            }
        }
    };

    conn.onclose = function() {
        log('Disconnected.');
        conn = null;
    };
};

function disconnect() {
    if (conn != null) {
        log('Disconnecting...');

        conn.close();
        conn = null;
    }
};
