// Số lượng phim phát hành qua các năm theo từng thể loại, quốc gia
// Thống kê rating của phim

function processDataCount(csvData, backgroundColor, choose, value, x_Axis) {
    Papa.parse(csvData, {
        header: true,
        dynamicTyping: true,
        complete: function (results) {
            const data = results.data;
            const movieCountsByXAxis = {};

            data.forEach(row => {
                if (row[choose] && row[choose].includes(value)) {

                    const xAxis = row[x_Axis];

                    if (xAxis in movieCountsByXAxis) {
                        movieCountsByXAxis[xAxis]++;
                    } else {
                        movieCountsByXAxis[xAxis] = 1;
                    }
                }
            });

            const xAxiss = Object.keys(movieCountsByXAxis);
            const movieCounts = xAxiss.map(xAxis => movieCountsByXAxis[xAxis]);

            drawChartCount(xAxiss, movieCounts, backgroundColor);
        }
    });
}

function drawChartCount(xAxiss, movieCounts, backgroundColor) {
    if (currentChartCount) {
        currentChartCount.destroy();
    }

    const sortedxAxis = xAxiss.slice().sort((a, b) => a - b);

    const sortedMovieCounts = sortedxAxis.map(xAxis => {
        const index = xAxiss.indexOf(xAxis);
        return movieCounts[index];
    });

    const movieData = {
        labels: sortedxAxis,
        datasets: [{
            label: 'Number of Movies',
            backgroundColor: backgroundColor,
            data: sortedMovieCounts
        }]
    };

    const ctx = document.getElementById('bar-chart-count').getContext('2d');
    currentChartCount = new Chart(ctx, {
        type: 'line',
        data: movieData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Thống kê doanh thu theo từng thể loại, quốc gia (theo mức)
function processDataLevel(csvData, backgroundColor, choose, value) {
    Papa.parse(csvData, {
        header: true,
        dynamicTyping: true,
        complete: function (results) {
            const data = results.data;
            // domestic_box_office
            const bins = { "< 30M": 0, "30M-60M": 0, "60M-90M": 0, "90M-150M": 0, "> 150M": 0 };

            data.forEach(row => {
                if (row[choose] && row[choose].includes(value)) {
                    const domestic_box_office = row.domestic_box_office;

                    if (domestic_box_office < 30000000) {
                        bins["< 30M"]++;
                    } else if (domestic_box_office < 60000000) {
                        bins["30M-60M"]++;
                    } else if (domestic_box_office < 90000000) {
                        bins["60M-90M"]++;
                    } else if (domestic_box_office < 150000000) {
                        bins["90M-150M"]++;
                    } else {
                        bins["> 150M"]++;
                    }
                }
            });

            drawChartLevel(bins, backgroundColor);
        }
    });
}

function drawChartLevel(bins, backgroundColor) {
    if (currentChartLevel) {
        currentChartLevel.destroy();
    }

    const ctx = document.getElementById('bar-chart-level').getContext('2d');
    currentChartLevel = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(bins),
            datasets: [{
                label: 'Revenue statistics by level',
                data: Object.values(bins),
                backgroundColor: backgroundColor,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
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

}

// --------------------------------------------------------------------------------

// Số lượng phim theo từng thể loại, quốc gia (2 biểu đồ)
function processDataAll(csvData, backgroundColorGenres, backgroundColorCountry) {
    Papa.parse(csvData, {
        header: true,
        dynamicTyping: true,
        complete: function (results) {
            const data = results.data;

            const listGenres = ["Action", "Drama", "Comedy", "Documentary", "Thriller", "Romance", "Animation", "Family", "Horror", "Crime", "Adventure", "Fantasy", "Sci-Fi", "Mystery", "Biography", "History", "Sport", "Musical", "War", "Western"];
            const bins_genres = { "Action": 0, "Drama": 0, "Comedy": 0, "Documentary": 0, "Thriller": 0, "Romance": 0, "Animation": 0, "Family": 0, "Horror": 0, "Crime": 0, "Adventure": 0, "Fantasy": 0, "Sci-Fi": 0, "Mystery": 0, "Biography": 0, "History": 0, "Sport": 0, "Musical": 0, "War": 0, "Western": 0 };
            const listCountry = ['United States', 'South Africa', 'Germany', 'Spain', 'United Kingdom', 'France', 'Canada', 'China', 'India', 'Brazil', 'Bahamas', 'Netherlands', 'Australia', 'Japan', 'Malta', 'Mexico', 'Morocco', 'Ireland', 'Greece', 'Hungary', 'New Zealand', 'Romania', 'Austria', 'Italy', 'Sweden', 'Poland', 'Belgium', 'United Arab Emirates', 'Argentina', 'Denmark', 'Finland', 'Iceland', 'Norway', 'Switzerland', 'Luxembourg', 'Namibia', 'Bulgaria', 'Chile', 'Croatia', 'Paraguay', 'Uruguay', 'Turkey', 'Israel', 'Colombia', 'Thailand', 'Iran', 'Russia', 'Bosnia and Herzegovina', 'Slovakia', 'Kuwait', 'South Korea'];
            const bins_country = { "United States": 0, "South Africa": 0, "Germany": 0, "Spain": 0, "United Kingdom": 0, "France": 0, "Canada": 0, "China": 0, "India": 0, "Brazil": 0, "Bahamas": 0, "Netherlands": 0, "Australia": 0, "Japan": 0, "Malta": 0, "Mexico": 0, "Morocco": 0, "Ireland": 0, "Greece": 0, "Hungary": 0, "New Zealand": 0, "Romania": 0, "Austria": 0, "Italy": 0, "Sweden": 0, "Poland": 0, "Belgium": 0, "United Arab Emirates": 0, "Argentina": 0, "Denmark": 0, "Finland": 0, "Iceland": 0, "Norway": 0, "Switzerland": 0, "Luxembourg": 0, "Namibia": 0, "Bulgaria": 0, "Chile": 0, "Croatia": 0, "Paraguay": 0, "Uruguay": 0, "Turkey": 0, "Israel": 0, "Colombia": 0, "Thailand": 0, "Iran": 0, "Russia": 0, "Bosnia and Herzegovina": 0, "Slovakia": 0, "Kuwait": 0, "South Korea": 0 };

            data.forEach(row => {
                if (row.genres) {
                    listGenres.forEach(genre => {
                        if (row.genres.includes(genre)) {
                            bins_genres[genre]++;
                        }
                    })
                }

                if (row.country) {
                    listCountry.forEach(country => {
                        if (row.country.includes(country)) {
                            bins_country[country]++;
                        }
                    })
                }
            });

            drawChartAll(bins_genres, bins_country, backgroundColorGenres, backgroundColorCountry);
        }
    });
}

function drawChartAll(bins_genres, bins_country, backgroundColorGenres, backgroundColorCountry) {
    if (currentChartAllGenres) {
        currentChartAllGenres.destroy();
    }

    if (currentChartAllCountry) {
        currentChartAllCountry.destroy();
    }

    const ctx_genres = document.getElementById('bar-chart-all-genres').getContext('2d');
    const ctx_country = document.getElementById('bar-chart-all-country').getContext('2d');

    currentChartAllGenres = new Chart(ctx_genres, {
        type: 'bar',
        data: {
            labels: Object.keys(bins_genres),
            datasets: [{
                label: 'Number of Movies by Genre',
                data: Object.values(bins_genres),
                backgroundColor: backgroundColorGenres,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
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

    currentChartAllCountry = new Chart(ctx_country, {
        type: 'bar',
        data: {
            labels: Object.keys(bins_country),
            datasets: [{
                label: 'Number of Movies by Country',
                data: Object.values(bins_country),
                backgroundColor: backgroundColorCountry,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
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

}

// --------------------------------------------------------------------------------

// Biểu đồ tương quan giữa doanh thu và budget
function processDataCorrelationRevenue(csvData, backgroundColor, choose, value) {
    Papa.parse(csvData, {
        header: true,
        dynamicTyping: true,
        complete: function (results) {
            const data = results.data;
            let revenue = [];
            let budget = [];

            data.forEach(row => {
                if (row[choose] && row[choose].includes(value)) {
                    const bud = row.budget;
                    const rev = row.domestic_box_office;
                    
                    budget.push(bud);
                    revenue.push(rev);
                }
            });

            drawChartCorrelationRevenue(budget, revenue, backgroundColor);
        }
    });
}

function drawChartCorrelationRevenue(budgets, revenues, backgroundColor) {
    if (currentChartCorrelationRevenue) {
        currentChartCorrelationRevenue.destroy();
    }

    // Tính toán các giá trị cần thiết cho regression line
    const regressionLine = linearRegression(budgets, revenues);
    const regressionLineData = [
        { x: Math.min(...budgets), y: regressionLine.intercept + regressionLine.slope * Math.min(...budgets) },
        { x: Math.max(...budgets), y: regressionLine.intercept + regressionLine.slope * Math.max(...budgets) }
    ];

    const data = {
        datasets: [{
            label: 'Correlation chart between revenue and budget',
            data: budgets.map((budget, index) => ({ x: budget, y: revenues[index] })),
            backgroundColor: backgroundColor, // Màu nền của điểm
        }, {
            label: 'Regression Line',
            data: regressionLineData,
            borderColor: 'red', // Màu của đường thẳng
            fill: false,
            type: 'line'
        }]
    };

    const options = {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'Budget'
                }
            },
            y: {
                type: 'linear',
                position: 'left',
                title: {
                    display: true,
                    text: 'Revenue'
                }
            }
        }
    };

    const ctx = document.getElementById('correlation-chart-revenue').getContext('2d');
    currentChartCorrelationRevenue = new Chart(ctx, {
        type: 'scatter',
        data: data,
        options: options
    });
}

// Hàm tính toán regression line
function linearRegression(x, y) {
    const n = x.length;
    let sumX = 0;
    let sumY = 0;
    let sumXY = 0;
    let sumXX = 0;
    let sumYY = 0;

    for (let i = 0; i < n; i++) {
        sumX += x[i];
        sumY += y[i];
        sumXY += x[i] * y[i];
        sumXX += x[i] * x[i];
        sumYY += y[i] * y[i];
    }

    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    return { slope, intercept };
}



// Biểu đồ tương quan giữa đánh giá của người dùng và đánh giá của chuyên gia (trục ngang là rating, trục dọc là metascore) 
function processDataCorrelationRatingMetaScore(csvData, backgroundColor, choose, value) {
    Papa.parse(csvData, {
        header: true,
        dynamicTyping: true,
        complete: function (results) {
            const data = results.data;
            let metascores = [];
            let ratings = [];

            data.forEach(row => {
                if (row[choose] && row[choose].includes(value)) {
                    const rate = row.ratings;
                    const meta = row.meta_score;
                    
                    ratings.push(rate);
                    metascores.push(meta);
                }
            });

            drawChartCorrelationRatingMetaScore(ratings, metascores, backgroundColor);
        }
    });
}

function drawChartCorrelationRatingMetaScore(ratings, metascores, backgroundColor) {
    if (currentChartCorrelationRatingsMetascore) {
        currentChartCorrelationRatingsMetascore.destroy();
    }

    // Tính toán các giá trị cần thiết cho regression line
    const regressionLine = linearRegression(ratings, metascores);
    const regressionLineData = [
        { x: Math.min(...ratings), y: regressionLine.intercept + regressionLine.slope * Math.min(...ratings) },
        { x: Math.max(...ratings), y: regressionLine.intercept + regressionLine.slope * Math.max(...ratings) }
    ];

    const data = {
        datasets: [{
            label: 'Correlation chart between user vote and critic vote',
            data: ratings.map((rating, index) => ({ x: rating, y: metascores[index] })),
            backgroundColor: backgroundColor, // Màu nền của điểm
        }, {
            label: 'Regression Line',
            data: regressionLineData,
            borderColor: 'red', // Màu của đường thẳng
            fill: false,
            type: 'line'
        }]
    };

    const options = {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'Ratings'
                }
            },
            y: {
                type: 'linear',
                position: 'left',
                title: {
                    display: true,
                    text: 'MetaScore'
                }
            }
        }
    };

    const ctx = document.getElementById('correlation-chart-ratings-metascore').getContext('2d');
    currentChartCorrelationRatingsMetascore = new Chart(ctx, {
        type: 'scatter',
        data: data,
        options: options
    });
}


export { processDataCount, processDataLevel, processDataAll, processDataCorrelationRevenue, processDataCorrelationRatingMetaScore }