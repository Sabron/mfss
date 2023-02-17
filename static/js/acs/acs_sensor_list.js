const ctx = document.getElementById('lineChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [
        ],
        datasets: [{
            label: 'Показания датчика',
            fill: false,
            data: [
            ],
          borderColor: 'rgb(54, 162, 235, 1)',
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

function intime(d) {
    var day = d.getDate();
    var hrs = d.getHours();
    var min = d.getMinutes();
    var sec = d.getSeconds();

    var mnt = new Array("января", "февраля", "марта", "апреля", "мая",
        "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря");

    if (day <= 9) day = "0" + day;
    if (hrs <= 9) hrs = "0" + hrs;
    if (min <= 9) min = "0" + min;
    if (sec <= 9) sec = "0" + sec;

    return "Дата последнего показания : " + hrs + ":" + min + ":" + sec + "&nbsp;&nbsp;&nbsp;" +
        day + " " + mnt[d.getMonth()] + " " + d.getFullYear() + " г."
}



function setparametrs(p) {
    document.getElementById('sensor_type').setAttribute('value', p);
    myChart.data.labels = []
    myChart.data.datasets[0].data = []
    myChart.update();
}

$(function () {

    /*
        * Flot Interactive Chart
        * -----------------------
        */
    // We use an inline data source in the example, usually data would
    // be fetched from a server
    var data = [],
        totalPoints = 100

    function getRandomData() {

        if (data.length > 0) {
            data = data.slice(1)
        }

        // Do a random walk
        while (data.length < totalPoints) {

            var prev = data.length > 0 ? data[data.length - 1] : 50,
                y = prev + Math.random() * 10 - 5

            if (y < 0) {
                y = 0
            } else if (y > 100) {
                y = 100
            }

            data.push(y)
        }

        // Zip the generated y values with the x values
        var res = []
        for (var i = 0; i < data.length; ++i) {
            
            res.push([new Date().getTime() - (i*100), data[i]])
        }
        console.log(res)
        return res
    }

    var interactive_plot = $.plot('#interactive', [
        {
            data: getRandomData(),
            //data: [[new Date().getTime(), 0.01], [new Date().getTime(), 0.3]]
        }
    ],
        {
            grid: {
                borderColor: '#f3f3f3',
                borderWidth: 1,
                tickColor: '#f3f3f3'
            },
            series: {
                color: '#3c8dbc',
                lines: {
                    lineWidth: 2,
                    show: true,
                    fill: true,
                },
            },
            yaxis: {
                min: 0,
                max: 100,
                show: true
            },
            xaxis: {
                show: true,
                mode: "time",
                timeBase: "seconds",
                timeformat: "%H:%M:%S"

            }
        }
    )

    console.log([[new Date().getTime(), 0.01], [new Date().getTime(), 0.3]])
    var updateInterval = 2000 //Fetch data ever x milliseconds
    var realtime = 'on' //If == to on then fetch data every x seconds. else stop fetching

    function update() {

        interactive_plot.setData([getRandomData()])

        // Since the axes don't change, we don't need to call plot.setupGrid()
        interactive_plot.draw()
        if (realtime === 'on') {
            setTimeout(update, updateInterval)
        }
    }

    //INITIALIZE REALTIME DATA FETCHING
    if (realtime === 'on') {
        update()
    }
    //REALTIME TOGGLE
    $('#realtime .btn').click(function () {
        if ($(this).data('toggle') === 'on') {
            realtime = 'on'
        }
        else {
            realtime = 'off'
        }
        update()
    })
    /*
     * END INTERACTIVE CHART
     */
    function show() {
        cmd = 'refresh';
        id = document.getElementById('sensor_id').value
        sensor_type = document.getElementById('sensor_type').value
        $.ajax({
            type: 'POST', // метод отправки
            url: window.location.pathname + 'sensor_ajax/', // путь к обработчику
            data: {
                "cmd": cmd,
                "id": id,
                "sensor_type": sensor_type,
            },
            // dataType: 'text',
            success: function (data) {
                str_table = ''
                start = 0
                length = data.length - 1
                myChart.data.labels = []
                myChart.data.datasets[0].data = []
                var res = []
                for (index = 0; index <= length; ++index) {
                    var date = []
                    date
                    //res.push([data[index].date_time, data[index].value])
                    res.push([new Date().getTime(), data[index].value])
                    start = start + 1
                    myChart.data.labels.push(data[index].date_time);
                    myChart.data.datasets[0].data.push(data[index].value);
                    str_table = str_table + '<tr><td>' + (data.length - index) + '.</td><td>' + data[length - index].date_time + '</td><td>' + data[length - index].value + ' ({{sensor.unit}})</td></tr>'
                    $("#maxdate").html(intime(new Date(data[index].date_max)));
                    //interactive_plot.data.labels.push(data[index].date_time)
                }
                //console.log(res)
                //interactive_plot.setData(res)
                myChart.update();
                $("#table_bo").html(str_table)

            },
            error: function (dataerr) {
                console.log('Ошибка выполнение команды :' + dataerr)
            }
        });
    }
    setInterval(show, updateInterval);

})


