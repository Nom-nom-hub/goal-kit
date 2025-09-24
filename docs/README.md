# Goal-Driven Development Kit Documentation

This directory contains the documentation for the Goal-Driven Development Kit.

## Documentation Structure

- **[Home](index.md)** - Overview of Goal-Driven Development methodology and core concepts
- **[Installation Guide](installation.md)** - How to install and set up the Goal CLI
- **[Quick Start Guide](quickstart.md)** - Fast track to building with goal-driven development
- **[Local Development](local-development.md)** - Contributing and developing the toolkit locally

## Building Documentation

This documentation is built using [DocFX](https://dotnet.github.io/docfx/) and can be deployed to GitHub Pages.

### Prerequisites

- [.NET SDK](https://dotnet.microsoft.com/download) (version 8.x)
- [DocFX Tool](https://www.nuget.org/packages/docfx.console)

### Building Locally

```bash
# Install DocFX
dotnet tool install -g docfx

# Build documentation
cd docs
docfx docfx.json

# Preview locally (optional)
docfx serve _site
```

### GitHub Pages Deployment

Documentation is automatically built and deployed to GitHub Pages when changes are pushed to the `main` branch in the `docs/` directory.

## Contributing to Documentation

1. Edit the Markdown files in this directory
2. Update `toc.yml` if adding new sections
3. Test the build locally with `docfx` before pushing
4. Ensure all links work and formatting is correct

## Documentation Guidelines

- Use clear, concise language
- Include practical examples
- Provide step-by-step instructions
- Link to related sections where appropriate
- Test all code examples and commands