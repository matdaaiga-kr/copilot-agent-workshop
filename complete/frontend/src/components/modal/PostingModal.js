import React, { useState } from "react";
import styled from "styled-components";
import Modal from "./Modal";
import { postApi } from "../../api/apiService";
import { useAuth } from "../../context/AuthContext";

// 포스팅 모달 컴포넌트
const PostingModal = ({ isOpen, onClose, onPostCreated }) => {
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const { user } = useAuth();

  // 내용 입력 처리
  const handleContentChange = (e) => {
    setContent(e.target.value);
    if (error) setError("");
  };

  // 포스트 생성 처리
  const handleSubmit = async () => {
    if (!content.trim()) {
      setError("내용을 입력해주세요.");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const response = await postApi.createPost(content, user.username);
      setContent("");
      onClose();
      if (onPostCreated) {
        onPostCreated(response.data);
      }
    } catch (error) {
      console.error("포스트 생성 중 오류 발생:", error);
      setError("포스트 생성 중 오류가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setIsLoading(false);
    }
  };

  // 모달 닫기 처리
  const handleCancel = () => {
    if (
      content.trim() &&
      !window.confirm("작성 중인 내용이 있습니다. 정말 취소하시겠습니까?")
    ) {
      return;
    }
    setContent("");
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={handleCancel}>
      <TextareaContainer>
        <Textarea
          value={content}
          onChange={handleContentChange}
          placeholder="내용을 입력하세요."
          disabled={isLoading}
          autoFocus
        />
      </TextareaContainer>

      {error && <ErrorMessage>{error}</ErrorMessage>}

      <ButtonContainer>
        <Button
          $primary
          onClick={handleSubmit}
          disabled={isLoading || !content.trim()}
        >
          {isLoading ? "처리 중..." : "완료"}
        </Button>
        <Button onClick={handleCancel} disabled={isLoading}>
          취소
        </Button>
      </ButtonContainer>
    </Modal>
  );
};

// 스타일 컴포넌트
const TextareaContainer = styled.div`
  width: 100%;
  margin-bottom: 1rem;
`;

const Textarea = styled.textarea`
  width: 100%;
  min-height: 150px;
  background-color: ${(props) => props.theme.colors.gray};
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  padding: 1rem;
  font-size: ${(props) => props.theme.fontSizes.md};
  color: ${(props) => props.theme.colors.background};
  resize: vertical;

  &::placeholder {
    color: ${(props) => props.theme.colors.inputText};
  }

  &:disabled {
    opacity: 0.7;
  }
`;

const ErrorMessage = styled.p`
  color: red;
  font-size: ${(props) => props.theme.fontSizes.sm};
  margin-bottom: 1rem;
`;

const ButtonContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 1rem;
`;

const Button = styled.button`
  background-color: ${(props) =>
    props.$primary ? props.theme.colors.primary : props.theme.colors.secondary};
  color: ${(props) =>
    props.$primary ? props.theme.colors.text : props.theme.colors.background};
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  padding: 0.75rem 2rem;
  font-size: ${(props) => props.theme.fontSizes.sm};
  transition: opacity 0.3s;

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
`;

export default PostingModal;
