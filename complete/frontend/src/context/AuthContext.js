import React, { createContext, useContext, useState, useEffect } from "react";
import { authApi } from "../api/apiService";

// 사용자 인증 컨텍스트 생성
const AuthContext = createContext(null);

// AuthProvider 컴포넌트 정의
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // 컴포넌트 마운트 시 로컬 스토리지에서 사용자 정보 확인
  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (error) {
        // 유효하지 않은 JSON 처리
        console.error("저장된 사용자 정보 파싱 오류:", error);
        localStorage.removeItem("user");
      }
    }
    setIsLoading(false);
  }, []);

  // 로그인 함수
  const login = async (username) => {
    try {
      setIsLoading(true);
      const response = await authApi.login(username);
      const userData = response.data;

      // 사용자 정보 상태 및 로컬 스토리지에 저장
      setUser(userData);
      localStorage.setItem("user", JSON.stringify(userData));

      return userData;
    } catch (error) {
      console.error("로그인 오류:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // 로그아웃 함수
  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  // 컨텍스트 값 정의
  const value = {
    user,
    isLoading,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// 커스텀 훅 정의
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth는 AuthProvider 내부에서만 사용할 수 있습니다");
  }
  return context;
};
