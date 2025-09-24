# Contributing to Goal-Kit

Thank you for your interest in contributing to Goal-Kit! We welcome contributions from the community to help improve the Goal-Driven Development methodology and toolkit.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming environment for everyone.

## How to Contribute

There are many ways you can contribute to Goal-Kit:

- **Report bugs**: File issues for bugs you encounter
- **Suggest features**: Share ideas for new features or improvements
- **Fix bugs**: Submit pull requests to fix bugs
- **Improve documentation**: Enhance the documentation or add examples
- **Write tutorials**: Create guides and tutorials for using Goal-Kit
- **Support users**: Help answer questions in issues and community channels

## Getting Started

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Ensure all tests pass
5. Submit a pull request

## Development Workflow

### Setting up your environment

1. Clone your fork of the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/goal-kit.git
   cd goal-kit
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

### Making Changes

1. Create a new branch for your work:
   ```bash
   git checkout -b feature/my-feature-name
   ```

2. Make your changes and test them thoroughly

3. Add or update tests as necessary

4. Update documentation as needed

5. Commit your changes with a clear commit message:
   ```bash
   git add .
   git commit -m "Add feature: description of what you added"
   ```

6. Push your changes to your fork:
   ```bash
   git push origin feature/my-feature-name
   ```

### Pull Request Process

1. Ensure your PR description clearly describes the problem and solution
2. Include any relevant issue numbers
3. Add tests for new functionality
4. Update documentation as needed
5. Make sure all CI checks pass
6. Request a review from maintainers

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write clear, concise comments
- Keep functions and methods focused on a single responsibility

### Testing

- Write tests for all new functionality
- Ensure existing tests continue to pass
- Aim for high test coverage
- Test edge cases and error conditions

### Documentation

- Update documentation for any changes to the public API
- Write clear, helpful docstrings
- Add examples where appropriate
- Keep README and other documentation up to date

## Feature Requests

We welcome feature requests! When suggesting a new feature:

1. Check if the feature already exists or is being planned
2. Explain the problem the feature would solve
3. Describe your proposed solution
4. Consider the impact on the existing codebase

## Questions?

If you have questions about contributing, feel free to open an issue or reach out to the maintainers.

Thank you for contributing to Goal-Kit and helping to improve Goal-Driven Development!