function connect(deviceId) {
    $.ajax({
        type: 'GET', //тип запроса
        url: '/connect', // адрес, на который отправлен запрос
        dataType: 'json', //тип данных, ожидаемый от сервера
        conectType:'application/json', //тип передаваемых данных
        data:{ //данные запроса
            "deviceId": deviceId
        },
        success: function (response) {
            location.reload();
        }
    });
};

function disconnect(deviceId) {
    $.ajax({
        type: 'GET', //тип запроса
        url: '/disconnect', // адрес, на который отправлен запрос
        dataType: 'json', //тип данных, ожидаемый от сервера
        conectType:'application/json', //тип передаваемых данных
        data:{ //данные запроса
            "deviceId": deviceId
        },
        success: function (response) {
            location.reload();
        }
    });
};

function on(deviceId) {
    $.ajax({
        type: 'GET', //тип запроса
        url: '/on', // адрес, на который отправлен запрос
        dataType: 'json', //тип данных, ожидаемый от сервера
        conectType:'application/json', //тип передаваемых данных
        data:{ //данные запроса
            "deviceId": deviceId
        },
        success: function (response) {
            location.reload();
        }
    });
};

function off(deviceId) {
    $.ajax({
        type: 'GET', //тип запроса
        url: '/off', // адрес, на который отправлен запрос
        dataType: 'json', //тип данных, ожидаемый от сервера
        conectType:'application/json', //тип передаваемых данных
        data:{ //данные запроса
            "deviceId": deviceId
        },
        success: function (response) {
            location.reload();
        }
    });
};