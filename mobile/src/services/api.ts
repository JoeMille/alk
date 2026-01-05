import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';
import Config from 'react-native-config'; 

const API_BASE_URL = Platform.select({
  ios: Config.API_BASE_URL_IOS || 'http://localhost:8000/api',
  android: Config.API_BASE_URL_ANDROID || 'http://10.0.2.2:8000/api',
});

console.log('api base', API_BASE_URL); 

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000,
});

api.interceptors.request.use(
    async (config) => {
        try {
            const token = await AsyncStorage.getItem('access_token');

            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            } else {
                console.log('no token found');
            }
        } catch (error) {
            console.error(error);
        }

        return config;
    },
    (error: any) => {
        return Promise.reject(error);
    }
);

export const authService = {
    login: async (username: string, password: string) => {
        try {
            console.log('Attempting login for:', username);

            const response = await axios.post(`${API_BASE_URL?.replace('/api', '')}/api/auth/login/`, {
                username, 
                password,
            });

            await AsyncStorage.setItem('access_token', response.data.access);
            await AsyncStorage.setItem('refresh_token', response.data.refresh);

            return response.data;
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    },

    register: async (username: string, email: string, password: string) => {
        try {
            console.log('Attempting registration for:', username);

            const response = await axios.post(`${API_BASE_URL?.replace('/api', '')}/api/users/register/`, {
                username, 
                email, 
                password,
                password2: password,
            });

            return response.data;
        } catch (error) {
            console.error('Registration failed:', error);
            throw error;
        }
    },

    logout: async () => {
        try {
            await AsyncStorage.removeItem('access_token');
            await AsyncStorage.removeItem('refresh_token');
            console.log('Logged out');
        } catch (error) {
            console.error('Logout error:', error);
        }
    },

    isAuthenticated: async () => {
        try {
            const token = await AsyncStorage.getItem('access_token');
            return !!token;
        } catch {
            return false;
        }
    },
};

export default api;