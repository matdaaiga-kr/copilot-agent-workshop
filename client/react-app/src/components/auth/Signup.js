import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/api';
import '../../styles/Signup.css';

const Signup = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    setError('');
    
    // 비밀번호 일치 확인
    if (password !== confirmPassword) {
      setError('비밀번호가 일치하지 않습니다.');
      return;
    }
    
    setIsLoading(true);
    
    try {
      await authService.signup(username, password);
      // 회원가입 성공 후 로그인 페이지로 이동
      navigate('/login');
    } catch (err) {
      console.error('회원가입 오류:', err);
      if (err.response && err.response.status === 400) {
        setError('이미 사용 중인 사용자명입니다.');
      } else {
        setError('회원가입 중 오류가 발생했습니다. 다시 시도해주세요.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="signup-container">
      <div className="signup-box">
        <h1 className="signup-title">환영합니다!</h1>
        
        <form onSubmit={handleSignup}>
          <div className="input-group">
            <input
              type="text"
              className="signup-input"
              placeholder="UserName"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          
          <div className="input-group">
            <input
              type="password"
              className="signup-input"
              placeholder="PW"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <div className="input-group">
            <input
              type="password"
              className="signup-input"
              placeholder="PW (again)"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          
          <button
            type="submit"
            className="signup-button"
            disabled={isLoading}
          >
            {isLoading ? '처리 중...' : '회원가입'}
          </button>
          
          {error && <div className="error-message">{error}</div>}
        </form>
        
        <div className="login-link">
          <span>이미 계정이 있나요? </span>
          <a href="#" onClick={handleLoginClick}>로그인</a>
        </div>
      </div>
    </div>
  );
};

export default Signup;