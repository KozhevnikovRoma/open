document.getElementById('fetchDataBtn').addEventListener('click', () => {
    fetch('/api/v1/user')
        .then(response => response.json())
        .then(data => {
            document.getElementById('dataOutput').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});
