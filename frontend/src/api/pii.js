import axios from 'axios';

export function detectPII(data, isFormData = false) {
  if (isFormData) {
    return axios.post('/api/pii/detect/', data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  } else {
    return axios.post('/api/pii/detect/', { text: data });
  }
}
