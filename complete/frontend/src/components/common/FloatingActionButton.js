import React from "react";
import styled from "styled-components";

// 플러스 아이콘 컴포넌트
const PlusIcon = () => (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor" />
  </svg>
);

// 플로팅 액션 버튼 컴포넌트
const FloatingActionButton = ({ onClick }) => {
  return (
    <FABContainer onClick={onClick}>
      <PlusIcon />
    </FABContainer>
  );
};

// 스타일 컴포넌트
const FABContainer = styled.button`
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: ${(props) => props.theme.colors.primary};
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  z-index: 100;
  transition: transform 0.3s, background-color 0.3s;

  &:hover {
    transform: scale(1.05);
    background-color: ${(props) => props.theme.colors.primary}e0;
  }

  &:active {
    transform: scale(0.95);
  }
`;

export default FloatingActionButton;
