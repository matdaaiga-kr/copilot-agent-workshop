# 백엔드 API 개발

## 사전 준비 사항

이전 [STEP 01 : 프롬프트 입력을 위한 기본 설정](./step-01.md)에서 프롬프트 입력을 위한 파일들을 모두 복사한 상태라고 가정합니다.

## 리포지토리 루트 설정

1. 아래 명령어를 실행시켜 `$REPOSITORY_ROOT` 환경 변수를 설정합니다.

   ```bash
   # Bash/Zsh
   REPOSITORY_ROOT=$(git rev-parse --show-toplevel)
   ```

   ```powershell
   # PowerShell
   $REPOSITORY_ROOT = git rev-parse --show-toplevel
   ```

## 프로젝트 실행

1. 처음 [STEP 00 : 개발 환경 설정](./step-00.md) 단계에서 익스텐션을 정상적으로 설치했다면, 다음과 같은 아이콘을 확인할 수 있습니다.
   ![open-chat1](./img/step02-open-chat1.png)

   아이콘을 클릭해 chat 기능을 활성화하면, 다음과 같은 화면을 볼 수 있습니다.
   ![open-chat2](./img/step02-open-chat2.png)

   > 🥕 팁 : 만약 익스텐션을 설치했음에도 보이지 않는다면, `ctrl+alt+i` 키를 누르거나 `ctrl+cmd+i` 키를 눌러 chat을 엽니다.

2. 다음 과정들을 통해 `agent` 모드로 변경합니다.
   ![agent-mode-1](./img/step02-agent-mode1.png)
   ![agent-mode-2](./img/step02-agent-mode2.png)
3. 다음 과정들을 통해 AI 모델을 `Claude 3.7 Sonnet`으로 변경합니다.
   ![pick-model-1](./img/step02-pick-model1.png)
   ![pick-model-2](./img/step02-pick-model2.png)
4. 코파일럿이 현재 파일을 더 빠르게 인식할 수 있도록 `backend/api-document.yaml` 파일을 클릭해 열어줍니다.
   ![step02-fileopen](./img/step02-fileopen.png)
5. 이제 다음 내용을 프롬프트에 입력합니다.
   ```text
   "api-document.yaml` 파일에 명시된 paths, models를 토대로 FastAPI 백엔드 프로젝트를 생성해줘
   ```
6. 이제 프로젝트의 오류를 마주칠 때 해당 오류를 수정해달라는 내용을 프롬프트에 입력합니다.
   > 🥕 팁 : 바이브 코딩의 묘미는 "해줘"체를 사용하는 것입니다.

# 번외) 완성된 버전의 백엔드 프로젝트를 실행해보고 싶다면?

1. 아래 명령어를 터미널에 입력합니다.
   ```bash
   cd $REPOSITORY_ROOT/complete/backend
   ```
2. 아래 명령어를 터미널에 입력해 `.env` 파일을 생성합니다.

   ```bash
   touch .env
   ```

   ```powershell
   New-Item -Path .env -ItemType File
   ```

3. `.env` 파일을 열고 다음 내용을 입력합니다.
   ```text
   DATABASE_URL=sqlite:///./app.db
   SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   ```
4. [complete/backend/README.md](/complete/backend/README.md) 파일의 `실행 방법` 섹션에 따라 명령어를 입력해 프로젝트를 실행합니다.
