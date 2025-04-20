import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useParams, useNavigate } from "react-router-dom";
import { postApi, commentApi } from "../api/apiService";
import { useAuth } from "../context/AuthContext";
import Layout from "../components/common/Layout";
import CommentItem from "../components/comment/CommentItem";
import CommentInput from "../components/comment/CommentInput";

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

const BackIcon = () => (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"
      fill="currentColor"
    />
  </svg>
);

// 게시물 상세 페이지 컴포넌트
const PostDetailPage = () => {
  const { postId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCommentsLoading, setIsCommentsLoading] = useState(true);
  const [error, setError] = useState("");
  const [isLiked, setIsLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(0);
  const [page, setPage] = useState(1);
  const [hasMoreComments, setHasMoreComments] = useState(true);

  // 게시글 수정 관련 상태
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // 게시물 상세 정보 조회
  useEffect(() => {
    fetchPostDetail();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [postId]);

  // 댓글 목록 조회
  useEffect(() => {
    if (postId) {
      fetchComments();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [postId, page]);

  // 게시물 상세 정보 불러오기
  const fetchPostDetail = async () => {
    try {
      setIsLoading(true);
      setError("");
      const response = await postApi.getPost(postId);
      setPost(response.data);
      setIsLiked(response.data.is_liked || false);
      setLikesCount(response.data.likes_count || 0);
      setEditContent(response.data.content); // 수정 폼을 위해 내용 저장
    } catch (error) {
      console.error("게시물 상세 조회 중 오류 발생:", error);
      setError("게시물을 불러오는 중 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  // 댓글 목록 불러오기
  const fetchComments = async () => {
    try {
      setIsCommentsLoading(true);
      const response = await commentApi.getComments(postId, page);
      const { items, pages } = response.data;

      if (page === 1) {
        setComments(items);
      } else {
        setComments((prevComments) => [...prevComments, ...items]);
      }

      setHasMoreComments(page < pages);
    } catch (error) {
      console.error("댓글 목록 조회 중 오류 발생:", error);
    } finally {
      setIsCommentsLoading(false);
    }
  };

  // 더 많은 댓글 불러오기
  const handleLoadMoreComments = () => {
    if (!isCommentsLoading && hasMoreComments) {
      setPage((prevPage) => prevPage + 1);
    }
  };

  // 좋아요 토글
  const handleLikeToggle = async () => {
    if (!user) return;

    try {
      if (isLiked) {
        const response = await postApi.unlikePost(postId, user.username);
        setLikesCount(response.data.likes_count);
        setIsLiked(false);
      } else {
        const response = await postApi.likePost(postId, user.username);
        setLikesCount(response.data.likes_count);
        setIsLiked(true);
      }
    } catch (error) {
      console.error("좋아요 처리 중 오류 발생:", error);
    }
  };

  // 뒤로가기
  const handleGoBack = () => {
    navigate(-1);
  };

  // 댓글 추가 후 처리
  const handleCommentAdded = (newComment) => {
    setComments((prevComments) => [newComment, ...prevComments]);

    // 게시물의 댓글 수 업데이트
    if (post) {
      setPost({
        ...post,
        comments_count: (post.comments_count || 0) + 1,
      });
    }
  };

  // 댓글 삭제 처리
  const handleCommentDelete = (commentId) => {
    setComments((prevComments) =>
      prevComments.filter((comment) => comment.id !== commentId)
    );

    // 게시물의 댓글 수 업데이트
    if (post) {
      setPost({
        ...post,
        comments_count: Math.max((post.comments_count || 0) - 1, 0),
      });
    }
  };

  // 댓글 업데이트 처리
  const handleCommentUpdate = (updatedComment) => {
    setComments((prevComments) =>
      prevComments.map((comment) =>
        comment.id === updatedComment.id ? updatedComment : comment
      )
    );
  };

  // 게시글 작성자인지 확인
  const isAuthor = user && post && user.userId === post.author.id;

  // 수정 모드 활성화
  const handleEditClick = () => {
    setIsEditing(true);
    setEditContent(post.content);
  };

  // 수정 취소
  const handleEditCancel = () => {
    setIsEditing(false);
    setEditContent(post.content);
  };

  // 수정 내용 저장
  const handleEditSave = async () => {
    if (!editContent.trim()) {
      return;
    }

    try {
      setIsSubmitting(true);
      const response = await postApi.updatePost(
        postId,
        editContent,
        user.username
      );
      setPost(response.data);
      setIsEditing(false);
    } catch (error) {
      console.error("게시글 수정 중 오류 발생:", error);
      alert("게시글 수정 중 오류가 발생했습니다.");
    } finally {
      setIsSubmitting(false);
    }
  };

  // 게시글 삭제
  const handleDeleteClick = async () => {
    if (!window.confirm("정말로 이 게시글을 삭제하시겠습니까?")) {
      return;
    }

    try {
      setIsSubmitting(true);
      await postApi.deletePost(postId, user.username);
      alert("게시글이 삭제되었습니다.");
      navigate("/");
    } catch (error) {
      console.error("게시글 삭제 중 오류 발생:", error);
      alert("게시글 삭제 중 오류가 발생했습니다.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <Layout>
        <LoadingMessage>불러오는 중...</LoadingMessage>
      </Layout>
    );
  }

  if (error || !post) {
    return (
      <Layout>
        <ErrorContainer>
          <ErrorMessage>{error || "게시물을 찾을 수 없습니다."}</ErrorMessage>
          <BackButton onClick={handleGoBack}>
            <BackIcon /> 뒤로 가기
          </BackButton>
        </ErrorContainer>
      </Layout>
    );
  }

  return (
    <Layout>
      <PageContainer>
        <HeaderContainer>
          <BackButton onClick={handleGoBack}>
            <BackIcon /> 뒤로 가기
          </BackButton>
          <PageTitle>게시물 상세</PageTitle>
        </HeaderContainer>

        <PostContainer>
          <UserInfoContainer>
            <UserAvatar />
            <Username>{post.author.username}</Username>
          </UserInfoContainer>

          <ContentContainer>
            {isEditing ? (
              <EditForm>
                <EditTextarea
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  disabled={isSubmitting}
                />
                <EditActions>
                  <EditButton onClick={handleEditSave} disabled={isSubmitting}>
                    저장
                  </EditButton>
                  <CancelButton
                    onClick={handleEditCancel}
                    disabled={isSubmitting}
                  >
                    취소
                  </CancelButton>
                </EditActions>
              </EditForm>
            ) : (
              <PostContent>{post.content}</PostContent>
            )}
          </ContentContainer>

          <ActionsContainer>
            <ActionButton onClick={handleLikeToggle} $isActive={isLiked}>
              <HeartIcon filled={isLiked} />
              {likesCount > 0 && <ActionCount>{likesCount}</ActionCount>}
            </ActionButton>
            <ActionText>댓글 {post.comments_count}</ActionText>
            {isAuthor && !isEditing && (
              <AuthorActions>
                <EditButton onClick={handleEditClick}>수정</EditButton>
                <DeleteButton onClick={handleDeleteClick}>삭제</DeleteButton>
              </AuthorActions>
            )}
          </ActionsContainer>
        </PostContainer>

        <CommentsSection>
          <SectionTitle>댓글</SectionTitle>

          <CommentInput postId={postId} onCommentAdded={handleCommentAdded} />

          {comments.length > 0 ? (
            <CommentsList>
              {comments.map((comment) => (
                <CommentItem
                  key={comment.id}
                  comment={comment}
                  onCommentDelete={handleCommentDelete}
                  onCommentUpdate={handleCommentUpdate}
                />
              ))}
            </CommentsList>
          ) : (
            !isCommentsLoading && (
              <EmptyComments>
                아직 댓글이 없습니다. 첫 댓글을 남겨보세요!
              </EmptyComments>
            )
          )}

          {isCommentsLoading && (
            <LoadingMessage>댓글을 불러오는 중...</LoadingMessage>
          )}

          {hasMoreComments && !isCommentsLoading && (
            <LoadMoreButton onClick={handleLoadMoreComments}>
              댓글 더 보기
            </LoadMoreButton>
          )}
        </CommentsSection>
      </PageContainer>
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

const HeaderContainer = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
`;

const PageTitle = styled.h1`
  font-size: ${(props) => props.theme.fontSizes.lg};
  margin-left: 1rem;
`;

const BackButton = styled.button`
  background: none;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: ${(props) => props.theme.colors.text};
  font-size: ${(props) => props.theme.fontSizes.sm};
  padding: 0.5rem;
  border-radius: 50%;

  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
`;

const PostContainer = styled.div`
  width: 100%;
  border-bottom: 1px solid #333;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
`;

const UserInfoContainer = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
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
  margin-bottom: 1rem;
`;

const PostContent = styled.p`
  font-size: ${(props) => props.theme.fontSizes.md};
  color: ${(props) => props.theme.colors.text};
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
`;

const EditForm = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const EditTextarea = styled.textarea`
  width: 100%;
  font-size: ${(props) => props.theme.fontSizes.md};
  padding: 0.5rem;
  border: 1px solid ${(props) => props.theme.colors.gray};
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
`;

const EditActions = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const EditButton = styled.button`
  background-color: ${(props) => props.theme.colors.primary};
  color: #fff;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};

  &:hover {
    background-color: ${(props) => props.theme.colors.primaryHover};
  }
`;

const CancelButton = styled.button`
  background-color: ${(props) => props.theme.colors.gray};
  color: #fff;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};

  &:hover {
    background-color: ${(props) => props.theme.colors.grayHover};
  }
`;

const ActionsContainer = styled.div`
  display: flex;
  align-items: center;
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

const ActionText = styled.span`
  font-size: ${(props) => props.theme.fontSizes.sm};
  color: ${(props) => props.theme.colors.text};
`;

const AuthorActions = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const DeleteButton = styled.button`
  background-color: ${(props) => props.theme.colors.danger};
  color: #fff;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};

  &:hover {
    background-color: ${(props) => props.theme.colors.dangerHover};
  }
`;

const CommentsSection = styled.section`
  width: 100%;
`;

const SectionTitle = styled.h2`
  font-size: ${(props) => props.theme.fontSizes.md};
  font-weight: ${(props) => props.theme.fontWeights.bold};
  margin-bottom: 1rem;
`;

const CommentsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
`;

const EmptyComments = styled.p`
  text-align: center;
  padding: 2rem 0;
  color: ${(props) => props.theme.colors.gray};
`;

const LoadingMessage = styled.p`
  text-align: center;
  padding: 1rem 0;
  color: ${(props) => props.theme.colors.gray};
`;

const ErrorContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  gap: 1rem;
`;

const ErrorMessage = styled.p`
  color: red;
  text-align: center;
  margin-bottom: 1rem;
`;

const LoadMoreButton = styled.button`
  background: none;
  border: 1px solid ${(props) => props.theme.colors.primary};
  color: ${(props) => props.theme.colors.primary};
  padding: 0.5rem 1rem;
  margin: 1rem auto;
  display: block;
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};

  &:hover {
    background-color: rgba(0, 183, 255, 0.1);
  }
`;

export default PostDetailPage;
