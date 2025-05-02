export async function operateData(url, method, data = {}, is_protected = false) {
    const response = await fetch(url, {
      method: method,
      headers: {
        "accept": "application/json",
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: JSON.stringify(data),
    });
    
    if (is_protected) {
        response.headers = getAuthHeader()
    }
    
    return response.json();  // Delete await
  }

export function getAuthHeader() {
    const token = localStorage.getItem('accessToken');
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };
}