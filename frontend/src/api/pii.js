import axios from 'axios';

export function desensitizePII(text, entities = null) {
  return axios.post('/api/pii/desensitize/', {
    text,
    ...(entities ? { entities } : {})
  });
}

export function detectPII(data, model = 'deepseek') {
  let requestData;
  if (data instanceof FormData) {
    requestData = data;
    requestData.append('model', model);
    return axios.post('/api/pii/detect/', requestData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  } else {
    requestData = {
      text: data,
      model: model
    };
    return axios.post('/api/pii/detect/', requestData);
  }
}
