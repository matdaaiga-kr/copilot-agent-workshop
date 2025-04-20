import React from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { postApi } from "../../api/apiService";
import { useAuth } from "../../context/AuthContext";

// 아이콘 컴포넌트
const HeartIcon = ({ filled }) => (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
      fill={filled ? "currentColor" : "none"}
      stroke={filled ? "none" : "currentColor"}
      strokeWidth="2"
    />
  </svg>
);

const CommentIcon = () => (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M21 6h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1zm-4 6V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v14l4-4h10c.55 0 1-.45 1-1z"
      fill="currentColor"
    />
  </svg>
);

// 게시물 카드 컴포넌트
const PostCard = ({ post }) => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [isLiked, setIsLiked] = React.useState(post.is_liked || false);
  const [likesCount, setLikesCount] = React.useState(post.likes_count || 0);

  // 게시물 상세 페이지로 이동
  const handlePostClick = () => {
    navigate(`/post/${post.id}`);
  };

  // 좋아요 토글
  const handleLikeToggle = async (e) => {
    e.stopPropagation(); // 부모 요소 클릭 이벤트 방지

    try {
      if (!user) return; // 로그인되지 않은 경우

      if (isLiked) {
        const response = await postApi.unlikePost(post.id, user.username);
        setLikesCount(response.data.likes_count);
        setIsLiked(false);
      } else {
        const response = await postApi.likePost(post.id, user.username);
        setLikesCount(response.data.likes_count);
        setIsLiked(true);
      }
    } catch (error) {
      console.error("좋아요 처리 중 오류 발생:", error);
    }
  };

  // 댓글 버튼 클릭 시 게시물 상세 페이지로 이동
  const handleCommentClick = (e) => {
    e.stopPropagation();
    navigate(`/post/${post.id}`);
  };

  return (
    <PostContainer>
      <UserInfoContainer>
        <UserAvatar />
        <Username>{post.author.username}</Username>
      </UserInfoContainer>

      <ContentContainer onClick={handlePostClick}>
        <PostContent>{post.content}</PostContent>
      </ContentContainer>

      <ActionsContainer>
        <ActionButton onClick={handleLikeToggle} $isActive={isLiked}>
          <HeartIcon filled={isLiked} />
          {likesCount > 0 && <ActionCount>{likesCount}</ActionCount>}
        </ActionButton>
        <ActionButton onClick={handleCommentClick}>
          <CommentIcon />
          {post.comments_count > 0 && (
            <ActionCount>{post.comments_count}</ActionCount>
          )}
        </ActionButton>
      </ActionsContainer>
    </PostContainer>
  );
};

// 스타일 컴포넌트
const PostContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: ${(props) => props.theme.sizes.maxContentWidth};
  background-color: ${(props) => props.theme.colors.background};
  border-bottom: 1px solid #333;
  padding: 1rem 0;
`;

const UserInfoContainer = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
`;

const UserAvatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: ${(props) => props.theme.colors.gray};
  margin-right: 0.5rem;
`;

const Username = styled.div`
  font-size: ${(props) => props.theme.fontSizes.md};
  font-weight: ${(props) => props.theme.fontWeights.bold};
  color: ${(props) => props.theme.colors.text};
`;

const ContentContainer = styled.div`
  cursor: pointer;
  margin-bottom: 0.5rem;
  padding: 0.5rem 0;
`;

const PostContent = styled.p`
  font-size: ${(props) => props.theme.fontSizes.md};
  color: ${(props) => props.theme.colors.text};
  line-height: 1.4;
`;

const ActionsContainer = styled.div`
  display: flex;
  gap: 1rem;
`;

const ActionButton = styled.button`
  background: none;
  display: flex;
  align-items: center;
  color: ${(props) =>
    props.$isActive ? props.theme.colors.heart : props.theme.colors.text};
  gap: 4px;
`;

const ActionCount = styled.span`
  font-size: ${(props) => props.theme.fontSizes.xs};
`;

export default PostCard;
