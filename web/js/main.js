$.fn.disableScroll = function() {
    window.oldScrollPos = $(window).scrollTop();

    $(window).on('scroll.scrolldisabler',function ( event ) {
       $(window).scrollTop( window.oldScrollPos );
       event.preventDefault();
    });
};
type = ['primary','info','success','warning','danger'];



$('#copy_id').on('click', async function() {
    eel.copy_id()();
});


eel.expose(set_status);
function set_status(work){
    if(work){
        document.getElementById("status").innerHTML = 'Статус: <span style="color:#28a745">Работает</span>';
    } else {
        document.getElementById("status").innerHTML = 'Статус: <span style="color:#dc3545">Не работает</span>';
    }
}


eel.expose(no_license);
function no_license(){
    alert("У вас нет лицензии, бот работать не будет. Активация на кнопке 'Лицензия'");
}


eel.expose(got_update);
function got_update(name){
    alert("Успешно установилось обновление под названием " + name + ", старый EXE бота можно удалить. На ДАННЫЙ момент запущена старая версия бота");
}


eel.expose(set_accepted);
function set_accepted(value){
    document.getElementById("accepted_roles").innerHTML = value;
}


eel.expose(set_asked);
function set_asked(value){
    document.getElementById("asked_roles").innerHTML = value;
}


eel.expose(showNotification)
function showNotification(from, align, type, text){
    	color = Math.floor((Math.random() * 4) + 1);

    	$.notify({
        	icon: "tim-icons icon-bell-55",
        	message: text

        },{
            type: type,
            timer: 5000,
            placement: {
                from: from,
                align: align
            }
        });
}


async function init(){
    eel.init_main();
    document.getElementById("key").innerHTML = eel.get_id()();
    document.getElementById("version").innerHTML = await eel.get_build_version()();
}


eel.expose(set_settings);
function set_settings(discord_token, telegram_token, telegram_id, min_delay, max_delay, channel, anti_flood, only_form, ask_stats, allow_leader, hide_browser, key, server) {
      document.getElementById("discord_token").value = discord_token;
      document.getElementById("telegram_token").value = telegram_token;
      document.getElementById("telegram_id").value = telegram_id;
      document.getElementById("min_delay").value = min_delay;
      document.getElementById("max_delay").value = max_delay;
      document.getElementById("channel").value = channel;
      document.getElementById("anti_flood").checked = anti_flood;
      document.getElementById("only_form").checked = only_form;
      document.getElementById("ask_stats").checked = ask_stats;
      document.getElementById("allow_leader").checked = allow_leader;
      document.getElementById("hide_browser").checked = hide_browser;
      document.getElementById("key").innerHTML = key;
      document.getElementById("server").value = server;
}


$('#save').on('click', async function () {
      let discord_token = document.getElementById("discord_token").value;
      let telegram_token = document.getElementById("telegram_token").value;
      let telegram_id = document.getElementById("telegram_id").value;
      let min_delay = document.getElementById("min_delay").value;
      let max_delay = document.getElementById("max_delay").value;
      let channel = document.getElementById("channel").value;
      let anti_flood = document.getElementById("anti_flood").checked;
      let only_form = document.getElementById("only_form").checked;
      let ask_stats = document.getElementById("ask_stats").checked;
      let allow_leader = document.getElementById("allow_leader").checked;
      let hide_browser = document.getElementById("hide_browser").checked;
      let server = document.getElementById("server").value;

      eel.save_settings(discord_token, telegram_token, telegram_id, min_delay, max_delay, channel, anti_flood, only_form, ask_stats, allow_leader, hide_browser, server)();
    });


function start_bot(){
    eel.start_bot()();
    document.getElementById("btn-run").innerHTML = '<button class="btn btn-danger animation-on-hover" type="button" onclick="stop_bot()" id="stop">Выключить</button>'
}


eel.expose(stop_bot)
function stop_bot(){
    eel.stop_bot()();
    document.getElementById("btn-run").innerHTML = '<button class="btn btn-primary animation-on-hover" type="button" onclick="start_bot()" id="start">Запустить</button>'
}


$("#selector").disableScroll();

init();
eel.change_rpc("Catching roles")