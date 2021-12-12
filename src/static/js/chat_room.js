const chat_NS = {}; //namespace

chat_NS.chat_socket = null;



chat_NS.init_chat_socket = function (roomName) {
    if (chat_NS.chat_socket) {
        console.log('socket already has been initialized')
        return;
    }
    chat_NS.chat_socket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
    );

    chat_NS.chat_socket.onopen = function(e) {
        chat_NS.socket_send(JSON.stringify({'command': 'get_room_messages'}))
    }
    
     chat_NS.chat_socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data)
        if(data.command == "new_message"){ //new message received
            chat_NS.add_message_log(data.message);
        }
        if(data.command = "get_room_messages"){ //initialize old messages
            if(data.messages){
                data.messages.reverse().forEach((message)=>{ //add messages to chat
                    chat_NS.add_message_log(message);
                })
            }
        }
    };

    

    chat_NS.chat_socket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };
}

chat_NS.left_room = function(){
    if(chat_NS.chat_socket)
        chat_NS.chat_socket.close();
    window.location.pathname = '/chat/';
}

chat_NS.socket_send = function (data) {
    chat_NS.chat_socket.send(data);
}

chat_NS.add_message_log = function (message) {
    let loggedInUser = localStorage.getItem('username')
    console.log(loggedInUser)
    console.log(message.username)
    console.log(loggedInUser == message.username)
    let html = `
            <div class="message ${(loggedInUser == message.username) ? "info" : "my-message"}">
            <img alt="" class="img-circle medium-image" src="https://www.shareicon.net/data/64x64/2016/01/03/697483_user_512x512.png">

            <div class="message-body">
                <div class="message-info">
                    <h4> ${message.username} </h4>
                    <h5> <i class="fa fa-clock-o"></i> ${globals_NS.datetimeToTimeString(message.created)} </h5>
                </div>
                <hr>
                <div class="message-text">
                    ${message.body}
                </div>
            </div>
            <br>
        </div>
    
    `
    $(".chat-body").append(html);
    $('.chat-body').scrollTop($('.chat-body')[0].scrollHeight); //scroll-down
}

