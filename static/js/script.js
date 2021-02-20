function fetch_bitcoin() { $.getJSON('/api/bitcoin', update_bitcoin); }
function fetch_chess() { $.getJSON('/api/chess', update_chess); }
function fetch_covid() { $.getJSON('/api/covid', update_covid); }
function fetch_trivia() { $.getJSON('/api/trivia', update_trivia); }
function fetch_weather() { $.getJSON('/api/weather', update_weather); }

function update_bitcoin(bitcoin) {

    console.log(bitcoin);

    $('#bitcoin_price').text(bitcoin.price);
    $('#bitcoin_days').text(bitcoin.days);
    $('#bitcoin_growthpct').text(bitcoin.pct);
    $('#bitcoin_profit').text(bitcoin.profit);
}

function update_chess(chess) {

    console.log(chess);

    $('#chess_daily').text(chess.daily);
    $('#chess_peak').text(chess.peak);
    $('#chess_wins').text(chess.wins);
    $('#chess_losses').text(chess.losses);
    $('#chess_drawn').text(chess.drawn);
    $('#chess_activecount').text(chess.active_count);

}

function update_covid(covid) {

    console.log(covid);

    $('#covid_state').text(covid.state);
    $('#covid_deaths').text(covid.deaths);
    $('#covid_hospital').text(covid.hospitalized);
    $('#covid_icu').text(covid.icued);
}

function update_weather(weather) {

    console.log(weather);

    $('#weather_state').text(weather.state);
    $('#weather_location').text(weather.location);
    $('#weather_time').text(weather.time);
    $('#weather_sunup').text(weather.sunup);
    $('#weather_sundown').text(weather.sundown);
    $('#weather_temp').text(weather.temp);
    $('#weather_tempf').text(weather.tempf);
    $('#weather_humidity').text(weather.humidity);
    $('#weather_low').text(weather.low);
    $('#weather_lowf').text(weather.lowf);
    $('#weather_high').text(weather.high);
    $('#weather_highf').text(weather.highf);

}

function update_trivia(trivia) {

    console.log(trivia);

    $('#trivia_question').text(trivia.question);
    $('#trivia_difficulty').text(trivia.difficulty);

    var ol = $('#trivia_answers');
    ol.empty();

    trivia.answers.map( (item,i) => {

        var li = $('<li/>')
            .addClass('answer trivia_answer')
            .text(item)
            .appendTo(ol);

        if (item == trivia.correct) {
            li.attr('id', 'trivia_correct');
            }
        }
    );
}


fetch_covid();
fetch_chess();
fetch_weather();
fetch_trivia();
fetch_bitcoin();

setInterval(fetch_covid,   15 * 60 * 1000);
setInterval(fetch_chess,   15 * 60 * 1000);
setInterval(fetch_weather, 15 * 60 * 1000);
setInterval(fetch_trivia,  15 * 60 * 1000);
setInterval(fetch_bitcoin, 15 * 60 * 1000);
