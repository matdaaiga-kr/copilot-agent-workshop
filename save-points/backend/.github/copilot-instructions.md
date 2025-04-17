<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a FastAPI backend project for a Threads-like application. Please ensure that generated code aligns with the following features:

- Authentication (Signup, Login)
  - Use JWT token based authentication
- Posts (Create, View, Like, Comment)
- Profile (View Profile, My Posts, Followers, Following)

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

<!-- Authentication Implementation -->

- Use HTTPBearer instead of OAuth2PasswordBearer for authentication to allow direct access token input in Swagger UI
- Set token expiration time to 1 day (24 hours or 1440 minutes)
- Implement exception handling for JWTError and other authentication-related exceptions
- Ensure proper token validation and user verification

<!-- Project Documentation -->

- Document the application execution process in the `README.md` file

<!-- Language Preference -->

Please always respond in Korean. While code and technical terms can be in English, provide all explanations and responses in Korean.
