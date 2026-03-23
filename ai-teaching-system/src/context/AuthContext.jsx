// import React, { createContext, useState, useContext, useEffect } from 'react';
// import axios from 'axios';

// const AuthContext = createContext(null);

// export const AuthProvider = ({ children }) => {
//   const [user, setUser] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [token, setToken] = useState(localStorage.getItem('token'));

//   // Set axios default header
//   useEffect(() => {
//     if (token) {
//       axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
//       fetchUser();
//     } else {
//       setLoading(false);
//     }
//   }, [token]);

//   const fetchUser = async () => {
//     try {
//       const response = await axios.get('http://localhost:8000/api/auth/me');
//       setUser(response.data);
//     } catch (error) {
//       console.error('Failed to fetch user:', error);
//       logout();
//     } finally {
//       setLoading(false);
//     }
//   };

//   const login = async (email, password) => {
//     try {
//       const response = await axios.post('http://localhost:8000/api/auth/login', {
//         email,
//         password
//       });
      
//       const { access_token, user: userData } = response.data;
      
//       localStorage.setItem('token', access_token);
//       setToken(access_token);
//       setUser(userData);
      
//       axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
//       return { success: true };
//     } catch (error) {
//       return {
//         success: false,
//         error: error.response?.data?.detail || 'Login failed'
//       };
//     }
//   };

//   const signup = async (email, username, password, fullName) => {
//     try {
//       const response = await axios.post('http://localhost:8000/api/auth/register', {
//         email,
//         username,
//         password,
//         full_name: fullName
//       });
      
//       return { 
//         success: true,
//         message: response.data.message
//       };
//     } catch (error) {
//       return {
//         success: false,
//         error: error.response?.data?.detail || 'Registration failed'
//       };
//     }
//   };

//   const logout = () => {
//     localStorage.removeItem('token');
//     setToken(null);
//     setUser(null);
//     delete axios.defaults.headers.common['Authorization'];
//   };

//   return (
//     <AuthContext.Provider value={{ user, login, signup, logout, loading, isAuthenticated: !!user }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };

// export const useAuth = () => {
//   const context = useContext(AuthContext);
//   if (!context) {
//     throw new Error('useAuth must be used within AuthProvider');
//   }
//   return context;
// };







import React, { createContext, useState, useContext, useEffect } from 'react';
import { authAPI, apiHelpers } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if token exists and fetch user
    if (apiHelpers.isAuthenticated()) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await authAPI.login(email, password);
      
      const { access_token, user: userData } = response;
      
      // Set token in localStorage and axios headers
      apiHelpers.setAuthToken(access_token);
      setUser(userData);
      
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed'
      };
    }
  };

  const signup = async (email, username, password, fullName) => {
    try {
      const response = await authAPI.register(email, username, password, fullName);
      
      return { 
        success: true,
        message: response.message
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Registration failed'
      };
    }
  };

  const logout = () => {
    apiHelpers.clearAuthToken();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      login, 
      signup, 
      logout, 
      loading, 
      isAuthenticated: !!user,
      refreshUser: fetchUser
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};