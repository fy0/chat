
var conn = null;
var uid = null;
var username = null;

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
                enter_room(info[1]);
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
