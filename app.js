function getRecommendations() {
    var memberId = document.getElementById('memberIdInput').value;

    if (!memberId) {
        alert("Lütfen geçerli bir Member ID girin.");
        return;
    }

    callYourRecommendationAlgorithm(memberId);
}

function callYourRecommendationAlgorithm(memberId) {
    fetch(`http://localhost:5000/recommendations/${memberId}`)
        .then(response => response.json())
        .then(data => {
            showRecommendations(data.recommendations);
        })
        .catch(error => {
            console.error('API çağrısı sırasında bir hata oluştu:', error);
        });
}

function showRecommendations(recommendations) {
    var recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = '';

    if (recommendations.length > 0) {
        for (var i = 0; i < Math.min(3, recommendations.length); i++) {
            var listItem = document.createElement('li');
            listItem.textContent = "Ürün " + (i + 1) + ": " + recommendations[i];
            recommendationsList.appendChild(listItem);
        }
    } else {
        alert("Öneri bulunamadı.");
    }
}
