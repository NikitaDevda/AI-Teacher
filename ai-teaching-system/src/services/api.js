import axios from 'axios';

// const API_BASE_URL = 'http://localhost:8000';
const API_BASE_URL = 'https://ai-teacher-q4pe.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false, 
});

// Request interceptor 
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      
      // Only redirect to login if not already on public pages
      const publicPages = ['/login', '/signup', '/'];
      const currentPath = window.location.pathname;
      
      if (!publicPages.includes(currentPath)) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const teachingAPI = {
  // Ask question (works with or without auth)
  askQuestion: async (question, sessionId = null, subject = 'general') => {
    try {
      const response = await api.post('/api/ask', {
        question,
        session_id: sessionId,
        subject,
        language: 'hi'
      });
      return response.data;
    } catch (error) {
      console.error('Ask question error:', error);
      throw error;
    }
  },

  // Interrupt with doubt
  interruptWithDoubt: async (doubt, sessionId, subject = 'general') => {
    try {
      const response = await api.post('/api/interrupt', {
        question: doubt,
        session_id: sessionId,
        subject,
        language: 'hi'
      });
      return response.data;
    } catch (error) {
      console.error('Interrupt error:', error);
      throw error;
    }
  },

  // Transcribe audio
  transcribeAudio: async (audioBlob) => {
    try {
      const formData = new FormData();
      formData.append('file', audioBlob, 'audio.webm');
      
      const response = await api.post('/api/transcribe', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Transcribe error:', error);
      throw error;
    }
  },

  // Get session history
  getSession: async (sessionId) => {
    try {
      const response = await api.get(`/api/session/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Get session error:', error);
      throw error;
    }
  },
};



export const authAPI = {
  // Login
  login: async (email, password) => {
    try {
      const response = await api.post('/api/auth/login', {
        email,
        password
      });
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // Register
  register: async (email, username, password, fullName = null) => {
    try {
      const response = await api.post('/api/auth/register', {
        email,
        username,
        password,
        full_name: fullName
      });
      return response.data;
    } catch (error) {
      console.error('Register error:', error);
      throw error;
    }
  },

  // Get current user
  getCurrentUser: async () => {
    try {
      const response = await api.get('/api/auth/me');
      return response.data;
    } catch (error) {
      console.error('Get current user error:', error);
      throw error;
    }
  },

  // Verify email
  verifyEmail: async (token) => {
    try {
      const response = await api.get(`/api/auth/verify-email?token=${token}`);
      return response.data;
    } catch (error) {
      console.error('Verify email error:', error);
      throw error;
    }
  },
};


export const userAPI = {
  // Get user's lessons
  getLessons: async (skip = 0, limit = 20) => {
    try {
      const response = await api.get(`/api/user/lessons?skip=${skip}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Get lessons error:', error);
      throw error;
    }
  },

  // Get specific lesson details
  getLesson: async (lessonId) => {
    try {
      const response = await api.get(`/api/user/lessons/${lessonId}`);
      return response.data;
    } catch (error) {
      console.error('Get lesson error:', error);
      throw error;
    }
  },

  // Delete lesson
  deleteLesson: async (lessonId) => {
    try {
      const response = await api.delete(`/api/user/lessons/${lessonId}`);
      return response.data;
    } catch (error) {
      console.error('Delete lesson error:', error);
      throw error;
    }
  },

  // Get user statistics
  getStats: async () => {
    try {
      const response = await api.get('/api/user/stats');
      return response.data;
    } catch (error) {
      console.error('Get stats error:', error);
      throw error;
    }
  },
};

export const apiHelpers = {
  // Set auth token
  setAuthToken: (token) => {
    if (token) {
      localStorage.setItem('token', token);
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      localStorage.removeItem('token');
      delete api.defaults.headers.common['Authorization'];
    }
  },

  // Get auth token
  getAuthToken: () => {
    return localStorage.getItem('token');
  },

  // Clear auth token
  clearAuthToken: () => {
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
  },

  // Check if authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },
};

export default api;
