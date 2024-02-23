# Contributing

First off, thank you for considering contributing to RandSN! It's people like you that make RandSN such a great tool.

## Getting Started

Before you begin:
- Ensure you have a [GitHub account](https://github.com/signup/free).
- Submit an issue for your work, unless there is already one.
- Fork the repository on GitHub.

## Making Changes

Here's a quick guide on how to make effective contributions to the project:

1. **Create a topic branch** from where you want to base your work.
   - This is usually the `main` branch.
   - Only target release branches if you are certain your fix must be on that branch.
   - To quickly create a topic branch: `git checkout -b fix/issue_##`.
2. **Make commits** of logical units.
3. **Check for unnecessary whitespace** with `git diff --check` before committing.
4. **Ensure your commit messages are clear** and follow the conventional commit messages format (e.g., `feat: add new feature for...`).
5. **Make sure you have added the necessary tests** for your changes.
6. **Run all the tests** to assure nothing else was accidentally broken.

### Making Trivial Changes

For small changes such as typos, minimal code changes, or documentation improvements, it's not always necessary to create a new issue. In such cases, feel free to make a pull request directly.

## Submitting Changes

1. **Push your changes** to a topic branch in your fork of the repository.
2. **Submit a pull request** to the RandSN repository in the GitHub UI.
   - In the pull request, describe what your changes do and mention any bugs/issues related to the pull request.
3. **Update the issue** to mark that you have submitted code and are ready for it to be reviewed (mentioning the pull request in the issue with `#PR`).

## Additional Resources

- [General GitHub documentation](https://help.github.com/)
- [GitHub pull request documentation](https://help.github.com/articles/about-pull-requests/)

## Communication

- If you have a large change in mind, please open an issue to discuss before making significant effort. This will allow community feedback and guidance.
- Use issues for any questions so the community can benefit from the discussion.

## Code Contributions

- **Unit Tests**: We highly appreciate pull requests that come with full unit test coverage.
- **Code Formatting**: Please use [black formatting](https://github.com/psf/black) to ensure consistency across the codebase.
- **Documentation**: Update the `README.md` with any changes that are relevant to the project's usage or setup instructions.

## Testing

- Tests are located in the [tests](tests) folder. Please add unit tests for new code and ensure all tests pass before submitting a pull request.

Thank you for your contributions to RandSN!