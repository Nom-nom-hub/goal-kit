# Goal-Dev-Spec Troubleshooting Guide and FAQ

This document provides solutions to common issues and answers to frequently asked questions about using the Goal-Dev-Spec tool.

## Troubleshooting Common Issues

### Installation and Setup Issues

#### Issue: Command not found after installation
**Symptoms:** Running `goal` command results in "command not found"
**Solutions:**
1. Verify installation: `pip install -e .`
2. Check if the installation directory is in your PATH:
   ```bash
   # Check Python scripts directory
   python -m site --user-base
   # Add to PATH if needed
   export PATH="$PATH:$(python -m site --user-script-dir)"
   ```
3. Try running with full path: `python -m goal_cli`

#### Issue: Permission errors during installation
**Symptoms:** Permission denied during pip install
**Solutions:**
1. Use user installation: `pip install --user -e .`
2. Use virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

#### Issue: Git not found during initialization
**Symptoms:** "git not found" error during project initialization
**Solutions:**
1. Install Git from https://git-scm.com/
2. Use the `--no-git` option: `goal init my-project --no-git`
3. Add Git to your PATH if already installed

### Project Initialization Issues

#### Issue: Directory conflict during initialization
**Symptoms:** "Directory already exists" error
**Solutions:**
1. Use different project name: `goal init my-project-2`
2. Initialize in current directory: `goal init --here`
3. Use force option if intentional: `goal init my-project --force`

#### Issue: AI agent not found during initialization
**Symptoms:** "AI agent not found" error when selecting Claude, Gemini, etc.
**Solutions:**
1. Install the required AI tool (Claude CLI, Gemini CLI, etc.)
2. Skip AI selection during initialization and configure later
3. Choose "None" or "Manual" option if AI tools aren't needed

### CLI Command Issues

#### Issue: "Not in a goal-dev-spec project directory"
**Symptoms:** Error when running goal commands in a directory
**Solutions:**
1. Verify you're in a Goal-Dev-Spec project directory
2. Check for `.goal/` directory: `ls -la`
3. Initialize a project if needed: `goal init`

#### Issue: Goal ID not found
**Symptoms:** Commands like `goal show <goal-id>` fail
**Solutions:**
1. List available goals: `goal list`
2. Verify the goal ID is correct
3. Check that it's not a plan, spec, or task ID

### Template and Configuration Issues

#### Issue: Missing template files
**Symptoms:** Template-related errors during goal creation
**Solutions:**
1. Verify complete installation with all template files
2. Check that `.goal/templates/` directory exists and is populated
3. Reinstall the package if templates are missing

#### Issue: Configuration file errors
**Symptoms:** YAML parsing errors in configuration files
**Solutions:**
1. Validate YAML syntax using an online YAML validator
2. Check for proper indentation and quotes
3. Ensure no tabs are mixed with spaces

### AI Agent Integration Issues

#### Issue: API key configuration
**Symptoms:** AI commands fail due to authentication
**Solutions:**
1. Verify API keys are set as environment variables
2. Check agent configuration in `.goal/agents/<agent>/config.yaml`
3. Ensure API key hasn't expired or been revoked

#### Issue: AI response quality
**Symptoms:** Generated content is not meeting expectations
**Solutions:**
1. Review and customize prompt templates
2. Try different AI agents for comparison
3. Provide more detailed specifications

### Governance and Quality Issues

#### Issue: Governance validation failures
**Symptoms:** `goal governance validate` reports failures
**Solutions:**
1. Check that artifacts meet required standards
2. Review governance policies in `.goal/governance/policies/`
3. Update artifacts to comply with required standards

#### Issue: Quality gate failures
**Symptoms:** `goal quality run-checks` shows failures
**Solutions:**
1. Address issues reported in quality checks
2. Update code/documentation to meet quality thresholds
3. Adjust quality thresholds if appropriate: `goal quality set-thresholds`

### Performance and Monitoring Issues

#### Issue: Dashboard not accessible
**Symptoms:** Cannot access live dashboard
**Solutions:**
1. Check if port is available: `goal monitor live-dashboard --port 8081`
2. Ensure firewall allows connections on the dashboard port
3. Verify network access if running on a remote server

#### Issue: Performance analysis taking too long
**Symptoms:** `goal perf analyze` command is slow
**Solutions:**
1. Use shallow analysis: `goal perf analyze --depth shallow`
2. Analyze specific components: `goal perf analyze --target database`
3. Check system resource availability (CPU, memory)

## Frequently Asked Questions (FAQ)

### General Questions

#### Q: What is Goal-Dev-Spec?
A: Goal-Dev-Spec is a goal-driven development specification system that uses YAML files to structure goals, specifications, plans, and tasks. It provides a systematic approach to defining goals, creating specifications, planning implementations, and tracking progress.

#### Q: How is Goal-Dev-Spec different from other project management tools?
A: Goal-Dev-Spec focuses specifically on goal-driven development with a strong emphasis on specifications and structured planning. It integrates AI assistants, governance, analytics, quality assurance, and cross-platform scripting in a single tool.

#### Q: Can I use Goal-Dev-Spec for any type of project?
A: Yes, Goal-Dev-Spec is designed to be flexible and can be used for software projects, data science projects, web applications, mobile apps, and other technical projects that can benefit from structured goal management.

#### Q: Is there a cloud version of Goal-Dev-Spec?
A: Currently, Goal-Dev-Spec is a command-line tool that runs locally. All data is stored in your project directories. There are no plans for a cloud version, ensuring your project data remains under your control.

### Setup and Configuration Questions

#### Q: Do I need to install AI tools to use Goal-Dev-Spec?
A: No, AI tools are optional. You can use Goal-Dev-Spec without any AI integrations. During project initialization, you can choose not to integrate with AI tools.

#### Q: How do I customize the default templates?
A: Templates are stored in the `.goal/templates/` directory of your project. You can modify the YAML and Markdown templates to match your organization's standards and processes.

#### Q: Can I use Goal-Dev-Spec with existing projects?
A: Yes, you can initialize Goal-Dev-Spec in existing projects using `goal init --here`. This will add the Goal-Dev-Spec structure to your existing project.

### Goal and Specification Questions

#### Q: What's the difference between a goal and a specification?
A: A goal represents a high-level objective with objectives and success criteria. A specification details the requirements for implementing a goal, including user stories, acceptance criteria, and functional requirements.

#### Q: How do I create dependencies between goals?
A: You can specify dependencies in the `dependencies` array of a goal's YAML file or through the UI during goal creation.

#### Q: How detailed should my goals be?
A: Goals should be specific, measurable, achievable, relevant, and time-bound (SMART). They should be granular enough to be manageable but high-level enough to represent meaningful objectives.

### Integration Questions

#### Q: Which AI agents are supported?
A: Goal-Dev-Spec supports Claude Code, Gemini CLI, GitHub Copilot, Cursor, Qwen Code, opencode, Codex CLI, Windsurf, Kilo Code, and Auggie CLI. You can select your preferred agent during project initialization.

#### Q: Can I integrate with my CI/CD pipeline?
A: Yes, Goal-Dev-Spec provides CI/CD integration features. You can set up pipelines using `goal cicd setup-pipeline` and integrate with GitHub Actions, GitLab CI, Jenkins, and other CI/CD tools.

#### Q: Is there a way to export project data?
A: Project data is stored in standard YAML and Markdown files, which can be easily exported, parsed, or integrated with other tools. You can also generate reports using the various reporting commands.

### Advanced Questions

#### Q: Can I extend Goal-Dev-Spec with custom functionality?
A: Yes, Goal-Dev-Spec has an API that allows developers to create custom commands and integrations. Refer to the API documentation for detailed information on extending the tool.

#### Q: How does the predictive analytics work?
A: The analytics engine uses historical project data, goal complexity analysis, and patterns to predict completion times, identify risks, and recommend resources. It learns from your past projects to improve predictions.

#### Q: What security measures are in place?
A: Goal-Dev-Spec includes security scanning capabilities, governance controls, and follows security best practices. However, security ultimately depends on your implementation and configuration.

#### Q: How do I handle team collaboration with Goal-Dev-Spec?
A: Since all data is stored in YAML files, you can use Git for version control and collaboration. Teams can work on different goals and merge changes. The governance features help ensure consistency across team members.

### Performance Questions

#### Q: How does Goal-Dev-Spec handle large projects?
A: Goal-Dev-Spec is designed to scale with project size by organizing artifacts in a structured directory system. Performance depends on your file system and hardware. For extremely large projects, consider breaking them into multiple Goal-Dev-Spec projects.

#### Q: Are there any performance considerations for using AI integration?
A: AI integration requires API calls, which may take time and incur costs. Plan your usage accordingly. You can also use Goal-Dev-Spec without AI integration for faster operations.

### Troubleshooting Questions

#### Q: How do I back up my Goal-Dev-Spec projects?
A: Since all project data is stored in the `.goal/` directory and other project files, backing up your project directory effectively backs up your Goal-Dev-Spec data. You can use standard backup tools or version control systems.

#### Q: What should I do if I accidentally delete a goal?
A: If you're using Git, you can restore deleted goals from previous commits. Otherwise, you may need to recreate the goal. This highlights the importance of using version control with your Goal-Dev-Spec projects.

#### Q: How do I reset a project to a previous state?
A: If using Git, use `git checkout` to revert to a previous commit. You can also manually modify the YAML files in the `.goal/` directory, but be careful to maintain proper structure.

### Support Questions

#### Q: Where can I get help if I encounter issues not covered here?
A: You can:
1. Check the detailed documentation in the `docs/` directory
2. Review the configuration files in your project's `.goal/` directory
3. Consult the API documentation for development-related questions
4. File an issue in the project's issue tracker if you believe you've found a bug

## Best Practices for Avoiding Issues

### 1. Project Setup
- Always initialize projects in dedicated directories
- Use meaningful project names
- Set up version control early
- Configure your preferred AI agent during initialization if you plan to use it

### 2. Goal Creation
- Be specific and detailed when creating goals
- Define clear success criteria
- Establish realistic dependencies
- Regularly review and update goal statuses

### 3. Quality Assurance
- Set appropriate quality thresholds early
- Regularly run quality checks
- Address issues promptly
- Maintain good documentation practices

### 4. Maintenance
- Regularly update the tool to get new features and fixes
- Back up project data regularly
- Review and update templates as needed
- Monitor performance metrics

## Getting Additional Help

If you encounter issues not covered in this guide:

1. **Check the Documentation**: The `docs/` directory contains comprehensive guides
2. **Review Configuration**: Check files in the `.goal/` directory for configuration issues
3. **Use Help Commands**: Run `goal --help` or `goal <command> --help` for detailed information
4. **Community Support**: Check the project repository for community support options

Remember that most Goal-Dev-Spec data is stored in readable YAML and Markdown files, so you can always inspect and modify them directly if needed, though using the CLI commands is recommended for consistency and validation.