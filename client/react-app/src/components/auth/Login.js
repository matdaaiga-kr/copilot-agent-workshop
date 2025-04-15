import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/api';
import '../../styles/Login.css';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      await authService.login(username, password);
      navigate('/'); // 로그인 성공 후 홈페이지로 이동
    } catch (err) {
      console.error('로그인 오류:', err);
      if (err.response && err.response.status === 401) {
        setError('아이디 또는 비밀번호가 올바르지 않습니다.');
      } else {
        setError('로그인 중 오류가 발생했습니다. 다시 시도해주세요.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignupClick = () => {
    navigate('/signup');
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1 className="login-title">다시 돌아오신 것을 환영합니다</h1>
        
        <form onSubmit={handleLogin}>
          <div className="input-group">
            <input
              type="text"
              className="login-input"
              placeholder="userName"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          
          <div className="input-group">
            <input
              type="password"
              className="login-input"
              placeholder="PW"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button
            type="submit"
            className="login-button"
            disabled={isLoading}
          >
            {isLoading ? '로그인 중...' : '로그인'}
          </button>
          
          {error && <div className="error-message">{error}</div>}
        </form>
        
        <div className="signup-link">
          <span>아직 회원이 아니신가요? </span>
          <a href="#" onClick={handleSignupClick}>회원가입</a>
        </div>
      </div>
    </div>
  );
};

export default Login;