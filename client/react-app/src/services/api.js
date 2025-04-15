import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터: 토큰이 있으면 헤더에 추가
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 인증 관련 API 호출
export const authService = {
  login: async (username, password) => {
    try {
      const response = await api.post('/auth/login', { username, password });
      const { access_token, refresh_token } = response.data;
      
      // 토큰 저장
      localStorage.setItem('accessToken', access_token);
      localStorage.setItem('refreshToken', refresh_token);
      
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  signup: async (username, password) => {
    try {
      const response = await api.post('/auth/signup', { username, password });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }
};

// 게시글 관련 API 호출
export const postService = {
  // 모든 게시글 가져오기
  getAllPosts: async () => {
    try {
      const response = await api.get('/posts');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  // 특정 게시글 상세 정보 가져오기
  getPostDetail: async (postId) => {
    try {
      const response = await api.get(`/posts/${postId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  // 내 게시글 목록 가져오기
  getMyPosts: async () => {
    try {
      const response = await api.get('/profile/posts');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  // 게시글 생성하기
  createPost: async (content) => {
    try {
      const response = await api.post('/posts', { content });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  // 게시글 좋아요/좋아요 취소
  likePost: async (postId) => {
    try {
      const response = await api.post(`/posts/${postId}/like`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  unlikePost: async (postId) => {
    try {
      const response = await api.delete(`/posts/${postId}/like`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

// 사용자 관련 API 호출
export const userService = {
  // 내 정보 가져오기
  getMyInfo: async () => {
    try {
      const response = await api.get('/users/me');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  // 팔로워 목록 가져오기
  getFollowers: async () => {
    try {
      const response = await api.get('/profile/followers');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  // 팔로잉 목록 가져오기
  getFollowing: async () => {
    try {
      const response = await api.get('/profile/following');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  // 프로필 정보 가져오기
  getProfile: async () => {
    try {
      const response = await api.get('/profile');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  // 프로필 정보 업데이트
  updateProfile: async (formData) => {
    try {
      const response = await api.put('/users/me', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default api;