import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useNavigate, useParams } from "react-router-dom";
import { userApi } from "../api/apiService";
import { useAuth } from "../context/AuthContext";
import Layout from "../components/common/Layout";
import PostCard from "../components/post/PostCard";
import FloatingActionButton from "../components/common/FloatingActionButton";
import PostingModal from "../components/modal/PostingModal";

// 프로필 페이지 컴포넌트
const ProfilePage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { userId: urlUserId } = useParams(); // URL에서 userId 가져오기
  const [userProfile, setUserProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [isPostModalOpen, setIsPostModalOpen] = useState(false);
  const [isMyProfile, setIsMyProfile] = useState(false);

  // 표시할 사용자 ID 결정 (문자열로 받은 urlUserId를 숫자로 변환)
  const profileUserId = urlUserId
    ? parseInt(urlUserId)
    : user
    ? user.userId
    : null;

  // 내 프로필인지 확인
  useEffect(() => {
    if (user && profileUserId) {
      setIsMyProfile(profileUserId === user.userId);
    } else {
      setIsMyProfile(false);
    }
  }, [user, profileUserId]);

  // 사용자 프로필 정보 조회
  useEffect(() => {
    if (profileUserId) {
      fetchUserProfile(profileUserId);
    } else {
      setIsLoading(false);
    }
  }, [profileUserId]);

  // 프로필 정보 불러오기
  const fetchUserProfile = async (userId) => {
    try {
      setIsLoading(true);
      setError("");

      // 헤더에 사용자 인증 정보 포함되도록 요청
      const response = await userApi.getUserProfile(userId);

      // 응답 데이터 처리 및 디코딩이 필요한 경우 처리
      const profileData = response.data;

      // username이 인코딩되어 있는 경우 디코딩
      if (profileData.username && typeof profileData.username === "string") {
        try {
          profileData.username = decodeURIComponent(profileData.username);
        } catch (e) {}
      }

      // 게시글 정보가 있는지 확인하고 가공
      if (profileData.posts) {
        // 게시글 목록도 디코딩이 필요한 경우 처리
        profileData.posts = profileData.posts.map((post) => {
          if (post.author && post.author.username) {
            try {
              post.author.username = decodeURIComponent(post.author.username);
            } catch (e) {}
          }
          return post;
        });

        // 게시글 정렬 (최신순)
        profileData.posts.sort(
          (a, b) => new Date(b.created_at) - new Date(a.created_at)
        );
      } else {
        // 게시글이 없는 경우 빈 배열로 초기화
        profileData.posts = [];
      }

      // 댓글 정보가 있는지 확인하고 가공
      if (profileData.comments) {
        profileData.comments = profileData.comments.map((comment) => {
          if (comment.author && comment.author.username) {
            try {
              comment.author.username = decodeURIComponent(
                comment.author.username
              );
            } catch (e) {}
          }
          return comment;
        });
      } else {
        profileData.comments = [];
      }

      setUserProfile(profileData);
    } catch (error) {
      console.error("프로필 정보 조회 중 오류 발생:", error);
      if (error.response) {
        console.error("오류 응답:", error.response.data);
        console.error("오류 상태:", error.response.status);
      }
      setError("프로필 정보를 불러오는 중 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  // 로그아웃 처리
  const handleLogout = () => {
    if (window.confirm("로그아웃 하시겠습니까?")) {
      logout();
      navigate("/");
    }
  };

  // 포스팅 모달 토글
  const togglePostModal = () => {
    setIsPostModalOpen(!isPostModalOpen);
  };

  // 포스트 생성 후 처리
  const handlePostCreated = (newPost) => {
    if (userProfile) {
      setUserProfile({
        ...userProfile,
        posts: [newPost, ...userProfile.posts],
        posts_count: userProfile.posts_count + 1,
      });
    }
  };

  if (!profileUserId) {
    return (
      <Layout>
        <NotLoggedInMessage>
          <p>로그인이 필요합니다.</p>
          <LoginButton onClick={() => navigate("/")}>홈으로 이동</LoginButton>
        </NotLoggedInMessage>
      </Layout>
    );
  }

  if (isLoading) {
    return (
      <Layout>
        <LoadingMessage>프로필 정보를 불러오는 중...</LoadingMessage>
      </Layout>
    );
  }

  if (!userProfile) {
    return (
      <Layout>
        <ErrorMessage>사용자를 찾을 수 없습니다.</ErrorMessage>
        <BackButton onClick={() => navigate(-1)}>뒤로 가기</BackButton>
      </Layout>
    );
  }

  return (
    <Layout>
      <PageContainer>
        <ProfileHeader>
          <ProfileInfoContainer>
            <UserAvatar />
            <UserInfo>
              <Username>{userProfile.username}</Username>
              <PostsCount>게시물 {userProfile?.posts_count || 0}개</PostsCount>
            </UserInfo>
          </ProfileInfoContainer>

          {isMyProfile && (
            <LogoutButton onClick={handleLogout}>로그아웃</LogoutButton>
          )}
        </ProfileHeader>

        {error && <ErrorMessage>{error}</ErrorMessage>}

        <PostsSection>
          <SectionTitle>
            {isMyProfile ? "내 게시물" : `${userProfile.username}님의 게시물`}
          </SectionTitle>

          {userProfile?.posts && userProfile.posts.length > 0 ? (
            <PostsGrid>
              {userProfile.posts.map((post) => (
                <PostCard key={post.id} post={post} />
              ))}
            </PostsGrid>
          ) : (
            <EmptyMessage>아직 게시물이 없습니다.</EmptyMessage>
          )}
        </PostsSection>
      </PageContainer>

      {isMyProfile && (
        <>
          <FloatingActionButton onClick={togglePostModal} />
          <PostingModal
            isOpen={isPostModalOpen}
            onClose={togglePostModal}
            onPostCreated={handlePostCreated}
          />
        </>
      )}
    </Layout>
  );
};

// 스타일 컴포넌트
const PageContainer = styled.div`
  width: 100%;
  max-width: ${(props) => props.theme.sizes.maxContentWidth};
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
`;

const ProfileHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
`;

const ProfileInfoContainer = styled.div`
  display: flex;
  align-items: center;
`;

const UserAvatar = styled.div`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: ${(props) => props.theme.colors.gray};
  margin-right: 1rem;
`;

const UserInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Username = styled.h1`
  font-size: ${(props) => props.theme.fontSizes.lg};
  font-weight: ${(props) => props.theme.fontWeights.bold};
  color: ${(props) => props.theme.colors.text};
`;

const PostsCount = styled.span`
  font-size: ${(props) => props.theme.fontSizes.sm};
  color: ${(props) => props.theme.colors.gray};
`;

const LogoutButton = styled.button`
  background-color: transparent;
  border: 1px solid ${(props) => props.theme.colors.primary};
  color: ${(props) => props.theme.colors.primary};
  padding: 0.5rem 1rem;
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  font-size: ${(props) => props.theme.fontSizes.sm};

  &:hover {
    background-color: rgba(0, 183, 255, 0.1);
  }
`;

const PostsSection = styled.section`
  width: 100%;
`;

const SectionTitle = styled.h2`
  font-size: ${(props) => props.theme.fontSizes.md};
  font-weight: ${(props) => props.theme.fontWeights.bold};
  margin-bottom: 1rem;
  border-bottom: 1px solid #333;
  padding-bottom: 0.5rem;
`;

const PostsGrid = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const EmptyMessage = styled.p`
  text-align: center;
  padding: 2rem 0;
  color: ${(props) => props.theme.colors.gray};
`;

const LoadingMessage = styled.p`
  text-align: center;
  padding: 2rem 0;
  color: ${(props) => props.theme.colors.gray};
`;

const ErrorMessage = styled.p`
  color: red;
  margin: 2rem 0;
  text-align: center;
`;

const NotLoggedInMessage = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  gap: 1rem;

  p {
    font-size: ${(props) => props.theme.fontSizes.md};
    color: ${(props) => props.theme.colors.gray};
  }
`;

const LoginButton = styled.button`
  background-color: ${(props) => props.theme.colors.primary};
  color: ${(props) => props.theme.colors.text};
  padding: 0.75rem 1.5rem;
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  font-size: ${(props) => props.theme.fontSizes.sm};
`;

const BackButton = styled.button`
  background-color: ${(props) => props.theme.colors.primary};
  color: ${(props) => props.theme.colors.text};
  padding: 0.5rem 1rem;
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  font-size: ${(props) => props.theme.fontSizes.sm};
  margin: 0 auto;
  display: block;
`;

export default ProfilePage;
