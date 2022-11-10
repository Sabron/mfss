var tags = new Map();
var tags_name = new Map();

function addTag(name) {
    // Создаем Tag
    tag = new fabric.Path(
        'm 11,-19.124715 c -8.2234742,0 -14.8981027,-6.676138 -14.8981027,-14.9016 0,-5.633585 3.35732837,-10.582599 6.3104192,-14.933175 C 4.5507896,-52.109948 9.1631953,-59.34619 11,-61.92345 c 1.733396,2.518329 6.760904,9.975806 8.874266,13.22971 3.050966,4.697513 6.023837,8.647788 6.023837,14.667425 0,8.225462 -6.674629,14.9016 -14.898103,14.9016 z m 0,-9.996913 c 2.703016,0 4.903568,-2.201022 4.903568,-4.904687 0,-2.703664 -2.200552,-4.873493 -4.903568,-4.873493 -2.7030165,0 -4.903568,2.169829 -4.903568,4.873493 0,2.703665 2.2005515,4.904687 4.903568,4.904687z',
            {
                angle: 180,
                width: 20,
                height: 40,
                scaleX: 0.4,
                scaleY: 0.4,
                left: 0,
                top: 0,
                originX: 'center',
                originY: 'center',
                fill: '#006400',
                stroke: 'black',
                text: name
        });
        textObject = new fabric.Text(name, {
            fontFamily: 'Arial',
            fontSize: 25,
            originX: 'center',
            fill: '#006400',
            originY: 'center'
        });
    
        // Обёртка вокруг текста
        background = new fabric.Rect({
            width: (name.length) * 14,
            height: 30,
            originX: 'center',
            originY: 'center',
            fill: 'white',
            stroke: 'black'
        });
        textGroup_marker = new fabric.Group([background, textObject], {
            scaleX: 0.5,
            scaleY: 0.5,
            left: tag.left + 30 * 0.5, 
            top: tag.top - 20 * 0.5 
        });

        canvas.add(tag);
        canvas.add(textGroup_marker);
  

    //canvas.add(tag);
    tags.set(name, tag);
    tags_name.set(name, textGroup_marker);
}

var canvas = new fabric.Canvas("canvas", {
    selection: false,
    scale: 1,
    moveCursor: 'default',
    hoverCursor: 'default'
});


fabric.Object.prototype.selectable = false;
const img = new Image();

img.onload = function () {
    canvas.setHeight(this.height);
    canvas.setWidth(this.width);
}

img.src = '/static/img/plan/otm_102.png';
img.crossOrigin = "Anonymous";
canvas.setBackgroundImage(img.src, canvas.renderAll.bind(canvas));

function getTag() {
    cmd = 'refresh';
    $.ajax({
        type: 'POST', // метод отправки
        url: window.location.pathname + 'gettag/', // путь к обработчику
        data: {
            "cmd": cmd
        },
        // dataType: 'text',
        success: function (data) {
            for (index = data.length - 1; index >= 0; --index) {
                left_x = data[index].x * (1014 / 42)
                top_y = (829 - data[index].y * (1014 / 42))
                addTag(data[index].name)
            }
        },
        error: function (dataerr) {
            console.log('Ошибка выполнение команды :' + dataerr)
        }
    });
}


function drawFrame() {
    $.ajax({
        type: 'POST', // метод отправки
        url: window.location.pathname + 'ajax/', // путь к обработчику
        success: function (data) {
            //console.log(data)
            $("#cont_id").html(data.length)
            for (index = data.length - 1; index >= 0; --index) {
                left_x = data[index].x
                top_y = data[index].y
                tag = tags.get(data[index].name)
                tag_name = tags_name.get(data[index].name)
                tag.set({ left: left_x, top: top_y })
                //tag_name.set({ left: left_x + 30 * 0.5, top: top_y - 20 * 0.5 })
                tag_name.set({ left: left_x - 24, top: top_y - 26 })
                canvas.renderAll();
            }
        },
        error: function (dataerr) {
            console.log('Ошибка выполнение команды :' + dataerr)
        }
    });
}


window.onload = function () {
    // Определение контекста рисования
    //canvas = document.getElementById("canvas");
    context = canvas.getContext("2d");
    getTag() 
    // Обновляем холст через 0.02 секунды
    setInterval("drawFrame()", 500);
}

//addMarker({ x: 10 * (1014 / 42), y: (829 - 20 * (1014 / 42)), name: 'ff' });