$.fn.disableScroll = function() {
    window.oldScrollPos = $(window).scrollTop();

    $(window).on('scroll.scrolldisabler',function ( event ) {
       $(window).scrollTop( window.oldScrollPos );
       event.preventDefault();
    });
};


eel.expose(no_license);
function no_license(){
    alert("У вас нет лицензии, бот работать не будет. Активация на кнопке 'Лицензия'");
}


eel.expose(add_log);
function add_log(text){
    log = document.getElementById("log");
    log.value = text
}


eel.expose(add_result);
function add_result(text){
    log = document.getElementById("result");
    log.value = text
}


$('#skip').on('click', async function () {
    eel.role_skip()();
});


$('#copy_id').on('click', async function() {
    eel.copy_id()();
});


$('#start').on('click', async function() {
    eel.start_clear_bot()();
    document.getElementById("btn-run").innerHTML = '<button class="btn btn-danger animation-on-hover" type="button" onclick="stop_bot()" id="stop">Выключить</button>'
});


function stop_bot(){
    eel.stop_clear_bot()();
    add_log("");
    document.getElementById("btn-run").innerHTML = '<button class="btn btn-primary animation-on-hover" type="button" onclick="start_bot()" id="start">Запустить</button>'
}


function init(){
    document.getElementById("key").innerHTML = eel.get_id()();
    document.getElementById("version").innerHTML = await eel.get_build_version()();
}


$("#selector").disableScroll();
eel.change_rpc("Removing non-fractions")