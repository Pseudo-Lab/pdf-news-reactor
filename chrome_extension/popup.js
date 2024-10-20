document.addEventListener('DOMContentLoaded', function () {
    const journalistStats = {
      'useful': 9,
      'touched': 87,
      'recommend': 14,
      'analytical': 1,
      'wow': 6
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
        "wow": "흥미진진"
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

    chrome.storage.local.get('journalist', function(result) {
      if (result.journalist) {
        document.getElementById('stats').innerHTML += `
          <p>Journalist: ${result.journalist}</p>
        `;
    }
    }
  );

    document.getElementById('stats').innerHTML += `
      <p>Useful: ${journalistStats.useful}</p>
      <p>Touched: ${journalistStats.touched}</p>
      <p>Recommend: ${journalistStats.recommend}</p>
      <p>Analytical: ${journalistStats.analytical}</p>
      <p>Wow: ${journalistStats.wow}</p>
    `;
  });
  
