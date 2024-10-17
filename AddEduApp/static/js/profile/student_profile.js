//function notifyMe () {
//    var notification = new Notification ("Все еще работаешь?", {
//        tag : "ache-mail",
//        body : "Пора сделать паузу и отдохнуть",
//        icon : "https://itproger.com/img/notify.png"
//    });
//}
//function notifSet () {
//    console.log(Notification)
//    if (!('serviceWorker' in navigator) || !('PushManager' in window))
//        alert ("Ваш браузер не поддерживает уведомления.");
//    else if (Notification.permission === "granted")
//        alert('Всё заебись')
//        setTimeout(notifyMe, 2000);
//    else if (Notification.permission !== "denied") {
//        Notification.requestPermission (function (permission) {
//            if (!('permission' in Notification))
//                Notification.permission = permission;
//            if (permission === "granted")
//                alert('Всё заебись')
//                setTimeout(notifyMe, 2000);
//        });
//    }
//}
//window.addEventListener("load", notifSet)