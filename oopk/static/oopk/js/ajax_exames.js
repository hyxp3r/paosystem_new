$(document).ready(function() {


    function makeFile(file, file_name){

        var decodedData = atob(file);
        var byteNumbers = new Array(decodedData.length);
        for (var i = 0; i < decodedData.length; i++) {
            byteNumbers[i] = decodedData.charCodeAt(i);
        }
        var fileByteArray = new Uint8Array(byteNumbers);

        // Создание объекта Blob из байтовых данных
        var fileBlob = new Blob([fileByteArray], {type: 'application/CSV'});

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
            url: '/oopk/oopk/report/registration/getreg',
            type: 'POST',
            data: {
                task_id: task_id,
            },
            
            success: function(response) {
                
                if (response.status == 'SUCCESS') {
                    // Если задача выполнена успешно, отображение ссылки на скачивание отчета
                  
                     makeFile(response.file, response.file_name)
                 
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
});