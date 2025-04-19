import React, { useState } from "react";
import styled from "styled-components";
import { useAuth } from "../../context/AuthContext";
import { commentApi } from "../../api/apiService";

// 댓글 입력 컴포넌트
const CommentInput = ({ postId, onCommentAdded }) => {
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { user } = useAuth();

  const handleContentChange = (e) => {
    setContent(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!content.trim() || !user) return;

    setIsLoading(true);

    try {
      const response = await commentApi.createComment(
        postId,
        content,
        user.username
      );
      setContent("");
      if (onCommentAdded) {
        onCommentAdded(response.data);
      }
    } catch (error) {
      console.error("댓글 추가 중 오류 발생:", error);
      alert("댓글을 추가하는 중 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <CommentInputContainer>
      <CommentForm onSubmit={handleSubmit}>
        <CommentTextarea
          value={content}
          onChange={handleContentChange}
          placeholder="댓글 달기"
          disabled={isLoading || !user}
        />
        <SubmitButton
          type="submit"
          disabled={!content.trim() || isLoading || !user}
        >
          게시
        </SubmitButton>
      </CommentForm>
    </CommentInputContainer>
  );
};

// 스타일 컴포넌트
const CommentInputContainer = styled.div`
  width: 100%;
  margin-top: 1rem;
  padding: 1rem 0;
  border-top: 1px solid #333;
`;

const CommentForm = styled.form`
  display: flex;
  gap: 0.5rem;
  align-items: flex-start;
`;

const CommentTextarea = styled.textarea`
  flex: 1;
  min-height: 60px;
  background-color: ${(props) => props.theme.colors.gray};
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  padding: 0.75rem;
  font-size: ${(props) => props.theme.fontSizes.sm};
  color: ${(props) => props.theme.colors.background};
  resize: vertical;

  &::placeholder {
    color: ${(props) => props.theme.colors.darkGray};
  }

  &:disabled {
    opacity: 0.7;
  }
`;

const SubmitButton = styled.button`
  background-color: ${(props) => props.theme.colors.primary};
  color: ${(props) => props.theme.colors.text};
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  padding: 0.5rem 1rem;
  font-size: ${(props) => props.theme.fontSizes.sm};
  height: 40px;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

export default CommentInput;
