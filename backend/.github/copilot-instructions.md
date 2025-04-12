<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a FastAPI backend project for a Threads-like application. Please ensure that generated code aligns with the following features:

- Authentication (Signup, Login)
- Posts (Create, View, Like, Comment)
- Profile (View Profile, My Posts, Followers, Following)

<!-- Architecture and Database -->

- Follow MVC (Model-View-Controller) pattern:
  - Models: Define data structures and database interactions
  - Controllers: Implement business logic in service layers
  - Views: Handle through FastAPI route handlers and responses
- Use SQLite as the database
- Organize code with clear separation of concerns

<!-- Language Preference -->

항상 한국어로 응답해주세요. 코드나 기술적인 용어는 영어로 작성하되, 설명과 답변은 한국어로 제공해주세요. Please always respond in Korean. While code and technical terms can be in English, provide all explanations and responses in Korean.
