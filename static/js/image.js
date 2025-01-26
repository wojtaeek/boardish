var fileInput = document.getElementById('file-input');
var contentInput = document.getElementById('content');

fileInput.addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function (e) {
        contentInput.value = e.target.result;
    };

    reader.readAsDataURL(file);
});

htmx.on('#form', 'htmx:xhr:progress', function (evt) {
    const progress = evt.detail.loaded / evt.detail.total * 100;
    htmx.find('#progress').setAttribute('value', progress);
    if (progress === 100) {
        htmx.ajax('GET', `/detail/{{board.id}}/`, {
            target: '#board-list',
            swap: 'innerHTML',
        });
    }
});

function scaleImage(button, type) {
    const container = button.closest('.image-container');
    const img = container.querySelector('img');

    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    if (type === 'scaled') {
        const aspectRatio = img.naturalWidth / img.naturalHeight;
        if (containerWidth / containerHeight > aspectRatio) {
            img.style.width = containerHeight * aspectRatio + 'px';
            img.style.height = containerHeight + 'px';
        } else {
            img.style.width = containerWidth + 'px';
            img.style.height = containerWidth / aspectRatio + 'px';
        }
    } else if (type === 'original') {
        img.style.width = '';
        img.style.height = '';
    }
}
