$(document).ready(function() {

    $('#select2Group, #select2EduLevel').on('change', function() {
        // Получение значений выбранных полей
        var group = $("#select2Group").val();
        
        var eduLevel = $("#select2EduLevel").val();
       
        

        // Отправка Ajax-запроса на сервер
        $.ajax({
            url: '/oopk/oopk/exam/write/filter',  // URL вашего представления
            type: 'get',
            data: {
                'group': group,
                'eduLevel': eduLevel,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()  // Добавление CSRF-токена для защиты от CSRF-атак
            },
            success: function(response) {
                // Обработка успешного ответа от сервера
                var filteredData = response.filtered_data;
                
                // Очистка текущих вариантов выбора во втором поле
                $('#select2Exam').empty();
                
                // Добавление отфильтрованных данных во второе поле
                for (var i = 0; i < filteredData.length; i++) {
                    var option = $('<option>').val(filteredData[i].name).text(filteredData[i].name);
                    $('#select2Exam').append(option);
                }
                $('#select2Exam').prop('disabled', false);
                $('#select2Group').prop('disabled', false);
                $('#start_date').prop('disabled', false);
                $('#end_date').prop('disabled', false);
            },
            error: function(error) {
                console.error('Ошибка при выполнении Ajax-запроса: ' + error);
            }
        });
    });

    function makeFile(file, file_name, type){

        var decodedData = atob(file);
        var byteNumbers = new Array(decodedData.length);
        for (var i = 0; i < decodedData.length; i++) {
            byteNumbers[i] = decodedData.charCodeAt(i);
        }
        var fileByteArray = new Uint8Array(byteNumbers);
        // Создание объекта Blob из байтовых данных
        if (type == "csv") {
            var fileBlob = new Blob([fileByteArray], {type: 'application/CSV'});
        }else{
            var fileBlob = new Blob([fileByteArray], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
        }
        // Создание ссылки на Blob
        var downloadLink = document.createElement('a');
        downloadLink.href = URL.createObjectURL(fileBlob);
        downloadLink.download = file_name;
         // Клик на ссылку для скачивания файла
        downloadLink.click();
         // Освобождение ресурсов Blob
        URL.revokeObjectURL(downloadLink.href);
        $('.alert-warning').hide() 
        $('.report-ready-xlsx').show() 

        
    }

    function checkTaskStatus(task_id) {

        // Отправка Ajax-запроса на Django view для получения статуса задачи
        $.ajax({
            url: '/oopk/oopk/exam/registration/getreg',
            type: 'POST',
            data: {
                task_id: task_id,
            },
            
            success: function(response) {
                
                if (response.status == 'SUCCESS') {
                    // Если задача выполнена успешно, отображение ссылки на скачивание отчета
                  
                     makeFile(response.file, response.file_name, response.type)
                 
                } else if (response.status == 'FAILURE') {
                    // Если задача завершена с ошибкой, отображение сообщения об ошибке
                    alert('Ошибка при создании отчета');
                } else {
                    // Если задача все еще выполняется, продолжаем опрашивать статус
                    setTimeout(function() {
                        checkTaskStatus(task_id);
                    }, 500);
                }
            },
            error: function(xhr, status, error) {
                // Обработка ошибки при опросе статуса задачи
                alert('Ошибка при проверке статуса задачи');
            }
        });
    }

    function checkTaskStatusWrite(task_id) {

        // Отправка Ajax-запроса на Django view для получения статуса задачи
        $.ajax({
            url: '/oopk/oopk/exam/write/getwrite',
            type: 'POST',
            data: {
                task_id: task_id,
            },
            
            success: function(response) {
                
                if (response.status == 'SUCCESS') {
                    // Если задача выполнена успешно, отображение ссылки на скачивание отчета
                  
                     makeFile(response.file, response.file_name, response.type)
                 
                } else if (response.status == 'FAILURE') {
                    // Если задача завершена с ошибкой, отображение сообщения об ошибке
                    alert('Ошибка при создании отчета');
                } else {
                    // Если задача все еще выполняется, продолжаем опрашивать статус
                    setTimeout(function() {
                        checkTaskStatus(task_id);
                    }, 500);
                }
            },
            error: function(xhr, status, error) {
                // Обработка ошибки при опросе статуса задачи
                alert('Ошибка при проверке статуса задачи');
            }
        });
    }

    function checkTaskStatusMail(task_id) {

        // Отправка Ajax-запроса на Django view для получения статуса задачи
        $.ajax({
            url: '/oopk/oopk/exam/mail/getmail',
            type: 'POST',
            data: {
                task_id: task_id,
            },
            
            success: function(response) {
                
                if (response.status == 'SUCCESS') {
                    // Если задача выполнена успешно, отображение ссылки на скачивание отчета
                  
                     makeFile(response.file, response.file_name, response.type)
                 
                } else if (response.status == 'FAILURE') {
                    // Если задача завершена с ошибкой, отображение сообщения об ошибке
                    alert('Ошибка при создании отчета');
                } else {
                    // Если задача все еще выполняется, продолжаем опрашивать статус
                    setTimeout(function() {
                        checkTaskStatus(task_id);
                    }, 500);
                }
            },
            error: function(xhr, status, error) {
                // Обработка ошибки при опросе статуса задачи
                alert('Ошибка при проверке статуса задачи');
            }
        });
    }
    
    // Обработка события отправки формы
    $('.register_exam').on('submit', function(event) {
        event.preventDefault();
        var form = $(this);
        const url = $(".register_exam").attr("data-url");

        $('.report-ready-xlsx').hide();

        $.ajax({
            type: 'post',
            data: $(this).serialize(),
            url: url,
            dataType: 'json',
            
            success: function (data){
          
                $('.report-making').show();
                checkTaskStatus(data.task_id);
            }
        }
        )

    });

    // Обработка события отправки формы
    $('.write_exam').on('submit', function(event) {
        event.preventDefault();
        var form = $(this);
        const url = $(".write_exam").attr("data-url");

        $('.report-ready-xlsx').hide();

        $.ajax({
            type: 'post',
            data: $(this).serialize(),
            url: url,
            dataType: 'json',
            
            success: function (data){
          
                $('.report-making').show();
                checkTaskStatusWrite(data.task_id);
            }
        }
        )

    });

    // Обработка события отправки формы
    $('.mail_exam').on('submit', function(event) {
        event.preventDefault();
        var form = $(this);
        const url = $(".mail_exam").attr("data-url");

        $('.report-ready-xlsx').hide();

        $.ajax({
            type: 'post',
            data: $(this).serialize(),
            url: url,
            dataType: 'json',
            
            success: function (data){
          
                $('.report-making').show();
                checkTaskStatusMail(data.task_id);
            }
        }
        )

    });
});