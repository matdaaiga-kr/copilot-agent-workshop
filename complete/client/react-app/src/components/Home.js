import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { postService, authService } from '../services/api';
import { 
  HomeIcon, 
  ProfileIcon, 
  LogoutIcon, 
  HeartIcon, 
  CommentIcon, 
  PlusIcon 
} from '../components/icons/Icons';
import PostModal from './PostModal';
import '../styles/Home.css';

const Home = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();

  // 게시글 목록 불러오기
  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await postService.getAllPosts();
      setPosts(response.posts || []);
      setError(null);
    } catch (err) {
      console.error('게시글을 불러오는 중 오류가 발생했습니다:', err);
      setError('게시글을 불러오는 중 오류가 발생했습니다.');
      if (err.response && err.response.status === 401) {
        // 인증 오류 시 로그인 페이지로 이동
        authService.logout();
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  // 컴포넌트 마운트 시 게시글 목록 불러오기
  useEffect(() => {
    fetchPosts();
  }, []);

  // 좋아요 토글 기능
  const toggleLike = async (postId, isLiked) => {
    try {
      if (isLiked) {
        await postService.unlikePost(postId);
      } else {
        await postService.likePost(postId);
      }
      
      // 좋아요 상태 업데이트
      setPosts(prevPosts => 
        prevPosts.map(post => {
          if (post.id === postId) {
            return {
              ...post,
              is_liked: !isLiked,
              likes_count: isLiked 
                ? Math.max(0, post.likes_count - 1) 
                : post.likes_count + 1
            };
          }
          return post;
        })
      );
    } catch (err) {
      console.error('좋아요 처리 중 오류가 발생했습니다:', err);
      if (err.response && err.response.status === 401) {
        authService.logout();
        navigate('/login');
      }
    }
  };

  // 로그아웃 처리
  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  // 프로필 페이지로 이동
  const goToProfile = () => {
    navigate('/profile');
  };

  // 새 게시글 작성 모달 열기
  const openPostModal = () => {
    setIsModalOpen(true);
  };

  // 새 게시글 작성 완료 후 처리
  const handlePostComplete = (newPost) => {
    // 새 게시글을 목록 맨 앞에 추가
    setPosts(prevPosts => [newPost, ...prevPosts]);
  };

  return (
    <div className="home-container">
      {/* 왼쪽 사이드바 */}
      <div className="sidebar">
        <div className="sidebar-icon">
          <HomeIcon />
        </div>
        <div className="sidebar-icon" onClick={goToProfile}>
          <ProfileIcon />
        </div>
        <div className="sidebar-icon" onClick={handleLogout}>
          <LogoutIcon />
        </div>
      </div>
      
      {/* 메인 콘텐츠 영역 */}
      <div className="content-area">
        {loading ? (
          <div className="loading-message">게시글을 불러오는 중...</div>
        ) : error ? (
          <div className="error-message">{error}</div>
        ) : (
          <div className="post-list">
            {posts.length === 0 ? (
              <div className="no-posts">아직 게시글이 없습니다.</div>
            ) : (
              posts.map((post, index) => (
                <React.Fragment key={post.id}>
                  <div className="post-item">
                    <div className="post-user">
                      <div className="post-avatar"></div>
                      <div className="post-username">{post.user.username}</div>
                    </div>
                    <div className="post-content">{post.content}</div>
                    <div className="post-actions">
                      <div 
                        className={`action-icon ${post.is_liked ? 'liked' : ''}`}
                        onClick={() => toggleLike(post.id, post.is_liked)}
                      >
                        <HeartIcon />
                      </div>
                      <div className="action-icon">
                        <CommentIcon />
                      </div>
                    </div>
                  </div>
                  {index < posts.length - 1 && <hr className="post-divider" />}
                </React.Fragment>
              ))
            )}
          </div>
        )}
      </div>
      
      {/* 새 게시글 작성 버튼 */}
      <button className="create-post-button" onClick={openPostModal}>
        <PlusIcon />
      </button>

      {/* 게시글 작성 모달 */}
      <PostModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onPostComplete={handlePostComplete}
      />
    </div>
  );
};

export default Home;