import axios from 'axios';

export function detectPII(text) {
  return axios.post('/api/pii/detect/', { text });
}
