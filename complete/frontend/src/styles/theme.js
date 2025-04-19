// 애플리케이션 전체에서 사용할 테마 색상 및 크기 정의
const theme = {
  colors: {
    primary: "#00B7FF", // 파란색 (버튼, 하이라이트 등)
    secondary: "#CCF1FF", // 연한 파란색
    background: "#000000", // 배경색 (검정)
    text: "#FFFFFF", // 텍스트 색상 (흰색)
    gray: "#D9D9D9", // 회색
    darkGray: "#878787", // 어두운 회색
    inputText: "#606060", // 입력 텍스트 색상
    heart: "#FF0000", // 하트 색상 (빨간색)
  },
  sizes: {
    navWidth: "110px", // 네비게이션 바 너비
    maxContentWidth: "700px", // 콘텐츠 최대 너비
    borderRadius: {
      sm: "10px", // 작은 모서리 둥글기
      md: "20px", // 중간 모서리 둥글기
    },
  },
  fontSizes: {
    xs: "16px",
    sm: "20px",
    md: "24px",
    lg: "32px",
    xl: "36px",
  },
  fontWeights: {
    normal: 400,
    bold: 700,
  },
};

export default theme;
