// Изменяет изображения при нажатии на них
document.addEventListener("DOMContentLoaded", () => {
    const imageToggles = [
        {
            id: "artem",
            image1: document.getElementById("artem").getAttribute("data-image-1"),
            image2: document.getElementById("artem").getAttribute("data-image-2"),
        },
        {
            id: "adelina",
            image1: document.getElementById("adelina").getAttribute("data-image-1"),
            image2: document.getElementById("adelina").getAttribute("data-image-2"),
        }
    ];

    imageToggles.forEach(({ id, image1, image2 }) => {
        const img = document.getElementById(id);
        let toggled = false;

        img.addEventListener("click", () => {
            toggled = !toggled;
            img.src = toggled ? image2 : image1;
        });
    });
});


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


// Закрытие модального окна
document.querySelector('.reports-modal').addEventListener('click', function (e) {
    if (e.target === this) {
        document.getElementById('reportsModal').style.display = 'none';
    }
});


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
            alert(`Файл ${fileName} и все связанные отчеты успешно удалены!`);
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