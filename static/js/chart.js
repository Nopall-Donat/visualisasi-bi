let lineChart;

function updateSummary(year) {
    fetch(`/summary-data?year=${year}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('highest-region').textContent = data.highest.region;
            document.getElementById('highest-value').textContent = `${data.highest.value}%`;
            document.getElementById('lowest-region').textContent = data.lowest.region;
            document.getElementById('lowest-value').textContent = `${data.lowest.value}%`;
            document.getElementById('selected-year').textContent = year;
        });
}

function updateLineChart(year) {
    fetch(`/linechart-data?year=${year}`)
        .then(response => response.json())
        .then(data => {
            const labels = data.map(item => item['Kabupaten/Kota']);
            let datasets = [];

            if (year === 'all') {
                const dataset2021 = data.map(item => item.Stunting_2021 || null);
                const dataset2022 = data.map(item => item.Stunting_2022 || null);
                const dataset2023 = data.map(item => item.Stunting_2023 || null);

                datasets = [
                    {
                        label: 'Stunting 2021',
                        data: dataset2021,
                        borderColor: 'blue',
                        fill: false,
                    },
                    {
                        label: 'Stunting 2022',
                        data: dataset2022,
                        borderColor: 'darkblue',
                        fill: false,
                    },
                    {
                        label: 'Stunting 2023',
                        data: dataset2023,
                        borderColor: 'red',
                        fill: false,
                    },
                ];
            } else {
                const dataset = data.map(item => item.value || null);
                datasets = [
                    {
                        label: `Stunting ${year}`,
                        data: dataset,
                        borderColor: year === '2021' ? 'blue' : year === '2022' ? 'darkblue' : 'red',
                        fill: false,
                    },
                ];
            }

            if (lineChart) {
                lineChart.destroy();
            }

            const ctx = document.getElementById('linechart').getContext('2d');
            lineChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: datasets,
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                        },
                    },
                },
            });
        });
}

// Inisialisasi dengan data 2023
updateSummary('2023');
updateLineChart('all');
