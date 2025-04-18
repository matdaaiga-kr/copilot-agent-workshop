<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a FastAPI backend project for a Threads-like application. Please ensure that generated code aligns with the following features:

<!-- Architecture and Database -->

- Follow MVC (Model-View-Controller) pattern:
  - Models: Define data structures and database interactions
  - Controllers: Implement business logic in service layers
  - Views: Handle through FastAPI route handlers and responses
- Use SQLite as the database
- Organize code with clear separation of concerns

<!-- Environment Variables -->

- Use environment variables for configuration (database connection, API keys, secrets)
- Store sensitive information using the .env file pattern
- Never commit sensitive credentials to version control
- Load environment variables using python-dotenv

<!-- File Creation and Code Generation -->

- When creating files and adding content, automatically generate the necessary folders and files without asking the user to use terminal commands
- Automatically write code in newly created files without requiring manual file creation steps

<!-- Project Documentation -->

- Document the application execution process in the `README.md` file

<!-- Language Preference -->

Please always respond in Korean. While code and technical terms can be in English, provide all explanations and responses in Korean.
