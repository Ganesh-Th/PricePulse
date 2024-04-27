document.addEventListener('DOMContentLoaded', function () {
    var priceData = JSON.parse('{{ price_data | tojson | safe }}');

    var ctx = document.getElementById('priceChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Original Price', 'Flipkart Price', 'Croma Price'],
            datasets: [{
                label: 'Prices',
                data: priceData,
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 206, 86, 0.2)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
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
});
