// Функция для скачивания отчета
function downloadReport(reportId) {
    // Отправляем запрос на сервер для получения отчета
    fetch(`/download_report/${reportId}`, {
        method: 'GET',
    })
    .then(response => response.blob()) // Получаем файл как Blob
    .then(blob => {
        // Создаем URL для файла
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `report_${reportId}.csv`; // Указываем имя для скачивания
        link.click(); // Инициируем скачивание
    })
    .catch(error => {
        console.error('Ошибка при скачивании отчета:', error);
        alert('Произошла ошибка при скачивании отчета');
    });
}



// Функция для удаления отчета
function deleteReport(reportId) {
    fetch(`/delete_report/${reportId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Перезагружаем список отчетов после удаления
            fetchReports(data.file_id); // Передаем file_id, чтобы заново загрузить отчеты
            alert('Отчет успешно удален');
        } else {
            alert('Ошибка при удалении отчета');
        }
    })
    .catch(error => {
        console.error('Ошибка при удалении отчета:', error);
    });
}


// Функция для отображения окна подтверждения удаления
function confirmDelete(fileId, fileName) {
    // Создаем и отображаем диалоговое окно с подтверждением
    const confirmDialog = document.createElement('div');
    confirmDialog.classList.add('confirm-dialog');

    confirmDialog.innerHTML = `
        <div class="confirm-dialog-content">
            <p>Вы уверены? Вместе с файлом будут удалены все отчеты!</p>
            <button onclick="deleteFile(${fileId}, '${fileName}')" class="confirm-btn">Удалить</button>
            <button onclick="cancelDelete()" class="cancel-btn">Отменить</button>
        </div>
    `;
    document.body.appendChild(confirmDialog);
}


// Функция для подтверждения удаления
function deleteFile(fileId, fileName) {
    fetch(`/delete_file/${fileId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload(); // Перезагружаем страницу для обновления списка
        } else {
            alert('Ошибка при удалении файла');
        }
        document.body.removeChild(document.querySelector('.confirm-dialog')); // Убираем диалог
    })
    .catch(error => {
        console.error('Ошибка при удалении файла:', error);
        document.body.removeChild(document.querySelector('.confirm-dialog')); // Убираем диалог
    });
}


// Функция для отмены удаления
function cancelDelete() {
    document.body.removeChild(document.querySelector('.confirm-dialog')); // Убираем диалог
}


// Обработчик отправки формы для загрузки файла
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();  // Останавливаем стандартное поведение формы

    const formData = new FormData(this);
    const uploadButton = document.querySelector('button'); // Кнопка загрузки файла

    // Отключаем кнопку загрузки, чтобы предотвратить повторную отправку
    uploadButton.disabled = true;

    // Отправка данных с использованием fetch
    fetch('/upload_data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Перезагружаем страницу после того, как данные отправлены
        // Сообщения будут отрендерены с использованием Flask flash
        window.location.reload();
    })
    .catch(error => {
        console.error('Ошибка при загрузке:', error);

        // Если произошла ошибка, перезагружаем страницу, чтобы показать стандартные сообщения Flask
        window.location.reload();
    })
    .finally(() => {
        uploadButton.disabled = false;  // Включаем кнопку снова
    });
});






