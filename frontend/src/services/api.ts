import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    }, 
    (error) => {
        return Promise.reject(error);
    }
);

export const authService = {
    login: async (username: string, password: string) => {
        const response = await axios.post('http://localhost:8000/api/auth/login/', {
            username,
            password,
        });

        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);

        return response.data;
    },

    register: async (username: string, email: string, password: string) => {
        return await axios.post('http://localhost:8000/api/users/register/', {
            username, 
            email,
            password,
            password2: password,
        });
    },

    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },
};

export default api;
