import axios from "axios";

// Create a custom axios instance pointing to your Flask backend.
const api = axios.create({
  baseURL: "http://localhost:5000", // Replace with your backend URL if needed
});

// Optionally add interceptors, headers, etc.
// api.interceptors.request.use(config => {
//   // e.g., attach token to headers
//   return config;
// });

export default api;
