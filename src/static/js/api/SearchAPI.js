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

function saveSearchAPI(data){
  return fetch('/api/search/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function getAllSearchAPI(data){
  return fetch('/api/search/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then(response => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

function deleteSearchAPI(searchID){
  return fetch('/api/search/'+searchID, {
      method: 'DELETE'
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}