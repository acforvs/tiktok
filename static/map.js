ymaps.ready(init);
var myMap;

function init () {
    myMap = new ymaps.Map("map", {
        center: [59.9499, 30.4020],
        zoom: 11
    }, {
            searchControlProvider: 'yandex#search'
        }
    );
    
    var request = new XMLHttpRequest();
    request.open('GET', 'http://127.0.0.1:8000/marks/');
    request.send();
    request.onload = function () {
        all_marks = JSON.parse(request.response);
        for (var i in all_marks) {
            if (all_marks[i].is_active == true) {
                color = "#50c878";
                bodyContent = '<p>Нажмите на кнопку, если хотите удалить точку</p>' +
                '<p> <button onclick="delete_mark(\'' + all_marks[i].mark_id + '\')">Удалить</button></p>'
            }
            else {
                color = "#ff2b2b";
                bodyContent = '<p>Нажмите на кнопку, если хотите сделать точку активной</p>' +
                '<p> <button onclick="make_mark_active(\'' + all_marks[i].mark_id + '\')">Сделать активной</button></p>'
            }

            myMap.geoObjects.add(new ymaps.Placemark([all_marks[i].latitude, all_marks[i].longitude], {
                balloonContentHeader: `${all_marks[i].content}`,
                balloonContentBody: bodyContent
            }, {
                    iconColor: color
                }
            ));
        }
    }
    
    myMap.events.add('click', function (e) {
        if (!myMap.balloon.isOpen()) {
            var coords = e.get('coords');
            myMap.balloon.open(coords, {
                contentHeader: 'Добавляем точку',
                contentBody: '<p>Добавить точку с такими вот координатами?</p>' +
                    '<p>Координаты щелчка: ' + [
                        coords[0].toPrecision(6),
                        coords[1].toPrecision(6)
                    ].join(', ') + '<button onclick="add_mark(\'' + coords[0].toPrecision(6) + '\', \'' + coords[1].toPrecision(6) + '\')">Добавить</button></p>',
                contentFooter: '<sup>Нажмите на кнопку, чтобы внести точку в базу</sup>'
            });
        }
        else {
            myMap.balloon.close();
        }
    });
}

function add_mark(latitude, longitude) {
    function choose(choices) {
        var index = Math.floor(Math.random() * choices.length);
        return choices[index];
    };
    text_choices = ["blabla", "tiktok is the best", "TipTop"]
    
    latitude = parseFloat(latitude);
    longitude = parseFloat(longitude);

    var request = new XMLHttpRequest();
    var params = {"latitude": latitude, "longitude": longitude, "content": choose(text_choices)};
    var paramsJSON = JSON.stringify(params);

    request.open('POST', 'http://127.0.0.1:8000/create_mark/');
    request.setRequestHeader('Content-Type', 'application/json')
    request.send(paramsJSON);

    window.location.reload(true);
}

function delete_mark(mark_id) {
    var request = new XMLHttpRequest();
    request.open('POST', `http://127.0.0.1:8000/make_mark_inactive/?mark_id=${mark_id}`);
    request.send();

    window.location.reload(true);
}

function make_mark_active(mark_id) {
    var request = new XMLHttpRequest();
    request.open('POST', `http://127.0.0.1:8000/make_mark_active/?mark_id=${mark_id}`);
    request.send();

    window.location.reload(true);
}
