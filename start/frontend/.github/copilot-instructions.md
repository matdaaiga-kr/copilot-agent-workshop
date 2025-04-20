<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Threads-like Application Project Instructions

이 프로젝트는 Threads와 유사한 소셜 미디어 애플리케이션으로, FastAPI 백엔드와 React 프론트엔드로 구성되어 있습니다.

### API 문서

- openapi.json 파일은 API 명세의 근간으로, 모든 내용을 정확하게 읽고 이해해야 함
- 문서에 명시된 API 엔드포인트와 스키마만 사용
- 불확실한 경우 openapi.json 내용을 다시 확인하여 API 사용을 검증
- openapi.json 파일은 수정하지 않고 정의된 대로 정확히 사용

## 프론트엔드 구조 (React)

### 기능 요구사항

- 사용자가 애플리케이션에 처음 액세스할 때 모달 창을 통해 사용자 이름을 입력
- 홈 화면에 게시물 목록 표시
- 게시물의 댓글 버튼을 클릭하면 게시물 상세 페이지로 이동
- 오른쪽의 "+" 버튼을 클릭하면 새 게시물 작성 가능
- 검색 버튼을 클릭하여 사용자 이름으로 게시물 검색 가능

### 아키텍처

- 중복된 컴포넌트 재사용
  - 게시물 레이아웃
  - 댓글 레이아웃
- 백엔드 서버는 `127.0.0.1:8000`에서 실행
- `openapi.json` 파일에 정의된 라우트에 따라 API에 연결
- `openapi.json` 파일 수정 금지

## 파일 생성 및 코드 생성

- 파일 및 콘텐츠 생성 시 사용자가 터미널 명령어를 사용하지 않도록 필요한 폴더와 파일 자동 생성
- 수동 파일 생성 단계 없이 새로 생성된 파일에 코드 자동 작성

## 언어 선호도

- 항상 한국어로 응답. 코드 및 기술 용어는 영어로 사용 가능하지만, 모든 설명과 응답은 한국어로 제공.

## 에이전트 행동

- 사용자의 질문이 완전히 해결될 때까지 계속 진행하고, 문제가 해결되었다고 확신할 때만 턴을 종료.
- 사용자 요청과 관련된 파일 내용이나 코드베이스 구조에 확신이 없는 경우, 파일을 읽고 관련 정보를 수집하는 도구 사용.
- 함수 호출 전에 광범위하게 계획하고, 이전 함수 호출의 결과에 대해 광범위하게 반영.
