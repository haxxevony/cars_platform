import axios from 'axios';

// Create an Axios instance with your backend base URL
const API = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
});

// Automatically attach JWT token to every request if available
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token'); // Stored after login
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Optional: handle global response errors (e.g., token expired)
API.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn('Unauthorized — token may be invalid or expired');
      // Optionally redirect to login or clear token
      localStorage.removeItem('token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export default API;
