var ctx;
var isAllowDraw = false;
var x_c, y_c;
window.onload = () => {
    ctx = document.getElementById('cv').getContext('2d');
    ctx.fillStyle = "#FFFFFF";
    ctx.fillRect(0, 0, cv.width, cv.height);
};

function get_pencil(canvas, x, y) {
    var rect = canvas.getBoundingClientRect();
    return { x: x - rect.left * (canvas.width / rect.width), y: y - rect.top * (canvas.height / rect.height) };
}

onmousedown = function (e) {
    isAllowDraw = true;
    var { x, y } = get_pencil(cv, e.clientX, e.clientY);
    x_c = x;
    y_c = y;
    ctx.beginPath();
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.moveTo(x, y);
};

onmousemove = function (e) {
    if (isAllowDraw) {
        var { x, y } = get_pencil(cv, e.clientX, e.clientY);
        ctx.quadraticCurveTo(x_c, y_c, (x + x_c) / 2, (y + y_c) / 2);
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 15;
        ctx.stroke();
        x_c = x;
        y_c = y;
    }
};

onmouseup = function () {
    isAllowDraw = false;
};

window.addEventListener('touchstart', function (e) {
    isAllowDraw = true;
    var { x, y } = get_pencil(cv, e.touches[0].clientX, e.touches[0].clientY);
    x_c = x;
    y_c = y;
    ctx.beginPath();
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.moveTo(x, y);
});

window.addEventListener('touchmove', function (e) {
    e.preventDefault();
    if (isAllowDraw) {
        var { x, y } = get_pencil(cv, e.touches[0].clientX, e.touches[0].clientY);
        ctx.quadraticCurveTo(x_c, y_c, (x + x_c) / 2, (y + y_c) / 2);
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 15;
        ctx.stroke();
        x_c = x;
        y_c = y;
    }
}, { passive: false });

window.addEventListener('touchend', function () {
    isAllowDraw = false;
});

function clear_canvas() {
    cv.height = cv.height;
    ctx.fillStyle = "#FFFFFF";
    ctx.fillRect(0, 0, cv.width, cv.height);
    document.getElementById('output').innerText = 'Handwritten Digit Recognition';
}

function image_process() {
    var c = document.getElementById('cv');
    var c2 = document.createElement('canvas');
    var ctx2 = c2.getContext("2d");
    c2.width = c.width * 2;
    c2.height = c.height * 2;
    ctx2.fillStyle = "#FFFFFF";
    ctx2.fillRect(0, 0, c2.width, c2.height);
    ctx2.drawImage(c, parseInt(c2.width / 4), parseInt(c2.height / 4));

    var img = ctx2.getImageData(0, 0, c2.width, c2.height);
    var pixs = img.data;
    var valid_x = [], valid_y = [];
    for (var i = 0; i < pixs.length; i += 4) {
        var r = pixs[i],
            g = pixs[i + 1],
            b = pixs[i + 2],
            a = pixs[i + 3];
        if (r != 255 || g != 255 || b != 255) {
            var x = ((i / 4) % c2.width);
            var y = Math.floor((i / 4) / c2.height);
            valid_x.push(x);
            valid_y.push(y);
        }
    }
    var minX = Math.min(...valid_x),
        maxX = Math.max(...valid_x),
        valid_W = maxX - minX,
        minY = Math.min(...valid_y),
        maxY = Math.max(...valid_y),
        valid_H = maxY - minY;
    if (valid_W < valid_H) {
        minX -= parseInt((valid_H - valid_W) / 2);
        maxX += parseInt((valid_H - valid_W) / 2);
        valid_W = maxX - minX;
    } else if (valid_W > valid_H) {
        minY -= parseInt((valid_W - valid_H) / 2);
        maxY += parseInt((valid_W - valid_H) / 2);
        valid_H = maxY - minY;
    }

    var c3 = document.createElement('canvas');
    var ctx3 = c3.getContext("2d");
    c3.width = 28;
    c3.height = 28;
    ctx3.fillStyle = "#FFFFFF";
    ctx3.fillRect(0, 0, c3.width, c3.height);
    ctx3.drawImage(c2, minX, minY, valid_W, valid_H, 5, 5, 18, 18);

    let prediction = modelPredict(c3);
    document.getElementById('output').innerText = prediction;
}
