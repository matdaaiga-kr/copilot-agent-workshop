# 도커로 어디서나 실행 가능한 워크샵 환경 만들기

## 사전 준비 사항

이전 [STEP 01 : 프롬프트 입력을 위한 기본 설정](./step-01.md)에서 프론트엔드 앱 개발용 소스코드 파일들을 모두 생성한 상태라고 가정합니다. 만약 STEP 1에서 완성한 프로그램을 실행 중이라면 종료해주세요.

> 🥕 팁 : 만약 오류를 해결하지 못했다면, `complete/frontend` 폴더를 복사해서 사용합니다.

## 도커 컨테이너 실행

1. Visual Studio Code에서 **새 터미널**을 열고, 아래 명령어를 입력해 `$REPOSITORY_ROOT` 환경 변수를 설정합니다.

   > ⚠️ 주의 : 자신이 사용 중인 터미널 종류에 따라 다음 두 명령어 중 하나를 입력합니다.

   ```bash
   # Bash/Zsh
   REPOSITORY_ROOT=$(git rev-parse --show-toplevel)
   ```

   ```powershell
   # PowerShell
   $REPOSITORY_ROOT = git rev-parse --show-toplevel
   ```

1. 이어서 `$REPOSITORY_ROOT`로 이동합니다. 
   ```bash
   cd $REPOSITORY_ROOT
   ```

1. 아래 명령어로 도커 파일을 실행합니다. 
   ```bash
   docker compose up
   ```

1. `http://localhost:80`으로 접속하여 앱을 실행시킵니다.

---

축하합니다!! `도커로 어디서나 실행 가능한 워크샵 환경 만들기`이 끝났습니다!! 바이브 코딩을 이용한 여러분만의 애플리케이션 개발에 도전해보세요!!
