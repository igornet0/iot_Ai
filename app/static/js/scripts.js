$(document).ready(function(a){
    var editMode = false;

    function get_schedule(deviceId){
        $.ajax({
            url: '/get-schedule',
            type: 'POST',
            data: {device_id: deviceId},
            success: function(data) {
            if (!data.length) {
                $('.modal-body').html('<p>Schedule not found</p>');
                return;
            }
            var scheduleHtml = '<ul class="list-group">';
            data.forEach(function(item) {
                scheduleHtml += `<li class="list-group-item" data-id="${item.id}">${item.time_on} - ${item.time_off}</li>`;
            });
            scheduleHtml += '</ul>';
            $('.modal-body').html(scheduleHtml);
            }
        });
    }
    
    $('#addButton').click(function(e) {
        $('.modal-body').html(`
            <form id="addForm">
                Time start: <input type="time" name="time_start"/><br/>
                Time end: <input type="time" name="time_end"/><br/>
                <br>
                <button id="saveButton" class="btn btn-primary" type="button">Safe</button>
                <button id="backButton" class="btn btn-secondary" type="button" onclick="closeForm">Back</button>
            </form>
        `);
        $(".modal-footer").addClass('d-none');
    });

     // Делегирование события клика для кнопки "Сохранить"
    $(document).on('click', '#saveButton', function(e) {
        e.preventDefault();
        var deviceId = $('#scheduleModal').data('device-id'); // Получаем сохраненный device ID
        var formData = $('#addForm').find("input"); // Сериализация данных формы
        $.ajax({
            url: '/add-schedule',
            type: 'POST',
            data: {time_start: formData[0].value, 
                time_end: formData[1].value, 
                device_id: deviceId},
            success: function(response) {
                if (!response.success) {
                    alert('Error.');
                }
                closeForm(deviceId);
            }
        });
    });

    $(document).on('click', '#saveEditButton', function(e) {
        var selectedId = $('#scheduleModal').data('selected-id');
        e.preventDefault();
        var deviceId = $('#scheduleModal').data('device-id'); // Получаем сохраненный device ID
        var formData = $('#addForm').find("input"); // Сериализация данных формы
        $.ajax({
            url: '/edit-schedule',
            type: 'POST',
            data: {time_start: formData[0].value, 
                time_end: formData[1].value, 
                schedule_id: selectedId},
            success: function(response) {
                closeForm(deviceId);
            }
        });
    });

    // Делегирование события клика для кнопки "Назад"
    $(document).on('click', '#backButton', function(e) {
        e.preventDefault();
        var deviceId = $('#scheduleModal').data('device-id'); // Получаем сохраненный device ID
        closeForm(deviceId); // Вызов функции закрытия формы
    });

    $('#editButton').click(function() {
        var selectedId = $('.list-group-item.active').data('id');
        $('#scheduleModal').data('selected-id', selectedId); 
        $.ajax({
            url: '/get-schedule-time',
            type: 'POST',
            data: {schedule_id: selectedId},
            success: function(response) {
                if (response.length) {
                    time_on = response[0].time_on
                    time_off = response[0].time_off
                    $('.modal-body').html(`
                        <form id="addForm">
                            Time start: <input type="time" value=${time_on} name="time_start"/><br/>
                            Time end: <input type="time" value=${time_off} name="time_end"/><br/>
                            <br>
                            <button id="saveEditButton" class="btn btn-primary" type="button">Safe</button>
                            <button id="backButton" class="btn btn-secondary" type="button" onclick="closeForm">Back</button>
                        </form>
                    `);
                    $(".modal-footer").addClass('d-none');
                }
            }
        });
    });

    $('#deleteButton').click(function(e) {
        var selectedId = $('.list-group-item.active').data('id');
        e.preventDefault();
        var deviceId = $('#scheduleModal').data('device-id');
        $.ajax({
            url: '/delete-schedule',
            type: 'POST',
            data: {schedule_id: selectedId},
            success: function(response) {
                if (response.success) {
                    $('.list-group-item.active').remove();
                    $('#deleteButton').addClass('d-none');
                    alert('Delete success!');
                    closeForm(deviceId);
                }
            }
        });
    });
    function closeForm(deviceId) {
        // Здесь логика для закрытия модального окна или очистки формы
        $(".modal-footer").removeClass('d-none');
        $('#deleteButton').addClass('d-none');
        $('#editButton').addClass('d-none');
        get_schedule(deviceId);
    }
});

$(document).ready(function(){

    function requst(url, data) {
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            success: function(data) {
                if (!data.length) {
                    $('.modal-body').html('<p>Not found</p>');
                    return;
                }
                var scheduleHtml = '<ul class="list-group">';
                data.forEach(function(item) {
                    scheduleHtml += `<li class="list-group-item" data-id="${item.id}">${item.time_on} - ${item.time_off}</li>`;
                });
                scheduleHtml += '</ul>';
                $(".modal-footer").removeClass('d-none');
                $('.modal-body').html(scheduleHtml);
                $('#deleteButton').addClass('d-none');
                $('#editButton').addClass('d-none');
            }
        });
    };

   $('#scheduleModal').on('show.bs.modal', function (e) {
        var deviceId = $(e.relatedTarget).attr('value');
        $('#scheduleModal').data('device-id', deviceId); 
        data = {device_id: deviceId}
        url = "get-schedule";
        requst(url, data);
    });

    $('#linksModal').on('show.bs.modal', function (e) {
        var deviceId = $(e.relatedTarget).attr('value');
        $('#linksModal').data('device-id', deviceId); 
        data = {device_id: deviceId}
        url = "get-links";
        requst(url, data);
    });


    // Обработка выбора элемента списка
    $('.modal-body').on('click', '.list-group-item', function() {
        $('.list-group-item').removeClass('active');
        $(this).addClass('active');
        $('#deleteButton').removeClass('d-none');
        $('#editButton').removeClass('d-none');
    });


    // Удаление выбранного элемента
    $('#deleteButton').click(function() {
        var selectedId = $('.list-group-item.active').data('id');
        // Здесь код для удаления элемента из базы данных через AJAX
        console.log('Удаляем элемент с id:', selectedId);
    });
});