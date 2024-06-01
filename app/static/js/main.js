import { processDataCount, processDataLevel, processDataAll, processDataCorrelationRevenue, processDataCorrelationRatingMetaScore } from "./func_draw.js"
import { fetch_csv } from "./func_fetch.js"

$(function () {
    const divChartAll = document.getElementById("div-chart-all");
    const divChartCount = document.getElementById("div-chart-count");
    const divChartLevel = document.getElementById("div-chart-level");
    const divChartCorrelationRevenue = document.getElementById("div-chart-correlation-revenue");
    const divChartCorrelationRatingsMetascore = document.getElementById("div-chart-correlation-ratings-metascore");
    const divChartImg = document.getElementById("div-chart-img");

    var selectElementGenres = document.getElementById("choose-genres");
    var selectElementCountry = document.getElementById("choose-country");

    let chooseGenre, chooseCountry;

    function choosePredictBtn() {
        $(".body-predict").css("display", "block");
        $(".content").css("display", "none");
        $(".body-data").css("display", "none");
    }

    function chooseDataBtn() {
        $(".body-data").css("display", "block");
        $(".content").css("display", "none");
        $(".body-predict").css("display", "none");
    }

    function choosePlotBtn() {
        $(".body-data").css("display", "none");
        $(".content").css("display", "block");
        $(".body-predict").css("display", "none");
    }

    function allNone() {
        divChartAll.style.display = "none";
        divChartCount.style.display = "none";
        divChartLevel.style.display = "none";
        divChartCorrelationRevenue.style.display = "none";
        divChartCorrelationRatingsMetascore.style.display = "none";
        divChartImg.style.display = "none";
    }

    function checkChooseGenres() {
        console.log(document.getElementById("radio1").checked);
        if (document.getElementById("radio1").checked)
            return true;
        else return false;
    }

    function getRandomColor() {
        const colors = [
            "#FF5733", // Đỏ cam
            "#33FF57", // Xanh lá nhạt
            "#3357FF", // Xanh dương nhạt
            "#FF33A8", // Hồng nhạt
            "#A833FF", // Tím nhạt
            "#33FFF3", // Xanh ngọc nhạt
            "#FF8C33", // Cam nhạt
            "#33FF8C", // Xanh lá cây nhạt
            "#FF33D4", // Hồng đậm
            "#8C33FF"  // Tím đậm
        ];

        const randomIndex = Math.floor(Math.random() * colors.length);
        return colors[randomIndex];
    }

    function drawPlotCountYearGenres(csvData) {
        var selectedValue = selectElementGenres.value;

        if (selectedValue === "all-genres") {
            processDataCount(csvData, getRandomColor(), "genres", "", "year");
        } else {
            processDataCount(csvData, getRandomColor(), "genres", selectedValue, "year");
        }
    }

    function drawPlotCountYearCountry(csvData) {
        var selectedValue = selectElementCountry.value;

        if (selectedValue === "all-country") {
            processDataCount(csvData, getRandomColor(), "country", "", "year");
        } else {
            processDataCount(csvData, getRandomColor(), "country", selectedValue, "year");
        }
    }

    function drawPlotCountRatingsGenres(csvData) {
        var selectedValue = selectElementGenres.value;

        if (selectedValue === "all-genres") {
            processDataCount(csvData, getRandomColor(), "genres", "", "ratings");
        } else {
            processDataCount(csvData, getRandomColor(), "genres", selectedValue, "ratings");
        }
    }

    function drawPlotCountRatingsCountry(csvData) {
        var selectedValue = selectElementCountry.value;

        if (selectedValue === "all-country") {
            processDataCount(csvData, getRandomColor(), "country", "", "ratings");
        } else {
            processDataCount(csvData, getRandomColor(), "country", selectedValue, "ratings");
        }
    }

    function drawPlotLevelGenres(csvData) {
        var selectedValue = selectElementGenres.value;

        if (selectedValue === "all-genres") {
            processDataLevel(csvData, getRandomColor(), "genres", "");
        } else {
            processDataLevel(csvData, getRandomColor(), "genres", selectedValue);
        }
    }

    function drawPlotLevelCountry(csvData) {
        var selectedValue = selectElementCountry.value;

        if (selectedValue === "all-country") {
            processDataLevel(csvData, getRandomColor(), "country", "");
        } else {
            processDataLevel(csvData, getRandomColor(), "country", selectedValue);
        }
    }

    function drawPlotCorrelationRevenueGenres(csvData) {
        var selectedValue = selectElementGenres.value;

        if (selectedValue === "all-genres") {
            processDataCorrelationRevenue(csvData, getRandomColor(), "genres", "");
        } else {
            processDataCorrelationRevenue(csvData, getRandomColor(), "genres", selectedValue);
        }
    }

    function drawPlotCorrelationRevenueCountry(csvData) {
        var selectedValue = selectElementCountry.value;

        if (selectedValue === "all-country") {
            processDataCorrelationRevenue(csvData, getRandomColor(), "country", "");
        } else {
            processDataCorrelationRevenue(csvData, getRandomColor(), "country", selectedValue);
        }
    }

    function drawPlotCorrelationRatingsMetascoreGenres(csvData) {
        var selectedValue = selectElementGenres.value;

        if (selectedValue === "all-genres") {
            processDataCorrelationRatingMetaScore(csvData, getRandomColor(), "genres", "");
        } else {
            processDataCorrelationRatingMetaScore(csvData, getRandomColor(), "genres", selectedValue);
        }
    }

    function drawPlotCorrelationRatingsMetascoreCountry(csvData) {
        var selectedValue = selectElementCountry.value;

        if (selectedValue === "all-country") {
            processDataCorrelationRatingMetaScore(csvData, getRandomColor(), "country", "");
        } else {
            processDataCorrelationRatingMetaScore(csvData, getRandomColor(), "country", selectedValue);
        }
    }

    function changeGenresDraw(funName, csvData) {
        selectElementGenres.onchange = function () {
            if (funName == "plot-count-year") drawPlotCountYearGenres(csvData);
            if (funName == "plot-count-ratings") drawPlotCountRatingsGenres(csvData);
            if (funName == "plot-level") drawPlotLevelGenres(csvData);
            if (funName == "plot-correlation-revenue") drawPlotCorrelationRevenueGenres(csvData);
            if (funName == "plot-correlation-ratings-metascore") drawPlotCorrelationRatingsMetascoreGenres(csvData);
        };
    }

    function changeCountryDraw(funName, csvData) {
        selectElementCountry.onchange = function () {
            if (funName == "plot-count-year") drawPlotCountYearCountry(csvData);
            if (funName == "plot-count-ratings") drawPlotCountRatingsCountry(csvData);
            if (funName == "plot-level") drawPlotLevelCountry(csvData);
            if (funName == "plot-correlation-revenue") drawPlotCorrelationRevenueCountry(csvData);
            if (funName == "plot-correlation-ratings-metascore") drawPlotCorrelationRatingsMetascoreCountry(csvData);
        };
    }

    function restartSelectAndRadio() {
        document.getElementById("radio1").checked = true;
        document.getElementById("radio2").checked = false;
        selectElementGenres.value = "all-genres";
        selectElementCountry.value = "all-country";
    }

    function noneTableContent() {
        document.getElementById("table-content").style.display = "none";
    }

    function showTableContent() {
        document.getElementById("table-content").style.display = "block";
    }

    (async () => {
        try {
            const csvData = await fetch_csv();

            $("#plot-count-year").on("click", () => {
                choosePlotBtn();
                allNone();
                restartSelectAndRadio();
                showTableContent();
                divChartCount.style.display = "block";
                processDataCount(csvData, getRandomColor(), "genres", "", "year");
                changeGenresDraw("plot-count-year", csvData);

                $("#radio1").change(function () {
                    drawPlotCountYearGenres(csvData);
                    changeGenresDraw("plot-count-year", csvData);
                });

                $("#radio2").change(function () {
                    drawPlotCountYearCountry(csvData);
                    changeCountryDraw("plot-count-year", csvData);
                });
            });



            $("#plot-count-ratings").on("click", () => {
                choosePlotBtn();
                allNone();
                restartSelectAndRadio();
                showTableContent();
                divChartCount.style.display = "block";
                processDataCount(csvData, getRandomColor(), "genres", "", "ratings");
                changeGenresDraw("plot-count-ratings", csvData);

                $("#radio1").change(function () {
                    drawPlotCountRatingsGenres(csvData);
                    changeGenresDraw("plot-count-ratings", csvData);
                });

                $("#radio2").change(function () {
                    drawPlotCountRatingsCountry(csvData);
                    changeCountryDraw("plot-count-ratings", csvData);
                });
            });

            $("#plot-level").on("click", () => {
                choosePlotBtn();
                allNone();
                restartSelectAndRadio();
                showTableContent();
                divChartLevel.style.display = "block";
                processDataLevel(csvData, getRandomColor(), "genres", "");
                changeGenresDraw("plot-level", csvData);

                $("#radio1").change(function () {
                    drawPlotLevelGenres(csvData);
                    changeGenresDraw("plot-level", csvData);
                });

                $("#radio2").change(function () {
                    drawPlotLevelCountry(csvData);
                    changeCountryDraw("plot-level", csvData);
                });
            });

            $("#plot-correlation-revenue").on("click", () => {
                choosePlotBtn();
                allNone();
                restartSelectAndRadio();
                showTableContent();
                divChartCorrelationRevenue.style.display = "block";
                processDataCorrelationRevenue(csvData, getRandomColor(), "genres", "");
                changeGenresDraw("plot-correlation-revenue", csvData);

                $("#radio1").change(function () {
                    drawPlotCorrelationRevenueGenres(csvData);
                    changeGenresDraw("plot-correlation-revenue", csvData);
                });

                $("#radio2").change(function () {
                    drawPlotCorrelationRevenueCountry(csvData);
                    changeCountryDraw("plot-correlation-revenue", csvData);
                });
            });

            $("#plot-correlation-ratings-metascore").on("click", () => {
                choosePlotBtn();
                allNone();
                restartSelectAndRadio();
                showTableContent();
                divChartCorrelationRatingsMetascore.style.display = "block";
                processDataCorrelationRatingMetaScore(csvData, getRandomColor(), "genres", "");
                changeGenresDraw("plot-correlation-ratings-metascore", csvData);

                $("#radio1").change(function () {
                    drawPlotCorrelationRatingsMetascoreGenres(csvData);
                    changeGenresDraw("plot-correlation-ratings-metascore", csvData);
                });

                $("#radio2").change(function () {
                    drawPlotCorrelationRatingsMetascoreCountry(csvData);
                    changeCountryDraw("plot-correlation-ratings-metascore", csvData);
                });
            });

            $("#plot-all").on("click", () => {
                choosePlotBtn();
                allNone();
                restartSelectAndRadio();
                noneTableContent();
                divChartAll.style.display = "block";
                processDataAll(csvData, getRandomColor(), getRandomColor());
            });



            $("#plot-img").on("click", () => {
                choosePlotBtn();
                allNone();
                restartSelectAndRadio();
                noneTableContent();
                divChartImg.style.display = "block";
            });

            $("#dataId").on("click", () => {
                chooseDataBtn();
                allNone();
                $(".body-data").css("display", "block");
                $(".content").css("display", "none");
                const tableElement = $("#table-data");

                const thead = document.createElement('thead');
                const tbody = document.createElement('tbody');

                // movie_name,mpaa,budget,runtime,screens,opening_week,domestic_box_office,ratings,user_vote,country,genres,critic_vote,meta_score,sequel,month,year

                const thMovieName = document.createElement('th');
                thMovieName.textContent = "movie_name";
                const thMpaa = document.createElement('th');
                thMpaa.textContent = "mpaa";
                const thBudget = document.createElement('th');
                thBudget.textContent = "budget";
                const thRuntime = document.createElement('th');
                thRuntime.textContent = "runtime";
                const thScreens = document.createElement('th');
                thScreens.textContent = "screens";
                const thOpeningWeek = document.createElement('th');
                thOpeningWeek.textContent = "opening_week";
                const thDomesticBoxOffice = document.createElement('th');
                thDomesticBoxOffice.textContent = "domestic_box_office";
                const thRatings = document.createElement('th');
                thRatings.textContent = "ratings";
                const thUserVote = document.createElement('th');
                thUserVote.textContent = "user_vote";
                const thCountry = document.createElement('th');
                thCountry.textContent = "country";
                const thGenres = document.createElement('th');
                thGenres.textContent = "genres";
                const thCriticVote = document.createElement('th');
                thCriticVote.textContent = "critic_vote";
                const thMetaScore = document.createElement('th');
                thMetaScore.textContent = "meta_score";
                const thSequel = document.createElement('th');
                thSequel.textContent = "sequel";
                const thMonth = document.createElement('th');
                thMonth.textContent = "month";
                const thYear = document.createElement('th');
                thYear.textContent = "year";

                thead.appendChild(thMovieName);
                thead.appendChild(thMonth);
                thead.appendChild(thYear);
                thead.appendChild(thGenres);
                thead.appendChild(thCountry);
                thead.appendChild(thMpaa);
                thead.appendChild(thBudget);
                thead.appendChild(thRuntime);
                thead.appendChild(thScreens);
                thead.appendChild(thCriticVote);
                thead.appendChild(thMetaScore);
                thead.appendChild(thUserVote);
                thead.appendChild(thRatings);
                thead.appendChild(thSequel);
                thead.appendChild(thOpeningWeek);
                thead.appendChild(thDomesticBoxOffice);

                Papa.parse(csvData, {
                    header: true,
                    dynamicTyping: true,
                    complete: function (results) {
                        const data = results.data;

                        data.sort((a, b) => {
                            if (a.year !== b.year) {
                                return b.year - a.year;
                            } else {
                                return b.month - a.month;
                            }

                        });

                        data.forEach(movie => {
                            if (movie.budget) {
                                movie.budget = movie.budget.toLocaleString('en-US');
                                movie.screens = movie.screens.toLocaleString('en-US');
                                movie.critic_vote = movie.critic_vote.toLocaleString('en-US');
                                movie.user_vote = movie.user_vote.toLocaleString('en-US');
                                movie.opening_week = movie.opening_week.toLocaleString('en-US');
                                movie.domestic_box_office = movie.domestic_box_office.toLocaleString('en-US');
                            }
                        });

                        data.forEach(row => {
                            if (row["movie_name"]) {
                                const tr = document.createElement('tr');

                                const tdMovieName = document.createElement('td');
                                tdMovieName.textContent = row["movie_name"];
                                const tdMpaa = document.createElement('td');
                                tdMpaa.textContent = row["mpaa"];
                                const tdBudget = document.createElement('td');
                                tdBudget.textContent = row["budget"];
                                const tdRuntime = document.createElement('td');
                                tdRuntime.textContent = row["runtime"];
                                const tdScreens = document.createElement('td');
                                tdScreens.textContent = row["screens"];
                                const tdOpeningWeek = document.createElement('td');
                                tdOpeningWeek.textContent = row["opening_week"];
                                const tdDomesticBoxOffice = document.createElement('td');
                                tdDomesticBoxOffice.textContent = row["domestic_box_office"];
                                const tdRatings = document.createElement('td');
                                tdRatings.textContent = row["ratings"];
                                const tdUserVote = document.createElement('td');
                                tdUserVote.textContent = row["user_vote"];
                                const tdCountry = document.createElement('td');
                                tdCountry.textContent = row["country"];
                                const tdGenres = document.createElement('td');
                                tdGenres.textContent = row["genres"];
                                const tdCriticVote = document.createElement('td');
                                tdCriticVote.textContent = row["critic_vote"];
                                const tdMetaScore = document.createElement('td');
                                tdMetaScore.textContent = row["meta_score"];
                                const tdSequel = document.createElement('td');
                                tdSequel.textContent = row["sequel"];
                                const tdMonth = document.createElement('td');
                                tdMonth.textContent = row["month"];
                                const tdYear = document.createElement('td');
                                tdYear.textContent = row["year"];

                                tr.appendChild(tdMovieName);
                                tr.appendChild(tdMonth);
                                tr.appendChild(tdYear);
                                tr.appendChild(tdGenres);
                                tr.appendChild(tdCountry);
                                tr.appendChild(tdMpaa);
                                tr.appendChild(tdBudget);
                                tr.appendChild(tdRuntime);
                                tr.appendChild(tdScreens);
                                tr.appendChild(tdCriticVote);
                                tr.appendChild(tdMetaScore);
                                tr.appendChild(tdUserVote);
                                tr.appendChild(tdRatings);
                                tr.appendChild(tdSequel);
                                tr.appendChild(tdOpeningWeek);
                                tr.appendChild(tdDomesticBoxOffice);


                                tbody.appendChild(tr);
                            }
                        });
                    }
                });

                tableElement.append(thead);
                tableElement.append(tbody);

            });

            $("#predictId").on("click", () => {
                choosePredictBtn();
            });


        } catch (error) {
            console.error('Error:', error);
        }
    })();
})