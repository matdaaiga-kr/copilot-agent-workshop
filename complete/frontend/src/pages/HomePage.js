import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { postApi } from "../api/apiService";
import { useAuth } from "../context/AuthContext";
import Layout from "../components/common/Layout";
import PostCard from "../components/post/PostCard";
import FloatingActionButton from "../components/common/FloatingActionButton";
import PostingModal from "../components/modal/PostingModal";
import NameInputModal from "../components/modal/NameInputModal";

// 홈 페이지 컴포넌트
const HomePage = () => {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [isPostModalOpen, setIsPostModalOpen] = useState(false);
  const [isNameModalOpen, setIsNameModalOpen] = useState(false);
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();

  // 인증 상태 확인하여 로그인 모달 표시
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      setIsNameModalOpen(true);
    } else if (isAuthenticated) {
      // 사용자가 인증되면 게시글 목록 로드
      fetchPosts();
    }
  }, [authLoading, isAuthenticated]);

  // 페이지 변경 시 포스트 목록 조회
  useEffect(() => {
    if (isAuthenticated && page > 1) {
      fetchPosts();
    }
  }, [page, isAuthenticated]);

  // 포스트 목록 불러오기
  const fetchPosts = async () => {
    if (!isAuthenticated) return;

    try {
      setIsLoading(true);
      setError("");
      const response = await postApi.getPosts(page);
      const { items, pages } = response.data;

      if (page === 1) {
        setPosts(items);
      } else {
        setPosts((prevPosts) => [...prevPosts, ...items]);
      }

      setHasMore(page < pages);
    } catch (error) {
      console.error("포스트 목록 조회 중 오류 발생:", error);
      setError("포스트를 불러오는 중 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  // 더 불러오기
  const handleLoadMore = () => {
    if (!isLoading && hasMore) {
      setPage((prevPage) => prevPage + 1);
    }
  };

  // 스크롤 이벤트 처리 (무한 스크롤)
  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + document.documentElement.scrollTop >=
          document.documentElement.scrollHeight - 300 &&
        !isLoading &&
        hasMore
      ) {
        handleLoadMore();
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [isLoading, hasMore]);

  // 포스트 모달 토글
  const togglePostModal = () => {
    setIsPostModalOpen(!isPostModalOpen);
  };

  // 이름 모달 토글
  const toggleNameModal = () => {
    if (isAuthenticated) {
      setIsNameModalOpen(false);
    }
  };

  // 새 포스트 추가 처리
  const handlePostCreated = (newPost) => {
    setPosts((prevPosts) => [newPost, ...prevPosts]);
  };

  // 로그인 완료 후 처리
  const handleLoginSuccess = () => {
    setIsNameModalOpen(false);
    // 로그인 성공 후 포스트 목록 다시 로드
    setPage(1); // 페이지를 1로 초기화
    fetchPosts();
  };

  return (
    <Layout>
      <PageContainer>
        <h1>홈</h1>

        {error && <ErrorMessage>{error}</ErrorMessage>}

        <PostsContainer>
          {posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}

          {isLoading && <LoadingMessage>불러오는 중...</LoadingMessage>}

          {!isLoading && posts.length === 0 && !isNameModalOpen && (
            <EmptyMessage>포스트가 없습니다.</EmptyMessage>
          )}
        </PostsContainer>

        {hasMore && !isLoading && (
          <LoadMoreButton onClick={handleLoadMore}>더 보기</LoadMoreButton>
        )}
      </PageContainer>

      <FloatingActionButton onClick={togglePostModal} />

      {/* 포스트 작성 모달 */}
      <PostingModal
        isOpen={isPostModalOpen}
        onClose={togglePostModal}
        onPostCreated={handlePostCreated}
      />

      {/* 이름 입력 모달 */}
      <NameInputModal isOpen={isNameModalOpen} onClose={handleLoginSuccess} />
    </Layout>
  );
};

// 스타일 컴포넌트
const PageContainer = styled.div`
  width: 100%;
  max-width: ${(props) => props.theme.sizes.maxContentWidth};
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 0;

  h1 {
    align-self: flex-start;
    margin-bottom: 1rem;
    font-size: ${(props) => props.theme.fontSizes.lg};
  }
`;

const PostsContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const ErrorMessage = styled.p`
  color: red;
  margin: 1rem 0;
  text-align: center;
`;

const LoadingMessage = styled.p`
  text-align: center;
  margin: 1rem 0;
  color: ${(props) => props.theme.colors.gray};
`;

const EmptyMessage = styled.p`
  text-align: center;
  margin: 2rem 0;
  color: ${(props) => props.theme.colors.gray};
`;

const LoadMoreButton = styled.button`
  background-color: transparent;
  border: 1px solid ${(props) => props.theme.colors.primary};
  color: ${(props) => props.theme.colors.primary};
  padding: 0.5rem 1rem;
  margin: 1rem 0;
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  cursor: pointer;

  &:hover {
    background-color: rgba(0, 183, 255, 0.1);
  }
`;

export default HomePage;
