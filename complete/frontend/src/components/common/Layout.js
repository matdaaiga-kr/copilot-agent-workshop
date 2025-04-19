import React from "react";
import styled from "styled-components";
import NavBar from "./NavBar";

// 레이아웃 컴포넌트
const Layout = ({ children }) => {
  return (
    <LayoutContainer>
      <NavBar />
      <Main>{children}</Main>
    </LayoutContainer>
  );
};

// 스타일 컴포넌트
const LayoutContainer = styled.div`
  display: flex;
  min-height: 100vh;
`;

const Main = styled.main`
  flex: 1;
  margin-left: ${(props) => props.theme.sizes.navWidth};
  width: calc(100% - ${(props) => props.theme.sizes.navWidth});
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

export default Layout;
