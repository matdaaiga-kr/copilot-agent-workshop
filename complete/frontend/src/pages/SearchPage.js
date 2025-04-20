import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { searchApi } from "../api/apiService";
import { useAuth } from "../context/AuthContext";
import Layout from "../components/common/Layout";
import FloatingActionButton from "../components/common/FloatingActionButton";
import PostingModal from "../components/modal/PostingModal";

// 검색 아이콘 컴포넌트
const SearchIcon = () => (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M15.5 14H14.71L14.43 13.73C15.41 12.59 16 11.11 16 9.5C16 5.91 13.09 3 9.5 3C5.91 3 3 5.91 3 9.5C3 13.09 5.91 16 9.5 16C11.11 16 12.59 15.41 13.73 14.43L14 14.71V15.5L19 20.49L20.49 19L15.5 14ZM9.5 14C7.01 14 5 11.99 5 9.5C5 7.01 7.01 5 9.5 5C11.99 5 14 7.01 14 9.5C14 11.99 11.99 14 9.5 14Z"
      fill="currentColor"
    />
  </svg>
);

// 검색 페이지 컴포넌트
const SearchPage = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [isPostModalOpen, setIsPostModalOpen] = useState(false);
  const { isAuthenticated } = useAuth();
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);

  // 검색어 입력 처리
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  // 검색 실행
  const handleSearch = async (e) => {
    e?.preventDefault();

    if (!searchTerm.trim()) return;

    try {
      setIsLoading(true);
      setError("");
      setPage(1);

      const response = await searchApi.searchUsers(searchTerm, 1);

      // 검색 결과가 없는 경우
      if (!response.data.items || response.data.items.length === 0) {
        setSearchResults([]);
        setHasMore(false);
        return;
      }

      // 응답 데이터에서 사용자 이름이 인코딩된 채로 오는 경우를 처리
      const processedResults =
        response.data.items?.map((user) => ({
          ...user,
          username:
            typeof user.username === "string"
              ? decodeURIComponent(user.username)
              : user.username,
        })) || [];

      setSearchResults(processedResults);
      setHasMore(response.data.page < response.data.pages);
    } catch (error) {
      if (error.response) {
        console.error("오류 응답:", error.response.data);
        console.error("오류 상태:", error.response.status);
      }
      setError("검색 중 오류가 발생했습니다.");
      setSearchResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  // 더 많은 결과 불러오기
  const handleLoadMore = async () => {
    if (isLoading || !hasMore) return;

    try {
      setIsLoading(true);
      const nextPage = page + 1;

      const response = await searchApi.searchUsers(searchTerm, nextPage);

      // 추가 결과의 사용자 이름도 디코딩 처리
      const processedResults =
        response.data.items?.map((user) => ({
          ...user,
          username:
            typeof user.username === "string"
              ? decodeURIComponent(user.username)
              : user.username,
        })) || [];

      setSearchResults((prev) => [...prev, ...processedResults]);
      setPage(nextPage);
      setHasMore(response.data.page < response.data.pages);
    } catch (error) {
      if (error.response) {
        console.error("오류 응답:", error.response.data);
        console.error("오류 상태:", error.response.status);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // 포스트 모달 토글
  const togglePostModal = () => {
    setIsPostModalOpen(!isPostModalOpen);
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isLoading, hasMore]);

  // Enter 키로 검색 실행
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.key === "Enter" && document.activeElement.id === "search-input") {
        handleSearch();
      }
    };

    window.addEventListener("keypress", handleKeyPress);
    return () => window.removeEventListener("keypress", handleKeyPress);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchTerm]);

  return (
    <Layout>
      <PageContainer>
        <h1>검색</h1>

        <SearchContainer onSubmit={handleSearch}>
          <SearchInputContainer>
            <SearchInput
              id="search-input"
              type="text"
              value={searchTerm}
              onChange={handleSearchChange}
              placeholder="사용자 이름 검색"
              disabled={isLoading}
            />
            <SearchButton
              type="submit"
              disabled={isLoading || !searchTerm.trim()}
            >
              <SearchIcon />
            </SearchButton>
          </SearchInputContainer>
        </SearchContainer>

        {error && <ErrorMessage>{error}</ErrorMessage>}

        <ResultsContainer>
          {searchResults.length > 0 ? (
            <>
              <ResultsCount>
                '{searchTerm}' 검색 결과: {searchResults.length}명
              </ResultsCount>
              <UserList>
                {searchResults.map((user) => (
                  <UserItem key={user.id}>
                    <UserAvatar />
                    <UserInfo>
                      <Username>{user.username}</Username>
                    </UserInfo>
                  </UserItem>
                ))}
              </UserList>

              {isLoading && <LoadingMessage>불러오는 중...</LoadingMessage>}

              {hasMore && !isLoading && (
                <LoadMoreButton onClick={handleLoadMore}>
                  더 보기
                </LoadMoreButton>
              )}
            </>
          ) : (
            !isLoading &&
            searchTerm && (
              <EmptyResults>
                '{searchTerm}'에 대한 검색 결과가 없습니다.
              </EmptyResults>
            )
          )}

          {!searchTerm && !isLoading && (
            <SearchPrompt>사용자 이름을 검색해보세요.</SearchPrompt>
          )}
        </ResultsContainer>
      </PageContainer>

      {isAuthenticated && (
        <>
          <FloatingActionButton onClick={togglePostModal} />
          <PostingModal isOpen={isPostModalOpen} onClose={togglePostModal} />
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

  h1 {
    margin-bottom: 1.5rem;
    font-size: ${(props) => props.theme.fontSizes.lg};
  }
`;

const SearchContainer = styled.form`
  width: 100%;
  margin-bottom: 1.5rem;
`;

const SearchInputContainer = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  background-color: ${(props) => props.theme.colors.gray};
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  overflow: hidden;
`;

const SearchInput = styled.input`
  flex: 1;
  padding: 0.75rem 1rem;
  font-size: ${(props) => props.theme.fontSizes.md};
  color: ${(props) => props.theme.colors.background};
  background: none;

  &::placeholder {
    color: ${(props) => props.theme.colors.darkGray};
  }

  &:disabled {
    opacity: 0.7;
  }
`;

const SearchButton = styled.button`
  background-color: ${(props) => props.theme.colors.primary};
  color: ${(props) => props.theme.colors.text};
  padding: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
`;

const ResultsContainer = styled.div`
  width: 100%;
`;

const ResultsCount = styled.div`
  font-size: ${(props) => props.theme.fontSizes.sm};
  color: ${(props) => props.theme.colors.text};
  margin-bottom: 1rem;
`;

const UserList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const UserItem = styled.div`
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border-bottom: 1px solid #333;

  &:hover {
    background-color: rgba(255, 255, 255, 0.05);
  }
`;

const UserAvatar = styled.div`
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: ${(props) => props.theme.colors.gray};
  margin-right: 1rem;
`;

const UserInfo = styled.div`
  display: flex;
  flex-direction: column;
`;

const Username = styled.div`
  font-size: ${(props) => props.theme.fontSizes.md};
  font-weight: ${(props) => props.theme.fontWeights.bold};
  color: ${(props) => props.theme.colors.text};
`;

const ErrorMessage = styled.p`
  color: red;
  margin-bottom: 1rem;
`;

const LoadingMessage = styled.p`
  text-align: center;
  padding: 1rem;
  color: ${(props) => props.theme.colors.gray};
`;

const EmptyResults = styled.p`
  text-align: center;
  padding: 2rem 0;
  color: ${(props) => props.theme.colors.gray};
`;

const SearchPrompt = styled.p`
  text-align: center;
  padding: 2rem 0;
  color: ${(props) => props.theme.colors.gray};
`;

const LoadMoreButton = styled.button`
  background: none;
  border: 1px solid ${(props) => props.theme.colors.primary};
  color: ${(props) => props.theme.colors.primary};
  padding: 0.5rem;
  margin: 1rem auto;
  display: block;
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};

  &:hover {
    background-color: rgba(0, 183, 255, 0.1);
  }
`;

export default SearchPage;
