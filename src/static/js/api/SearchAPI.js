function searchAPI(query){
    return fetch('/api/search/table', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(query),
      })
      .then(response => response.json())
      .catch((error) => {
        console.error('Error:', error);
      });
}