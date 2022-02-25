$.fn.disableScroll = function() {
    window.oldScrollPos = $(window).scrollTop();

    $(window).on('scroll.scrolldisabler',function ( event ) {
       $(window).scrollTop( window.oldScrollPos );
       event.preventDefault();
    });
};


$('#copy_id').on('click', async function() {
    eel.copy_id()();
});


eel.expose(no_license);
function no_license(){
    alert("У вас нет лицензии, бот работать не будет. Активация на кнопке 'Лицензия'");
}


function init(){
    document.getElementById("version").innerHTML = await eel.get_build_version()();
    document.getElementById("key").innerHTML = eel.get_id()();
}


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


eel.change_rpc("Auto chat moderation")