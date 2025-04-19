import React from "react";
import { Link, useLocation } from "react-router-dom";
import styled from "styled-components";

// 아이콘 컴포넌트
const HomeIcon = () => (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M12 5.69L17 10.19V18H15V12H9V18H7V10.19L12 5.69ZM12 3L2 12H5V20H11V14H13V20H19V12H22L12 3Z"
      fill="currentColor"
    />
  </svg>
);

const PersonIcon = () => (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z"
      fill="currentColor"
    />
  </svg>
);

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

// 네비게이션바 컴포넌트
const NavBar = () => {
  const location = useLocation();

  return (
    <NavContainer>
      <NavItem to="/" active={location.pathname === "/" ? "true" : "false"}>
        <HomeIcon />
      </NavItem>
      <NavItem
        to="/search"
        active={location.pathname === "/search" ? "true" : "false"}
      >
        <SearchIcon />
      </NavItem>
      <NavItem
        to="/profile"
        active={location.pathname === "/profile" ? "true" : "false"}
      >
        <PersonIcon />
      </NavItem>
    </NavContainer>
  );
};

// 스타일 컴포넌트
const NavContainer = styled.nav`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: ${(props) => props.theme.sizes.navWidth};
  height: 100vh;
  background-color: ${(props) => props.theme.colors.background};
  position: fixed;
  top: 0;
  left: 0;
  gap: 2rem;
  padding: 1rem 0;
  border-right: 1px solid #333;
`;

const NavItem = styled(Link)`
  color: ${(props) =>
    props.active === "true"
      ? props.theme.colors.primary
      : props.theme.colors.text};
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  transition: all 0.3s;

  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
`;

export default NavBar;
