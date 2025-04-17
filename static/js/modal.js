// Отправка формы для генерации отчета
document.querySelector('.modal-content form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const loadingNotification = document.getElementById('loadingNotification');
    const submitButton = document.querySelector('.modal-header button');  // Кнопка отправки формы

    // Показываем уведомление, что отчет создается + отключаем кнопку
    loadingNotification.style.display = 'block';
    submitButton.disabled = true;  // Отключаем кнопку на время


    fetch('/generate_report', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            // Закрыть модальное окно после успешного создания отчета
            document.getElementById('reportsModal').style.display = 'none';
            // Перезагрузить список отчетов в модальном окне с актуальными данными
            fetchReports(formData.get('file_id')); // передаем file_id, которое было в форме
        } else {
            alert('Ошибка: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка при отправке запроса:', error);
    })
    .finally(() => {
        // Скрываем уведомление и восстанавливаем кнопку после завершения запроса
        loadingNotification.style.display = 'none';
        submitButton.disabled = false;  // Включаем кнопку снова
    });
});

// Открытие модального окна для выбранного набора данных
function openModal(fileId, file_name, session_id) {
    // Заполняем скрытое поле file_id значением выбранного файла


    document.getElementById('file_id').value = fileId;
    // Открываем модальное окно
    const modal = document.getElementById('reportsModal');
    modal.style.display = 'flex';

    // Вставляем название файла в заголовок модального окна
    const header = document.querySelector('.modal-header h3');
    header.innerText = `Создание отчета для набора данных: ${file_name}`;

    // Загружаем отчеты из базы данных для этого файла
    fetchReports(fileId, session_id);
}

// Функция для получения отчетов с сервера
function fetchReports(fileId, session_id) {
    console.log('Запрос к серверу с fileId:', fileId, 'и session_id:', session_id);


    // Запрос к серверу с правильными параметрами
    fetch(`/get_reports?file_id=${fileId}&session_id=${session_id}`)
        .then(response => response.json())
        .then(data => {
            // Обработка данных после получения
            console.log('Данные отчета:', data);

            // Пример: обновление UI с отчетами
            const reportsList = document.getElementById('reportsList');
            reportsList.innerHTML = ''; // Очищаем список перед добавлением новых данных

            if (data.reports && data.reports.length > 0) {
                data.reports.forEach(report => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${report.created_at}</td>
                        <td>${report.max_inventory}</td>
                        <td>${report.total_cost}</td>
                        <td><button class="delete-btn" onclick='deleteReport(${report.id})'>Удалить</button></td>
                        <td><button class="download-btn" onclick='downloadReport(${report.id})'>Скачать</button></td>
                    `;
                    reportsList.appendChild(row);
                });
            } else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="4">Отчеты не найдены</td>';
                reportsList.appendChild(row);
            }
        })
        .catch(error => {
            console.error('Ошибка при загрузке отчетов:', error);
        });
}

// Закрытие модального окна
document.querySelector('.reports-modal').addEventListener('click', function (e) {
    if (e.target === this) {
        document.getElementById('reportsModal').style.display = 'none';
    }
});
