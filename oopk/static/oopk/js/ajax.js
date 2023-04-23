$(document).ready(function() {
    // Обработка события изменения выбора в первом поле
    $('#select2EduLevel').on('change', function() {
        // Получение значений выбранных полей
        var filterValue1 = $(this).val();
        console.log(filterValue1)

        // Отправка Ajax-запроса на сервер
        $.ajax({
            url: 'http://127.0.0.1:8000/oopk/oopk/report/filter',  // URL вашего представления
            type: 'get',
            data: {
                'filter_field1': filterValue1,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()  // Добавление CSRF-токена для защиты от CSRF-атак
            },
            success: function(response) {
                // Обработка успешного ответа от сервера
                var filteredData = response.filtered_data;
                
                // Очистка текущих вариантов выбора во втором поле
                
                $('#select2Program').empty();
                
                // Добавление отфильтрованных данных во второе поле
                for (var i = 0; i < filteredData.length; i++) {
                    var option = $('<option>').val(filteredData[i].code + " " + filteredData[i].name).text(filteredData[i].code + " " + filteredData[i].name);
                    $('#select2Program').append(option);
                }
                $('#select2Program').prop('disabled', false);
            },
            error: function(error) {
                console.error('Ошибка при выполнении Ajax-запроса: ' + error);
            }
        });
    });


    function checkTaskStatus(task_id) {
        console.log("HI")
        // Отправка Ajax-запроса на Django view для получения статуса задачи
        $.ajax({
            url: 'http://127.0.0.1:8000/oopk/oopk/report/getreport',
            type: 'POST',
            data: {
                task_id: task_id
            },
            
            success: function(response) {
                
                if (response.status == 'SUCCESS') {
                    // Если задача выполнена успешно, отображение ссылки на скачивание отчета
                 
                    var decodedData = atob(response.file);
                    var byteNumbers = new Array(decodedData.length);
                    for (var i = 0; i < decodedData.length; i++) {
                        byteNumbers[i] = decodedData.charCodeAt(i);
                    }
                    var fileByteArray = new Uint8Array(byteNumbers);
            
                    // Создание объекта Blob из байтовых данных
                    var fileBlob = new Blob([fileByteArray], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
            
                    // Создание ссылки на Blob
                    var downloadLink = document.createElement('a');
                    downloadLink.href = URL.createObjectURL(fileBlob);
                    downloadLink.download = response.file_name;
                    $('.alert-warning').hide() 
                    $('.alert-success').show() 
                    // Клик на ссылку для скачивания файла
                    downloadLink.click();
            
                    // Освобождение ресурсов Blob
                    URL.revokeObjectURL(downloadLink.href);
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
    $('.customer_request').on('submit', function(event) {
        event.preventDefault();
        var form = $(this);
        const url = $(".customer_request").attr("data-url");
        $('.report-ready').hide();

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
});