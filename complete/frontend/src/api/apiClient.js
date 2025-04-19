import axios from "axios";

// API 기본 설정
const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// 요청 인터셉터 추가
apiClient.interceptors.request.use(
  (config) => {
    // 로컬 스토리지에서 사용자 정보 가져오기
    const userStr = localStorage.getItem("user");
    if (userStr) {
      try {
        const user = JSON.parse(userStr);

        // 사용자 ID는 숫자형이므로 헤더에 안전하게 추가
        if (user.userId) {
          config.headers["X-User-ID"] = user.userId;
        }

        // OpenAPI 문서에 따라 x-username 헤더 사용
        if (user.username) {
          // 한글 등의 유니코드 문자를 위해 encodeURIComponent 사용
          config.headers["x-username"] = encodeURIComponent(user.username);
        }

        // 디버깅 로그
        console.log("사용자 인증 정보 추가:", {
          userId: user.userId,
          username: user.username,
        });
      } catch (error) {
        console.error("사용자 정보 파싱 오류:", error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;
