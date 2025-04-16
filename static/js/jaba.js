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