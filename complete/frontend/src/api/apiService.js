import apiClient from "./apiClient";

// Auth 관련 API
export const authApi = {
  // 로그인 (사용자 이름 설정)
  login: (username) => apiClient.post("/login", { username }),
};

// 포스트 관련 API
export const postApi = {
  // 포스트 목록 조회
  getPosts: (page = 1, limit = 10) =>
    apiClient.get(`/posts?page=${page}&limit=${limit}`),

  // 포스트 상세 조회
  getPost: (postId) => apiClient.get(`/posts/${postId}`),

  // 포스트 생성
  createPost: (content, username) =>
    apiClient.post("/posts", { content, username }),

  // 포스트 수정
  updatePost: (postId, content, username) => {
    return apiClient.put(
      `/posts/${postId}`,
      { content },
      { params: { username } }
    );
  },

  // 포스트 삭제
  deletePost: (postId, username) => {
    return apiClient.delete(`/posts/${postId}`, {
      params: { username },
    });
  },

  // 좋아요 추가 (userId와 username은 헤더에서 전달)
  likePost: (postId, username) => {
    return apiClient.post(`/posts/${postId}/like`, null, {
      params: { username },
    });
  },

  // 좋아요 취소 (userId와 username은 헤더에서 전달)
  unlikePost: (postId, username) => {
    return apiClient.delete(`/posts/${postId}/like`, {
      params: { username },
    });
  },
};

// 댓글 관련 API
export const commentApi = {
  // 댓글 목록 조회
  getComments: (postId, page = 1, limit = 10) =>
    apiClient.get(`/posts/${postId}/comments?page=${page}&limit=${limit}`),

  // 댓글 추가
  createComment: (postId, content, username) =>
    apiClient.post(`/posts/${postId}/comments`, { content, username }),

  // 댓글 수정 - OpenAPI 스키마에 맞게 수정
  updateComment: (commentId, content, username) => {
    return apiClient.put(
      `/comments/${commentId}`,
      { content },
      {
        params: { username },
      }
    );
  },

  // 댓글 삭제
  deleteComment: (commentId, username) => {
    return apiClient.delete(`/comments/${commentId}`, {
      params: { username },
    });
  },
};

// 검색 관련 API
export const searchApi = {
  // 사용자 검색
  searchUsers: (username, page = 1, limit = 10) => {
    // encodeURIComponent 대신 axios의 자동 파라미터 인코딩 사용
    return apiClient.get(`/search`, {
      params: {
        username, // 직접 인코딩하지 않고 axios가 처리하도록 함
        page,
        limit,
      },
    });
  },
};

// 사용자 관련 API
export const userApi = {
  // 사용자 프로필 조회
  getUserProfile: (userId) => apiClient.get(`/users/${userId}`),
};
