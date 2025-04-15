// Открытие модального окна для выбранного набора данных
function openModal(fileId) {

    // Заполняем скрытое поле file_id значением выбранного файла
    document.getElementById('file_id').value = fileId;
    // Открываем модальное окно
    const modal = document.getElementById('reportsModal');
    modal.style.display = 'flex';

    // Вставляем название файла в заголовок модального окна
    const header = document.querySelector('.modal-header h3');
    header.innerText = 'Создание отчета для набора данных: ${fileName}';

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
                        <td><button class="download-btn" onclick="downloadReport(${fileId})">Скачать</button></td>

                        alert("${fileId}");
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

// Закрытие модального окна
document.querySelector('.reports-modal').addEventListener('click', function (e) {
    if (e.target === this) {
        document.getElementById('reportsModal').style.display = 'none';
    }
});


// Функция для скачивания отчета
function downloadReport(reportId) {
    alet('god')
    // Отправляем запрос на сервер для получения отчета
    fetch(`/download_report/${reportId}`, {
        method: 'GET',
    })
    .then(response => response.blob()) // Получаем файл как Blob
    .then(blob => {
        // Создаем URL для файла
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'report_${reportId}.csv'; // Указываем имя для скачивания
        link.click(); // Инициируем скачивание
    })
    .catch(error => {
        console.error('Ошибка при скачивании отчета:', error);
    });
}
