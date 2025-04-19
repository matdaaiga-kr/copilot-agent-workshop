import React, { useState } from "react";
import styled from "styled-components";
import Modal from "./Modal";
import { useAuth } from "../../context/AuthContext";

// 이름 입력 모달 컴포넌트
const NameInputModal = ({ isOpen, onClose }) => {
  const [username, setUsername] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const { login } = useAuth();

  // 이름 입력 처리
  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
    if (error) setError("");
  };

  // 로그인 처리
  const handleSubmit = async () => {
    if (!username.trim()) {
      setError("이름을 입력해주세요.");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      await login(username);
      // 로그인 성공 후 바로 모달 닫기
      setUsername("");
      onClose();
    } catch (error) {
      console.error("로그인 중 오류 발생:", error);
      setError("로그인 처리 중 오류가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setIsLoading(false);
    }
  };

  // Enter 키로 로그인 처리
  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !isLoading && username.trim()) {
      handleSubmit();
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalTitle>이름을 입력해주세요</ModalTitle>

      <InputContainer>
        <Input
          type="text"
          value={username}
          onChange={handleUsernameChange}
          onKeyPress={handleKeyPress}
          placeholder="이름"
          disabled={isLoading}
          autoFocus
        />
      </InputContainer>

      {error && <ErrorMessage>{error}</ErrorMessage>}

      <ButtonContainer>
        <SubmitButton
          onClick={handleSubmit}
          disabled={isLoading || !username.trim()}
        >
          {isLoading ? "처리 중..." : "완료"}
        </SubmitButton>
      </ButtonContainer>
    </Modal>
  );
};

// 스타일 컴포넌트
const ModalTitle = styled.h2`
  font-size: ${(props) => props.theme.fontSizes.xl};
  font-weight: ${(props) => props.theme.fontWeights.normal};
  color: ${(props) => props.theme.colors.text};
  margin-bottom: 1.5rem;
  text-align: center;
`;

const InputContainer = styled.div`
  width: 100%;
  margin-bottom: 1rem;
`;

const Input = styled.input`
  width: 100%;
  background-color: ${(props) => props.theme.colors.gray};
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  padding: 1rem;
  font-size: ${(props) => props.theme.fontSizes.md};
  color: ${(props) => props.theme.colors.background};

  &::placeholder {
    color: ${(props) => props.theme.colors.darkGray};
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
`;

const SubmitButton = styled.button`
  background-color: ${(props) => props.theme.colors.primary};
  color: ${(props) => props.theme.colors.text};
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  padding: 0.75rem 2rem;
  font-size: ${(props) => props.theme.fontSizes.sm};
  transition: opacity 0.3s;

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
`;

export default NameInputModal;
