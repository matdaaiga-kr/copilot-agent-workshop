import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { ThemeProvider } from "styled-components";
import { AuthProvider } from "./context/AuthContext";

// 스타일
import GlobalStyle from "./styles/GlobalStyle";
import theme from "./styles/theme";

// 페이지
import HomePage from "./pages/HomePage";
import PostDetailPage from "./pages/PostDetailPage";
import SearchPage from "./pages/SearchPage";
import ProfilePage from "./pages/ProfilePage";

function App() {
  return (
    <AuthProvider>
      <ThemeProvider theme={theme}>
        <GlobalStyle />
        <Router
          future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
        >
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/post/:postId" element={<PostDetailPage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/profile/:userId" element={<ProfilePage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;
