window.onclick=function(event) {
    if (!event.target.offsetParent.classList.contains('dropdown-contact'))
     app.contacts=[]
}


function setActive_chatbox(){
    var btns = document.getElementsByClassName('chat_box');
    var current = document.getElementsByClassName("chat_box active");
    if(current.length!=0)
    current[0].className = current[0].className.replace("active", "");
    for(i=0;i<btns.length;i++){
        if (btns[i].id==('chat'+app.chatroom.currentChatRoomId)){
            app.chat_index=i;
            btns[i].className += " active";
            break;
        }
    }
}

function setActive(target_class,event){
    var btns = document.getElementsByClassName(target_class);
    var current = document.getElementsByClassName(target_class+" active");
    if(current.length!=0)
    current[0].className = current[0].className.replace(" active", "");
    event.target.className +=" active";
    }


function formatDate(formated_Date){
    const date = new Date(formated_Date) // formated_Date - SDK returned date
    var YY=date.getYear().toString().substr(-2)
    var mm=date.getMonth()+1
    var MM=mm>9?mm.toString():'0'+mm.toString()
    var dd=date.getDate()
    var DD=dd>9?dd.toString():'0'+dd.toString()
    var hh=date.getHours()
    var HH=hh>9?hh.toString():'0'+hh.toString()
    var mi=date.getMinutes()
    var MI=mi>9?mi.toString():'0'+mi.toString()
    return `${YY}-${MM}-${DD} ${HH}:${MI}`
}

function formatTime(formated_Date){
    const date = new Date(formated_Date) // formated_Date - SDK returned date
    var hh=date.getHours()
    var HH=hh>9?hh.toString():'0'+hh.toString()
    var mi=date.getMinutes()
    var MI=mi>9?mi.toString():'0'+mi.toString()
    return `${HH}:${MI}`
}




var app=new Vue({
    el:'#page',
    delimiters: ['[{', '}]'],
    components:{
        'chatbox-component':{
            props:['on_chatroom','chatindex','pannel'],
            methods:{
                async renderChatWindow(){
                    app.profile=null;
                    if(this.on_chatroom.has_room_id){
                        app.chatroom={currentChatRoomName:this.on_chatroom.first_arg,currentChatRoomImage:this.on_chatroom.room_image_url,is_group:this.on_chatroom.is_group,chatmessages:[],currentChatRoomId:this.on_chatroom.room_id};
                        for(i=0;i<this.on_chatroom.messages.length;i++){
                            data=this.on_chatroom.messages[i]
                        await app.chatroom.chatmessages.push({auther_name: data.auther_name, is_send: data.sender==user, time_stamp: data.time_stamp, content: data.content, file_msg_link: data.file_msg_link});    
                        }
                        setActive_chatbox();
                        setScroll()    
                    }else{
                        app.findRoomId(this.on_chatroom)
                    }
                }
            },
            template:
                 ` <div class="row border" :id="pannel + on_chatroom.room_id" :class="pannel+'_box'">
                <div class="img_box ">
                    <img :src="on_chatroom.room_image_url"  class="rounded-circle border" width="45" height="45">
                </div>
                <a style="text-decoration: none;" class="detail_box container-fluid" v-on:click="renderChatWindow" >
                    <div class="row ">
                    <div class="box_top_left col-8">{{ on_chatroom.first_arg }}</div>
                    <div class="box_top_right col-4">{{ on_chatroom.second_arg }}</div>
                    <div class="box_bottom_left col-12">{{ on_chatroom.third_arg }}</div>
                    </div>
                </a>
            </div>`
        },   
        'contact-component':{
            props:['on_chatroom'],
            template:
            ` <div class="row chat_box  border " >
                <div class="img_box ">
                    <img :src="on_chatroom.room_image_url"  class="rounded-circle border" width="45" height="45">
                </div>
                <a style="text-decoration: none;" class="detail_box container-fluid" >
                    <div class="row ">
                    <div class="box_top_left col-8">{{ on_chatroom.first_arg }}</div>
                    <div class="box_top_right col-4">{{ on_chatroom.second_arg }}</div>
                    <div class="box_bottom_left col-12">{{ on_chatroom.third_arg }}</div>
                    </div>
                </a>
            </div>`
        },
        'searchbar-component':{
            props:['value',],
            methods:{
                onRenderSearchNames(){
                    app.renderSearchNames()
                }
            },
            template:
        `<div class='search_class'>
            <div class="input-group">
                <input type="text" class="inline_a" placeholder="Search.." name="username_substring"  :value="value" @input="$emit('input', $event.target.value)" @keyup="onRenderSearchNames" />
                <button class="input-group-addon inline_b"><i class="fa fa-search"></i></button>
             </div>
        </div>`
        },
        'message-component':{
            props:['chatmessage','is_group'],
            template:
        `   <div class="row">
            <div class="col-12" v-if='chatmessage.is_notification'>
                <div class="notification"> {{chatmessage.notification}} </div>
            </div>
            <div class="col-12" v-else>
                <div :class="chatmessage.is_send? 'send':'receive'" class="container-fluid">
                    <div class="row auther" v-show="!chatmessage.is_send && is_group"> {{ chatmessage.auther_name }} </div>
                    <div class="row  content"> {{chatmessage.content}} </div>
                    <div v-show="chatmessage.file_msg_link !=''" class="row file_box">
                        <img  class="file_link" :src="chatmessage.file_msg_link" >  
                    </div>
                    <div class="row timebox"> 
                        <div class='time'>{{ chatmessage.time_stamp }} </div>
                    </div>
                </div>    
            </div>
        </div>`
        }
    },
    data:{
        is_search:false,
        user_sub_str:"",
        chatroom_url:'http://'+window.location.host+'/api/v1/findusers/',
        message_url:'http://'+window.location.host+'/api/v2/messages/?roomid=',
        chatroom_find_url:'http://'+window.location.host+'/api/v2/ChatRoom/',
        chatrooms:[],
        contactlist:[],
        searchlist:[],
        chat_index:'',
        chatSocket:null,
        form:false,
        new_group:{group_name:'', added_contacts:[]},
        new_contact:{first_name:'', last_name:'', username:''},
        is_search:false,
        chatroom:{currentChatRoomName:'',currentChatRoomImage:'',is_group:false,chatmessages:[],currentChatRoomId:-1},
        is_group:false,
        chatmessages:[],
        message_content:'',
        files:[],
        profile:null,
        currentTab:'Home',
        pannel:'chat',
        contacts:[],
        error_message:''
    },  
    methods: {
        displayProfile(room_id){

            var api_url='http://'+window.location.host+'/api/v2/profile/'+room_id
            var is_self=false
            if (room_id=='')
            is_self=true
            axios.get(api_url)
            .then( (response)=>{
                app.profile={
                   'data': response.data,
                   'is_self': is_self
                };
                if(app.profile.data.members) {
                    for(var i=0; i<app.profile.data.members.length; i++){
                        var a=app.profile.data.members[i];
                        app.profile.data.members[i]={room_image_url:a.img_link, first_arg: a.full_name, second_arg:'',third_arg:a.username,has_room_id:false, username:a.username ,is_group:false};
                    }
                    }
            }).catch(function(error){
                console.log(error);
            })
        },
        async renderChat(){
            var chatroom_message_url='http://'+window.location.host+'/api/v2/chatroomapi/';
            await axios.get(chatroom_message_url)
            .then((response)=>{
                this.user_sub_str="";
                this.chatrooms=[];
                for(var i=0; i<response.data.length; i++){
                    var a=response.data[i];
                    p={roomie:a.roomie,is_group:a.group,group_admins:a.group_admins, second_arg:formatTime(a.lastping), messages:a.messages, third_arg:a.lastmsg, room_image_url:a.room_image_url, first_arg:a.guest_name, room_id:a.id,has_room_id:true};
                    this.chatrooms.push(p);
                }
            }).catch(function(error){
                console.log(error)
            })
            setActive_chatbox()
        },
        saveEditedProfile(){
            var profile_url='http://'+window.location.host+'/api/v3/profileapi/';
            var name=this.profile.data.name.split(' ')
            var f_name=''
            for(i=0;i<name.length-1;i++)
            f_name+=name[i]
            var l_name=name[name.length-1]
            var status=this.profile.data.status
            var email=this.profile.data.email
            let formData = new FormData();
            rawData={
                'host': {
                    "first_name": f_name,
                    "last_name": l_name,
                    "email":email
                },
                "status":status
                }
            rawData = JSON.stringify(rawData)
            formData.append('data',rawData );
            if(profile_image_file)
            formData.append('image',profile_image_file, profile_image_file.name);            
            let req = {
                url:profile_url,
                method: 'PUT',
                data:formData,
                headers: {'X-CSRFTOKEN': csrftoken,'Content-Type': 'multipart/form-data'}
              } 
            axios(req)
            .then( function(response){
                resetAllProfileInputs()
            }).catch(function(error){
                console.log(error)
            })             
        },
        renderContact(){
            this.user_sub_str="";
            var contact_url='http://'+window.location.host+'/api/v3/Contact/';
            axios.get(contact_url)
            .then((response)=>{
                this.contactlist=[];
                for(var i=0; i<response.data.length; i++){
                    var a=response.data[i];
                    this.contactlist.push({room_image_url:a.room_image_url, first_arg: a.full_name, second_arg:'',third_arg:a.username,has_room_id:false, username:a.username ,is_group:false});
                }
            }).catch(function(error){
                console.log(error)
            })
        }, 
        renderSearch(){
            this.form=false;
            this.user_sub_str="";
            app.searchlist=[];
        },
        renderSearchNames(){
            var c_url='http://'+window.location.host+'/api/v1/findusers/'+app.user_sub_str
            axios.get(c_url)
            .then(function(response){
                app.searchlist=[];
                for(var i=0; i<response.data.length; i++){
                    var a=response.data[i];
                    app.searchlist.push({room_image_url:a.img_link, username:a.username , first_arg: a.username , second_arg:'',third_arg: a.full_name,has_room_id:false, is_group:false});
                }
            }).catch(function(error){
                console.log(error)
            })
        },
        createGroup(){
            var chatroom_url='http://'+window.location.host+'/api/v2/chatroomapi/'
            let req = {
                url:chatroom_url,
                method: 'POST',
                data: {
                    "group_with_current_user":app.new_group.group_name,
                    "added_contacts":app.new_group.added_contacts
                },
                headers: {'X-CSRFTOKEN': csrftoken}
              }  
            axios(req)
            .then( function(response){
                app.new_group.group_name='';
                app.renderChat();
                app.form=false;
            }).catch(function(error){
                console.log(error)
            })              
        },
          createContact(){
            var contact_url='http://'+window.location.host+'/api/v3/Contact/'
            let req = {
                url:contact_url,
                method: 'POST',
                data: {
                    "first_name":app.new_contact.first_name,
                    "last_name":app.new_contact.last_name,
                    "username":app.new_contact.username
                },
                headers: {'X-CSRFTOKEN': csrftoken}
              } 
            axios(req)
            .then( function(response){
                app.new_contact.first_name='';
                app.new_contact.last_name='';
                app.new_contact.username='';
                app.renderContact();
                app.form=false;
            }).catch(function(error){
                app.error_message=error.response.data.message;
                console.log(error.response.data.message)
            })              
        }, 
        findRoomId(arg){
            var flag=false;
                for(i=0;i<this.chatrooms.length;i++){
                  if(!this.chatrooms[i].is_group && (this.chatrooms[i].roomie.filter( i=> i.username==arg.username).length>0))
                    {
                        flag=true;
                        app.chatroom={currentChatRoomName:this.chatrooms[i].first_arg,currentChatRoomImage:this.chatrooms[i].room_image_url,is_group:this.chatrooms[i].is_group,chatmessages:this.chatrooms[i].messages,currentChatRoomId:this.chatrooms[i].room_id,username:''}; 
                        break;
                    }
                }
                if(!flag){
                    app.chatroom={currentChatRoomName:arg.first_arg,currentChatRoomImage:arg.room_image_url,is_group:arg.is_group,chatmessages:[],currentChatRoomId:-1,username:arg.username}; 
                }
            
        },
        displayDropdown(){
            if(this.contacts.length==0){
                var contact_url='http://'+window.location.host+'/api/v3/Contact/'+'?roomid='+this.chatroom.currentChatRoomId
                axios.get(contact_url)
                .then( function(response){
                    app.contacts=[];
                    if(response.data.length==0)
                    app.contacts.push({ blank_arg:'Nothing to add'});
                    for(var i=0; i<response.data.length; i++){
                        var a=response.data[i];
                        app.contacts.push({room_image_url:a.room_image_url, first_arg: a.full_name, third_arg:a.username});
                    }
                }).catch(function(error){
                    console.log(error)
                })    
            }else{
                app.contacts=[]
            }
        },
        toggleCheckBox(id) {
            document.getElementById('chatbox_'+id).checked = !document.getElementById('chatbox_'+id).checked;
          },
        loadapp(){
           this.renderChat();
           this.renderContact();
           this.displayProfile('');
        },
        addToGroup(username){
            var chatroom_url='http://'+window.location.host+'/api/v2/chatroomapi/'+this.chatroom.currentChatRoomId
            let req = {
                url:chatroom_url,
                method: 'PUT',
                data: {
                    "newroomie":username
                },
                headers: {'X-CSRFTOKEN': csrftoken }
              }            
            axios(req)
            .then( function(response){
                app.contacts=[];
                app.displayDropdown();
                var rawData={
                    'type':'chat_notification',
                    'username': username,
                    'operation': 'add',
                    'groupid': app.chatroom.currentChatRoomId
                }
    
                rawData = JSON.stringify(rawData)
                app.chatSocket.send(rawData)
            }).catch(function(error){
                console.log(error)
            })              
        },
        addFiles(event){
            this.files=[]
            for(var i=0;i<event.target.files.length;i++){
                this.files.push(event.target.files[i]);
            }
        },
        manageMessage(event){
            if(!event.shiftKey)
                this.sendMessage(event);
        },
        sendMessage(event){
            var is_file=this.files.length!=0
            var file_size=0
            var upload_status=''
            var file_name=''
            if(is_file){
        //            app.chatSocket.send(this.files[0],{ binary: true });                                        
                var file_size=this.files[0].size;
                var upload_status='started';
                var file_name=this.files[0].name;
            }
            var rawData={
                'type':'message',
                'message_content': this.message_content,
                'is_file': is_file,
                'file_size':file_size,
                'upload_status':upload_status,
                'file_name':file_name,
                'chatroom':app.chatroom.currentChatRoomId,
                'receiver':app.chatroom.username
            }

            rawData = JSON.stringify(rawData)
            if(this.message_content!='' || this.files.length!=0){
                if(app.chatSocket){
                        app.chatSocket.send(rawData);
                        if (is_file)
                            app.chatSocket.send(this.files[0],{ binary: true });  
                            for( i=1;i<this.files.length;i++){
                                file_size=this.files[i].size;
                                upload_status='started';
                                file_name=this.files[i].name;
                
                                var blankrawData={
                                    'type':'message',
                                    'message_content': '',
                                    'is_file': is_file,
                                    'file_size':file_size,
                                    'upload_status':upload_status,
                                    'file_name':file_name,
                                    'chatroom':app.chatroom.currentChatRoomId,
                                    'receiver':app.chatroom.currentChatRoomName
                                }
                                app.chatSocket.send(JSON.stringify(blankrawData));
                                app.chatSocket.send(this.files[i],{ binary: true });  
                            }
                    }
                else{
                    alert("ChatRoom doesn't extst.\n Refresh this Page.");
                }
            }
            this.message_content=''
            this.files=[]
            
        },

    },
    mounted(){
        this.loadapp();
        var str='ws://' + window.location.host + '/ws/chat/' + user + '/';
        this.chatSocket=new ReconnectingWebSocket(str);

        this.chatSocket.onmessage = function(e) {
            var data = JSON.parse(e.data).message;
            if(app.chatroom.currentChatRoomId==data['room_id']){
                if(data['type']=='notification'){
                    console.log('**************')
       //             app.chatroom.chatmessages.push({is_notification:true, notification:"You have been added to this group"});    
                }
                else
                app.chatroom.chatmessages.push({is_notification:false,auther_name: data['auther'], is_send: data['auther']==user, time_stamp: data['timestamp'], content: data['content'], file_msg_link: data['file_msg_url']});    
                setScroll()    
            }
            app.renderChat()
        };
    },
    updated(){
    //    setActive('chat_box')
        document.getElementsByClassName('loading')[0].classList+=' hide';  
    }
})


