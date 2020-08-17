var r = window.location.href.split("?room=")[1];
var username = "";
var isOwner = false;
var isMod = false;
var count = 0;
$("#box-2-x").on("click", function(){
    $("#box-2").hide();
});
$("#log-btn").on("click", function(){
    if($(this).text() == "Login") {
        $("#box-2").show();
        $("#box-2").show();
        $("#register").hide();
        $("#join").hide();
        $("#login").show();
        $("#create").hide();
        $("#ul").hide();
        $("#banlist").hide();
    }
    if ($(this).text() == "Logout"){
        var m = {"logout": 1}
        var s = JSON.stringify(m);
        ws.send(s);
        $(this).text("Login");
        $("#join-btn").hide();
        $("#userlist-btn").hide();
        $("#modlist-btn").hide();
        $("#reg-btn").show();
        $("#login-status").text("");
        $("#box").html("");
        message_index = 0;


    }
})
$("#submit-login-btn").on("click", function(){
    var email = $("#log-email").val();
    $("#log-email").val("");
    var password = $("#log-password").val();
    $("#log-password").val("");
    var m = {"login":1, "email": email, "password": password};
    var s = JSON.stringify(m);
    ws.send(s);
});
$("#submit-join-btn").on("click", function(){
    var r = $("#j-room");
    var rv = r.val();
    r.val("");
    var m = {"join": 1, "room": rv};
    var s = JSON.stringify(m);
    ws.send(s);
})
$("#userlist-btn").on("click", function(){
    $("#box-2").show();
    $("#register").hide();
    $("#join").hide();
    $("#login").hide();
    $("#create").hide();
    $("#ul").show();
    $("#banlist").hide();

});

$("#join-btn").on("click", function(){
    $("#box-2").show();
    $("#register").hide();
    $("#join").show();
    $("#login").hide();
    $("#create").hide();
    $("#ul").hide();
    $("#banlist").hide();
    $("#create").hide();
});
$("#reg-btn").on("click", function(){
    $("#box-2").show();
    $("#register").show();
    $("#join").hide();
    $("#login").hide();
    $("#create").hide();
    $("#ul").hide();
    $("#banlist").hide();
    $("#create").hide();
});
$("#create-room-btn").on("click", function(){
    $("#box-2").show();
    $("#register").hide();
    $("#join").hide();
    $("#login").hide();
    $("#create").hide();
    $("#ul").hide();
    $("#banlist").hide();
    $("#create").show();
});
$("#banlist-btn").on("click", function(){
    $("#box-2").show();
    $("#register").hide();
    $("#join").hide();
    $("#login").hide();
    $("#create").hide();
    $("#ul").hide();
    $("#banlist").show();
    $("#create").hide();
})
$("#submit-create-btn").on("click", function(){
    var c = $("#cr");
    var cr = c.val();
    c.val("");
    var m = {"createroom": 1, "room": cr};
    var s = JSON.stringify(m);
    ws.send(s);
});
$("#msg").keyup(function(e){
    if (e.which == 13){
        var message = $("#msg")
        if (message.val().length === 0 || message.val() == " " || message.val() == ""){
            message.val("")
        } else{
            var v = message.val();
            var m = {"message": 1, "body": v};
            var s = JSON.stringify(m);
            ws.send(s);
            message.val("");   
        }

        return false;
    }
});
$("#submit-register-btn").on("click", function(){
    var email = $("#reg-email").val();
    var user = $("#reg-username").val();
    var password = $("#reg-password").val();
    var m = {
        "register": 1,
        "email": email,
        "username": user,
        "password": password
    }
    var s = JSON.stringify(m);
    ws.send(s);
});
$("#alert-x").on("click", function() {
    $("#alert").hide();
});
function addMessage(user, uuid, mid, ts, message) {
    var element = document.createElement("div");
    element.setAttribute("data-msgid", mid);
    element.setAttribute("class", "message border-2 border-solid border-gray-300 rounded shadow mx-3 my-3 h-32");
    element.setAttribute("data-uuid", uuid);
    element.setAttribute("data-user", user);
    var time = document.createElement("span");
    time.id = "time";
    time.innerText = ts;
    var modb = document.createElement("div");
    modb.setAttribute("class", "modbuttons");
    var b = document.createElement("span");
    var delmsg = document.createElement("span");
    delmsg.id = "mod-delete-message"
    delmsg.innerText = "Delete Message";
    delmsg.setAttribute("class", "message-delete");
    b.id = "mod-ban";
    b.setAttribute("class", "message-ban");
    b.innerText = "Ban";
    var deluser = document.createElement("span")
    deluser.setAttribute("class", "message-delete-user");
    deluser.id = "mod-delete";
    deluser.innerText = "Delete";
    var img = document.createElement("img");
    img.src = "/profile/image/" + user + ".jpg";
    img.id = 'profileimg';
    img.setAttribute("class", "rounded shadow border-solid border-gray-300 border-2 h-12 w-12")
    var u = document.createElement("span");
    u.id = "user";
    u.innerText = user;
    var msg = document.createElement("span");
    msg.id = "text";
    msg.innerHTML = message;
    element.appendChild(time);
    modb.appendChild(deluser);
    modb.appendChild(b);
    modb.appendChild(delmsg);
    element.appendChild(modb);
    element.appendChild(img);
    element.appendChild(u);
    element.appendChild(msg);
    document.getElementById("box").appendChild(element);
    $(deluser).on("click", function(){
        var parent = $(this).parent();
        var parent = $(parent).parent();
        var u = $(parent).data("user");
        console.log(u)
        var m = {
            "deleteuser": 1,
            "name": u
        }
        var s = JSON.stringify(m);
        ws.send(s);
    })
    $(delmsg).on("click", function(){
        var parent = $(this).parent();
        var parent = $(parent).parent();
        var id = $(parent).data("msgid");
        var m = {
            "delete": 1,
            "id": id
        }
        var s = JSON.stringify(m);
        ws.send(s);
    })
    
}

function addBanlist(name, id) {
    var div = document.createElement("div");
    div.setAttribute("class", "my-3");
    div.setAttribute("data-ban-user", name);
    div.setAttribute("data-ban-id", id);
    var user = document.createElement("span");
    user.setAttribute("class", "mx-1 my-1 shadow");
    user.innerText = name;
    var button = document.createElement("span");
    button.setAttribute("class", "unban text-white bg-green-300 border-2 border-solid border-green-200 py-1 px-1 shadow mx-1 hover:bg-green-500");
    button.innerText = "Unban";
    div.appendChild(user);
    div.appendChild(button);
    var bl = document.getElementById("banlist");
    bl.appendChild(div);
    $(button).on("click", function() {
        var parent = $(this).parent()
        var id = $(parent).data("ban-user");
        var name = $(parent).data("ban-id");
        var m = {
            "unban": 1,
            "target": name,
            "id": id
        }
        var s = JSON.stringify(m);
        ws.send(s);
    })
}
function hideModButtons() {
    var buttons = $(".modbuttons");
    for (var i = 0; i < buttons.length; i++) {
        var button = buttons[i];
        $(button).hide();
    }
}
function showModbuttons() {
    var buttons = $(".modbuttons");
    for (var i = 0; i < buttons.length; i++) {
        var button = buttons[i];
        $(button).show();
    }
}
function hideOwnerButtons() {
    var buttons = $(".ownerbuttons");
    for (var i = 0; i < buttons.length; i++) {
        var button = buttons[i];
        $(button).hide();
    }
}
function showOwnerbuttons() {
    var buttons = $(".ownerbuttons");
    for (var i = 0; i < buttons.length; i++) {
        var button = buttons[i];
        $(button).show();
    }
}

function removeById(id){
    $(".message").filter(function(){
        return $(this).data("msgid") == id;
    }).remove(); 
}
function removeByUser(user) {
    $(".message").filter(function(){
        return $(this).data("user") == user;
    }).remove();
}
function removeUl(user) {
    $(".userlist-entry").filter(function(){
        return $(this).data("ul-user") == user;
    }).remove();
}
function addUserlist(user) {
    var entry = document.createElement("p");
    entry.setAttribute("class", "userlist-entry                                ");
    entry.setAttribute("data-ul-user", user);
    entry.innerText = user;
    var userlist = document.getElementById("ul");
    userlist.appendChild(entry)
}
function removeMod(user) {
    $(".mod").filter(function(){
        return $(this).data("ul-user") == user;
    }).removeClass("mod");
}
function addMod(user) {
    $(".userlist-entry").filter(function(){
        return $(this).data("ul-user") == user;
    }).addClass("mod");
}
function formatTime(ts) {
    var date = new Date(ts * 1000);
    var h = date.getHours();
    var m = date.getMinutes();
    var s = date.getSeconds();
    var month = date.getMonth() + 1;
    var day = date.getDay();
    var yr = date.getFullYear();
    return h + ":" + m + ":" + s + " - " + month + "/" + day + "/" + yr;
}
(function(){
    isLoggedIn = false;
    username = null;
    isJoinedRoom = false;
    ws = new WebSocket("wss://anichat.ga:9000/serv");
    ws.onopen = function() {
        console.log("connected to server!");
    }
    ws.onmessage = function(e){
        var j = JSON.parse(e.data);
        console.log(e.data);
        if (j.login) {
            isLoggedIn = true;
            username = j.name;
            if (!r == undefined) {
                var m = {"join": 1, "room": r};
                var s = JSON.stringify(m);
                ws.send(s);
            }
            $("#log-btn").text("Logout");
            $("#log-btn").css("color", "red");
            $("#reg-btn").hide();
            $("#join-btn").show();
            $("#userlist-btn").show();
            $("#box-2").hide();
            $("#status-login").text("");

        } 
        if(j.login == 0){
            $("#status-login").text(j.error);
            username = null;
        }
        if (j.register){
            $("#box-2").hide();
            $("#status-register").text("");
        }
        if(j.register) {
            $("#status-register").text(j.error);
        }
        if(j.joined) {
            $("#box").html("")
            var his = {"history": 1, "limit": 500, "start_at": 0};
            var mods = {"mods": 1};
            var ul = {"userlist": 1};
            var h = JSON.stringify(his);
            var m = JSON.stringify(mods);
            var u = JSON.stringify(ul);
            ws.send(h);
            ws.send(m);
            window.setTimeout(function(){
                ws.send(u);
            }, 5000);
            isJoinedRoom = true;
            $("#status-join").text("");
            $("#msg").show()
            $("#userlist").html("");
            $("#banlist").html("");
            $("#userlist-btn").show();
            $("#count").text(0);
            hideModButtons();
            hideOwnerButtons();
        }
        if(j.joined == 0) {
        
           $("#status-join").text(j.error);
        }
        if(j.message) {
            var name = j.name;
            var mid = j.mid;
            var id = j.id;
            var ts = formatTime(j.time);
            var body = j.body;
            addMessage(name, id, mid, ts, body);
            var div = document.getElementById("box");
            div.scrollTop = div.scrollHeight;


        }
        if(j.ul){
            count++;
            addUserlist(j.name);
            $("#count").text(count);
        }
        if (j.history) {
            var name = j.name;
            var id = j.id;
            var mid = j.mid;
            var ts = formatTime(j.time);
            var body = j.body;
            addMessage(name, id, mid, ts, body);
            var div = document.getElementById("box");
            div.scrollTop = div.scrollHeight;
        }
        if (j.delete) {
            removeByUser(j.name);
        }
        if(j.deletemessage){
            var id = j.id;
            removeById(id);
        }
        if (j.left){
            count--;
            removeUl(j.name);
            $("#count").text(count);
        };
        if(j.modded) {
            if (j.name == username) {
                isMod = true;
                $("#banlist-btn").show();
                showModbuttons();
            }
            addMod(j.name);
        }
        if(j.join) {
            if (!username == j.name) {
                addUserlist(j.name);
                count++;
                $("#count").text(count);
            }
        }
        if(j.mods) {
            if (j.owner) {
                var mod = j.modname;
                if(mod == username) {
                    isOwner = true;
                    showOwnerbuttons();
                }
            }
            if (j.modname == username) {
                $("#banlist-btn").show();
                showModbuttons();
                if (!isOwner) {
                    isMod = true;
                }
            }
            addMod(j.modname);
        }
        if(j.demodded) {
            if(j.name == username) {
                isMod = false;
                hideModButtons();
                $("#banlist-btn").hide();
            }
            removeMod(j.name);
        }
        if(j.banned) {
            $("#msg").hide();
            $("#alert-text").text("you are banned from this room");
            $("#alert").show();
        }
        if(j.ban) {
            var name = j.name;
            var id = j.id;
            addBanlist(name, id)
        }
    }
    ws.onclose = function() {
        ws.close();
    }
})();
