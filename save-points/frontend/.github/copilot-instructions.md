<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a React frontend project for a Threads-like application. Please ensure that generated code aligns with the following features:

- Authentication (Signup, Login)
  - Use JWT token based authentication
- Posts (Create, View, Like, Comment)
- Profile (View Profile, My Posts, Followers, Following)

<!-- Architecture -->

- Reuse duplicated components.
  - Post layout
  - Comment layout
- The backend server is running at `127.0.0.1:8000`.
- Connect to the APIs according to the routes defined in the `openapi.json` file.

<!-- Project Documentation -->

- Do not modify `openapi.json` file

<!-- Language Preference -->

Please always respond in Korean. While code and technical terms can be in English, provide all explanations and responses in Korean.
