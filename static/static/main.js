document.addEventListener("DOMContentLoaded", function () {
    const deadlines = document.querySelectorAll(".deadline");

    deadlines.forEach(function (item) {
        const date = new Date(item.dataset.date);
        const now = new Date();
        const diff = Math.ceil((date - now) / (1000 * 60 * 60 * 24));

        if (diff <= 2) {
            item.classList.add("urgent");
            item.innerText += " (URGENT)";
        } else {
            item.innerText += " (" + diff + " days left)";
        }
    });
});