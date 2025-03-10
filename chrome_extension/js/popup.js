document.addEventListener('DOMContentLoaded', function () {
    chrome.storage.local.get('journalist', function(result) {
      if (result.journalist) {
        document.getElementById('stats').innerHTML += `
          <p>Journalist: ${result.journalist}</p>
        `;
      }
    }
    );

    chrome.storage.local.get( ['useful', 'wow', 'touched', 'analytical', 'recommend','useful_avg', 'wow_avg', 'touched_avg', 'analytical_avg', 'recommend_avg'] , function(result) {
    const journalistStats = {
          'useful': result.useful,
          'touched': result.touched,
          'recommend': result.recommend,
          'analytical': result.analytical,
          'wow': result.wow
    };
    const journalistAverage = {
          'useful_avg' : result.useful_avg,
          'touched_avg' : result.touched_avg,
          'recommend_avg' : result.recommend_avg,
          'analytical_avg' : result.analytical_avg,
          'wow_avg' : result.wow_avg

    };
    const korStats = {
            "touched": "공감백배",
            "warm": "훈훈해요",
            "analytical": "분석탁월",
            "like": "좋아요",
            "sad": "슬퍼요",
            "want": "후속기사원해요",
            "recommend": "후속강추",
            "angry": "화나요",
            "useful": "쏠쏠정보",
            "wow": "흥미진진",
    }

    const ctx = document.getElementById('radarChart').getContext('2d');
    const radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: [korStats.useful , korStats.touched, korStats.recommend, korStats.analytical, korStats.wow],
            datasets: [{
                label: 'Journalist Stats',
                data: [
                    journalistStats.useful,
                    journalistStats.touched,
                    journalistStats.recommend,
                    journalistStats.analytical,
                    journalistStats.wow
                ],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgb(255, 99, 132)',
                borderWidth: 1
            },
            {
                label: 'Journalist Average',
                data: [
                    journalistAverage.useful_avg,
                    journalistAverage.touched_avg,
                    journalistAverage.recommend_avg,
                    journalistAverage.analytical_avg,
                    journalistAverage.wow_avg
                ],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                r: {
                    beginAtZero: true
                }
            }
        }
    });
    console.log(radarChart)
    document.getElementById('stats').innerHTML += `
          <p>Useful: ${journalistAverage.useful_avg}</p>
          <p>Touched: ${journalistAverage.touched_avg}</p>
          <p>Recommend: ${journalistAverage.recommend_avg}</p>
          <p>Analytical: ${journalistAverage.analytical_avg}</p>
          <p>Wow: ${journalistAverage.wow_avg}</p>
        `;
    }
    );
});
