import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { userService, postService, authService } from '../services/api';
import { 
  HomeIcon, 
  ProfileIcon, 
  LogoutIcon, 
  HeartIcon, 
  CommentIcon, 
  PlusIcon 
} from './icons/Icons';
import PostModal from './PostModal';
import '../styles/Profile.css';

const Profile = () => {
  const [userProfile, setUserProfile] = useState(null);
  const [userPosts, setUserPosts] = useState([]);
  const [followers, setFollowers] = useState([]);
  const [following, setFollowing] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();

  // 필요한 모든 프로필 데이터를 불러오는 함수
  const fetchProfileData = async () => {
    try {
      setLoading(true);
      // 병렬로 여러 API 요청 실행
      const [profileResponse, postsResponse, followersResponse, followingResponse] = await Promise.all([
        userService.getMyInfo(),
        postService.getMyPosts(),
        userService.getFollowers(),
        userService.getFollowing()
      ]);

      setUserProfile(profileResponse);
      setUserPosts(postsResponse.posts || []);
      setFollowers(followersResponse.followers || []);
      setFollowing(followingResponse.following || []);
      setError(null);
    } catch (err) {
      console.error('프로필 데이터를 불러오는 중 오류가 발생했습니다:', err);
      setError('프로필 데이터를 불러오는 중 오류가 발생했습니다.');
      if (err.response && err.response.status === 401) {
        // 인증 오류 시 로그인 페이지로 이동
        authService.logout();
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  // 컴포넌트 마운트 시 프로필 데이터 불러오기
  useEffect(() => {
    fetchProfileData();
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
      setUserPosts(prevPosts => 
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

  // 홈 페이지로 이동
  const goToHome = () => {
    navigate('/');
  };

  // 새 게시글 작성 모달 열기
  const openPostModal = () => {
    setIsModalOpen(true);
  };

  // 새 게시글 작성 완료 후 처리
  const handlePostComplete = (newPost) => {
    // 새 게시글을 목록 맨 앞에 추가
    setUserPosts(prevPosts => [newPost, ...prevPosts]);
  };

  // 프로필 수정 페이지로 이동
  const goToEditProfile = () => {
    navigate('/edit-profile');
  };

  return (
    <div className="profile-container">
      {/* 왼쪽 사이드바 */}
      <div className="sidebar">
        <div className="sidebar-icon" onClick={goToHome}>
          <HomeIcon />
        </div>
        <div className="sidebar-icon">
          <ProfileIcon />
        </div>
        <div className="sidebar-icon" onClick={handleLogout}>
          <LogoutIcon />
        </div>
      </div>
      
      {/* 메인 콘텐츠 영역 */}
      <div className="profile-content-area">
        {loading ? (
          <div className="loading-message">프로필 정보를 불러오는 중...</div>
        ) : error ? (
          <div className="error-message">{error}</div>
        ) : (
          <div className="profile-section">
            {/* 프로필 헤더 */}
            <div className="profile-header">
              <div className="profile-avatar">
                {userProfile?.profile_image_url && (
                  <img src={userProfile.profile_image_url} alt="프로필 이미지" />
                )}
              </div>
              <h1 className="profile-username">{userProfile?.username}</h1>
            </div>
            
            {/* 프로필 통계 */}
            <div className="profile-stats">
              <div className="profile-stat">
                <span className="stat-value">{following.length}</span>
                <span className="stat-label">팔로잉</span>
              </div>
              <div className="profile-stat">
                <span className="stat-value">{userPosts.length}</span>
                <span className="stat-label">게시글</span>
              </div>
              <div className="profile-stat">
                <span className="stat-value">{followers.length}</span>
                <span className="stat-label">팔로워</span>
              </div>
            </div>
            
            {/* 프로필 수정 버튼 */}
            <div style={{ textAlign: 'center' }}>
              <button className="profile-edit-button" onClick={goToEditProfile}>
                프로필 수정
              </button>
            </div>
            
            <hr className="divider" />
            
            {/* 사용자 게시글 목록 */}
            <div className="profile-posts-section">
              {userPosts.length === 0 ? (
                <div className="no-posts" style={{ textAlign: 'center' }}>아직 게시글이 없습니다.</div>
              ) : (
                userPosts.map((post, index) => (
                  <React.Fragment key={post.id}>
                    <div className="profile-post-item">
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
                    {index < userPosts.length - 1 && <hr className="post-divider" />}
                  </React.Fragment>
                ))
              )}
            </div>
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

export default Profile;