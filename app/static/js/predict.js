// Genres
document.getElementById('input-genres').addEventListener('input', function () {
  const input = this.value.trim().toLowerCase();
  const suggestions = document.getElementById('genre-suggestions');

  const validGenres = `Short Drama Comedy Cocumentary Adult Action Thriller Romance Animation Family Horror Crime Adventure Fantasy Sci_Fi Mystery Biography History Sport Musical War Western Film_noir`.split(' ');

  suggestions.innerHTML = '';

  const matchedGenres = validGenres.filter(genre => genre.toLowerCase().includes(input));

  matchedGenres.forEach(genre => {
    const suggestionItem = document.createElement('div');
    suggestionItem.textContent = genre;
    suggestionItem.classList.add('genre-suggestion');
    suggestionItem.addEventListener('click', function () {
      document.getElementById('input-genres').value = this.textContent;
      suggestions.innerHTML = '';
    });
    suggestions.appendChild(suggestionItem);
    suggestions.style.display = 'block';
  });
});

document.addEventListener('click', function (event) {
  const genresSuggestions = document.getElementById('genre-suggestions');
  const clickedElement = event.target;

  if (!genresSuggestions.contains(clickedElement)) {
    genresSuggestions.style.display = 'none';
  }
});

document.getElementById('add-genre-btn').addEventListener('click', function () {
  const genresInput = document.getElementById('input-genres');
  const genresList = document.getElementById('genres-list');
  const genreValue = genresInput.value.trim();

  const validGenres = `short drama comedy documentary adult action thriller romance animation family horror crime adventure fantasy sci_Fi mystery biography history sport musical war western film_noir`.split(' ');

  if (validGenres.includes(genreValue.toLowerCase())) {
    const genreItem = document.createElement('div');
    genreItem.classList.add('genre-item');
    genreItem.textContent = genreValue;

    const removeButton = document.createElement('button');
    removeButton.textContent = 'X';
    removeButton.classList.add('remove-btn');
    removeButton.addEventListener('click', function () {
      genresList.removeChild(genreItem);
    });

    genreItem.appendChild(removeButton);
    genresList.appendChild(genreItem);

    genresInput.value = '';
  } else {
    alert('Invalid genre!');
  }
});

const validCountry = ['United States', 'South Africa', 'Germany', 'Spain', 'United Kingdom', 'France', 'Canada', 'China', 'India', 'Brazil', 'Bahamas', 'Netherlands', 'Australia', 'Japan', 'Malta', 'Mexico', 'Morocco', 'Ireland', 'Greece', 'Hungary', 'New Zealand', 'Romania', 'Austria', 'Italy', 'Sweden', 'Poland', 'Belgium', 'United Arab Emirates', 'Argentina', 'Denmark', 'Finland', 'Iceland', 'Norway', 'Switzerland', 'Luxembourg', 'Namibia', 'Bulgaria', 'Chile', 'Croatia', 'Paraguay', 'Uruguay', 'Turkey', 'Israel', 'Colombia', 'Thailand', 'Iran', 'Russia', 'Bosnia and Herzegovina', 'Slovakia', 'Kuwait', 'South Korea'];

// Country
document.getElementById('input-country').addEventListener('input', function () {
  const input = this.value.trim().toLowerCase();
  const suggestions = document.getElementById('country-suggestions');

  suggestions.innerHTML = '';

  const matchedCountries = validCountry.filter(country => country.toLowerCase().includes(input));

  matchedCountries.forEach(country => {
    const suggestionItem = document.createElement('div');
    suggestionItem.textContent = country;
    suggestionItem.classList.add('country-suggestion');
    suggestionItem.addEventListener('click', function () {
      document.getElementById('input-country').value = this.textContent;
      suggestions.innerHTML = '';
    });
    suggestions.appendChild(suggestionItem);
    suggestions.style.display = 'block';
  });
});

document.addEventListener('click', function (event) {
  const genresSuggestions = document.getElementById('country-suggestions');
  const clickedElement = event.target;

  if (!genresSuggestions.contains(clickedElement)) {
    genresSuggestions.style.display = 'none';
  }
});

document.getElementById('add-country-btn').addEventListener('click', function () {
  const countryInput = document.getElementById('input-country');
  const countryList = document.getElementById('country-list');
  const countryValue = countryInput.value.trim();

  if (validCountry.includes(countryValue)) {
    const countryItem = document.createElement('div');
    countryItem.classList.add('country-item');
    countryItem.textContent = countryValue;

    const removeButton = document.createElement('button');
    removeButton.textContent = 'X';
    removeButton.classList.add('remove-btn');
    removeButton.addEventListener('click', function () {
      countryList.removeChild(countryItem);
    });

    countryItem.appendChild(removeButton);
    countryList.appendChild(countryItem);

    countryInput.value = '';
  } else {
    alert('Invalid country!');
  }
});

// Submit
let currentChart4;
function saveFormData() {
  // Lấy giá trị từ các trường input
  const movieName = document.getElementById('input-movie_name').value.trim();
  const month = document.getElementById('input-month').value;
  const year = document.getElementById('input-year').value;
  const mpaa = document.getElementById('input-mpaa').value;
  const runtime = document.getElementById('input-runtime').value.trim();
  const genresList = document.getElementById('genres-list');
  const countryList = document.getElementById('country-list');
  const genres = Array.from(genresList.children).map(genreItem => genreItem.textContent.trim().slice(0, -1)).join(', ');
  const country = Array.from(countryList.children).map(countryItem => countryItem.textContent.trim().slice(0, -1)).join(', ');
  const budget = document.getElementById('input-budget').value.trim();
  const screens = document.getElementById('input-screens').value.trim();
  const criticVote = document.getElementById('input-critic-vote').value.trim();
  const metaScore = document.getElementById('input-meta_score').value.trim();
  const sequel = document.querySelector('input[name="input-sequel"]:checked').value;

  let data = {
    movieName: movieName,
    month: month,
    year: year,
    mpaa: mpaa,
    runtime: runtime,
    genres: genres,
    country: country,
    budget: budget,
    screens: screens,
    criticVote: criticVote,
    metaScore: metaScore,
    sequel: sequel
  };

  if (openingWeekDiv.style.display == "block") {
    const userVote = document.getElementById('input-user-vote').value.trim();
    const ratings = document.getElementById('input-ratings').value.trim();
    const openingWeek = document.getElementById('input-opening_week').value.trim();
    data.userVote = userVote;
    data.ratings = ratings;
    data.openingWeek = openingWeek;
  }

  fetch('/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(predict => {
      console.log(predict);
      document.getElementById('movie_name_h2').innerHTML = data.movieName;
      document.getElementById('result_rf').innerHTML = parseInt(predict['prediction_rf']) + "$";
      document.getElementById('loinhuan_rf').innerHTML = parseFloat(((parseInt(predict['prediction_rf']) - parseInt(data.budget))/parseInt(data.budget)) * 100).toFixed(2) + "%";
      
      document.getElementById('result_gb').innerHTML = parseInt(predict['prediction_gb']) + "$";
      document.getElementById('loinhuan_gb').innerHTML = parseFloat(((parseInt(predict['prediction_gb']) - parseInt(data.budget))/parseInt(data.budget)) * 100).toFixed(2) + "%";

      document.getElementById('result_xgb').innerHTML = parseInt(predict['prediction_xgb']) + "$";
      document.getElementById('loinhuan_xgb').innerHTML = parseFloat(((parseInt(predict['prediction_xgb']) - parseInt(data.budget))/parseInt(data.budget)) * 100).toFixed(2) + "%";

      document.getElementById('result_lgbm').innerHTML = parseInt(predict['prediction_lgbm']) + "$";
      document.getElementById('loinhuan_lgbm').innerHTML = parseFloat(((parseInt(predict['prediction_lgbm']) - parseInt(data.budget))/parseInt(data.budget)) * 100).toFixed(2) + "%";

      document.getElementById('result_cb').innerHTML = parseInt(predict['prediction_cb']) + "$";
      document.getElementById('loinhuan_cb').innerHTML = parseFloat(((parseInt(predict['prediction_cb']) - parseInt(data.budget))/parseInt(data.budget)) * 100).toFixed(2) + "%";
      
      document.getElementById('popup-overlay').style.display = 'flex';
      // fetch('../static/final_merged.csv')
      //   .then(response => response.text())
      //   .then(csvData => {
      //     processData4(csvData, "blue", data, predict['prediction_rf'])
      //   })
      //   .catch(error => console.error('Failed to load data.csv', error));
    })
    .catch(error => {
      console.error('Error:', error);
    });


}

// mpaa,budget,runtime,screens,opening_week,ratings,user_vote,country,genres,critic_vote,meta_score,sequel,month,year
function processData4(csvData, backgroundColor, data_inp, predict) {
  Papa.parse(csvData, {
    header: true,
    dynamicTyping: true,
    complete: function (results) {
      const data = results.data;

      console.log("Data: " + data_inp['mpaa']);
      console.log("Data Country: " + data_inp['country']);

      let list_country = data_inp['country'].split(', ');

      let revenue_mpaa = 0;
      let revenue_month = 0;
      let revenue_year = 0;
      let revenue_country = 0;
      let revenue_genres = 0;

      let index_mpaa = 0;
      let index_month = 0;
      let index_year = 0;
      let index_country = 0;
      let index_genres = 0;

      data.forEach(row => {
        if (row.mpaa == data_inp['mpaa']) {
          revenue_mpaa = revenue_mpaa + row.domestic_box_office;
          index_mpaa += 1;
        }
        if (parseInt(row.month) == parseInt(data_inp['month'])) {
          revenue_month = revenue_month + row.domestic_box_office;
          index_month += 1;
        }
        if (parseInt(row.year) == parseInt(data_inp['year'])) {
          revenue_year = revenue_year + row.domestic_box_office;
          index_year += 1;
        }
        if (row.country && checkAllWords(row.country, data_inp['country'])) {
          revenue_country = revenue_country + row.domestic_box_office;
          index_country += 1;
        }
        if (row.genres && checkAllWords(row.genres, data_inp['genres'])) {
          revenue_genres = revenue_genres + row.domestic_box_office;
          index_genres += 1;
        }
      });

      revenue_mpaa = revenue_mpaa / index_mpaa;
      revenue_month = revenue_month / index_month;
      revenue_year = revenue_year / index_year;
      revenue_country = revenue_country / index_country;
      revenue_genres = revenue_genres / index_genres;

      const currentMovie = {
        mpaa: predict,
        month: predict,
        year: predict,
        country: predict,
        genres: predict
      };

      console.log("Current Movie: " + currentMovie);

      const averageData = {
        mpaa: revenue_mpaa,
        month: revenue_month,
        year: revenue_year,
        country: revenue_country,
        genres: revenue_genres
      };

      const labels = ['mpaa', 'month', 'year', 'country', 'genres'];

      const currentMovieData = Object.values(currentMovie);
      const averageDataValues = Object.values(averageData);

      drawChart4(currentMovieData, labels, averageDataValues, backgroundColor);

    }
  });
}

function drawChart4(currentMovieData, labels, averageDataValues, backgroundColor) {
  if (currentChart4) {
    currentChart4.destroy();
  }
  const data = {
    labels: labels,
    datasets: [
      {
        label: 'Current Movie',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
        data: currentMovieData
      },
      {
        label: 'Average Data',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
        data: averageDataValues
      }
    ]
  };

  const config = {
    type: 'bar',
    data: data,
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Comparison of Movie Attributes with Averages'
        }
      }
    },
  };
  const ctx = document.getElementById('bar4-chart').getContext('2d');
  currentChart4 = new Chart(ctx, config);
  
}

function checkAllWords(str1, str2) {
  // Tách các từ trong str2 thành một danh sách
  const words = str2.split(", ");

  for (const word of words) {
    if (!str1.includes(word)) {
      return false;
    }
  }

  return true;
}

document.addEventListener('DOMContentLoaded', function () {
  // Bắt sự kiện khi nhấn nút "Submit"
  document.querySelector('.submit-button').addEventListener('click', function (event) {
    // Ngăn chặn hành động mặc định của nút "Submit"
    event.preventDefault();

    // Gọi hàm để lấy giá trị từ form và lưu vào các biến
    saveFormData();
  });
});

const openingWeekRadioNo = document.getElementById('opening_week_0');
const openingWeekRadioYes = document.getElementById('opening_week_1');
const openingWeekDiv = document.getElementById('div-inp-opn-week');
const divInpUserVote = document.getElementById('div-inp-user-vote');
const divInpRatings = document.getElementById('div-inp-ratings');

openingWeekRadioNo.addEventListener('click', function () {
  openingWeekDiv.style.display = 'none';
  divInpUserVote.style.display = 'none';
  divInpRatings.style.display = 'none';
});

openingWeekRadioYes.addEventListener('click', function () {
  openingWeekDiv.style.display = 'block';
  divInpUserVote.style.display = 'block';
  divInpRatings.style.display = 'block';
});

document.getElementById('cancel-popup').addEventListener('click', function () {
  document.getElementById('popup-overlay').style.display = 'none';
});