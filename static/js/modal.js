// Открытие модального окна для выбранного набора данных
function openModal(fileId, file_name) {
    // Заполняем скрытое поле file_id значением выбранного файла
    document.getElementById('file_id').value = fileId;
    // Открываем модальное окно
    const modal = document.getElementById('reportsModal');
    modal.style.display = 'flex';

    // Вставляем название файла в заголовок модального окна
    const header = document.querySelector('.modal-header h3');
    header.innerText = `Создание отчета для набора данных: ${file_name}`;

    // Загружаем отчеты из базы данных для этого файла
    fetchReports(fileId);
}

// Вывод отчетов в модальном окне
function fetchReports(fileId) {
    fetch(`/get_reports/${fileId}`)
        .then(response => response.json())
        .then(data => {
            const reportsList = document.getElementById('reportsList');
            reportsList.innerHTML = ''; // Очистить таблицу перед добавлением данных


            // Добавляем отчеты в таблицу
            if (data.reports.length > 0) {
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
