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
function openModal(fileId) {
    const modal = document.getElementById('reportsModal');
    modal.style.display = 'flex';

    // Вставим данные отчетов в таблицу (пока заглушка)
    const reportsList = document.getElementById('reportsList');
    reportsList.innerHTML = `
        <tr>
            <td>15 апреля 2025, 03:31</td>
            <td>480</td>
            <td>1500.75</td>
            <td><button class="download-btn">Скачать</button></td>
        </tr>
        <tr>
            <td>16 апреля 2025, 05:12</td>
            <td>480</td>
            <td>1400.60</td>
            <td><button class="download-btn">Скачать</button></td>
        </tr>
    `;
}

// Закрытие модального окна
document.querySelector('.reports-modal').addEventListener('click', function (e) {
    if (e.target === this) {
        document.getElementById('reportsModal').style.display = 'none';
    }
});