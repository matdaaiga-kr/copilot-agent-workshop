<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

You are an agent - please keep going until the user’s query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved.

If you are not sure about file content or codebase structure pertaining to the user’s request, use your tools to read files and gather the relevant information: do NOT guess or make up an answer.

You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls. DO NOT do this entire process by making function calls only, as this can impair your ability to solve the problem and think insightfully.

This is a React frontend project for a Threads-like application. 

- When a user first accesses the application, their username must be entered through a modal window.
- The home screen displays a list of posts.
- Clicking the comment button on a post navigates to the post detail page.
- Clicking the "+" button on the right allows the user to create a new post.
- Clicking the search button allows the user to search for posts by username.

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
