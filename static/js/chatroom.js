var roomName = "{{ room_id|cut:'-'|escapejs }}";

var chatSocket = new ReconnectingWebSocket(
    'ws://' + window.location.host +
    '/ws/chat/' + roomName + '/');

    chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var command = data['command'];
    if(command == 'old_messages'){
        var messages=data['messeges']
        get_old_messages(messages)
    }
    else if (command == 'new_message'){
        var message=data['message']
        show_new_message(message)
    }
};

function get_old_messages(messages){
    document.querySelector('#chat-message-input').value = ''
    for (var j=0;j<messages.length;j++ ){
            var full_msg=messages[j]['auther']+":"+messages[j]['content']+messages[j]['file_msg_url']
            document.querySelector('#chat-log').value += (full_msg + '\n');
        }
}

function show_new_message(message){
        var full_msg=message['auther']+":"+message['content']+message['file_msg_url']
        document.querySelector('#chat-log').value += (full_msg + '\n');
}

chatSocket.onopen = function(e) {
    chatSocket.send(JSON.stringify({
        'invoke_fn': 'load_old_msg'
    }))
    };

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly '+e);
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};


document.querySelector('#chat-message-submit').onclick = function(e) {
    
    function FileSlicer(file) {
    // randomly picked 1MB slices,
    // I don't think this size is important for this experiment
    this.sliceSize = 1024*1024;  
    this.slices = Math.ceil(file.size / this.sliceSize);

    this.currentSlice = 0;

    this.getNextSlice = function() {
        var start = this.currentSlice * this.sliceSize;
        var end = Math.min((this.currentSlice+1) * this.sliceSize, file.size);
            ++this.currentSlice;

        return file.slice(start, end);
    }
}
    var messageInputDom = document.querySelector('#chat-message-input');
    var message = messageInputDom.value;
    var file=document.getElementById("chat-message-attachment");
    if (file.length==0) {
        var is_file= false
    }
    else { 
        var is_file=true
    }
    if(!is_file){ 
        chatSocket.send(JSON.stringify({
            'invoke_fn': 'add_new_msg',
            'msg_content': message,
            'is_file': is_file
        }));
    }
    else{
        var fReader = new FileReader();
        fReader.readAsDataURL(file.files[0]);
        console.log(file);
        console.log(fReader);
        fReader.onloadend = function(event){
        }
        chatSocket.send(JSON.stringify({
            'invoke_fn': 'add_new_msg',
            'msg_content': message,
            'is_file': is_file,
            'file': file
        }));


/*
        for(var i = 0; i < fs.slices; ++i) {
            socket.send(JSON.stringify({'file_slice':fs.getNextSlice()})); // see below
        }*/
    }
    messageInputDom.value = '';
};