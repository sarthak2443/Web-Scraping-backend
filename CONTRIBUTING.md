# Contributing to Stock Market Sentiment Analysis Pipeline

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the codebase.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs or request features
- Include detailed information about your environment and steps to reproduce
- Search existing issues before creating new ones

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-sentiment-analysis.git
   cd stock-sentiment-analysis
   ```

2. **Set up development environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # OR
   .\.venv\Scripts\Activate.ps1  # Windows PowerShell
   
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

3. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Add docstrings and type hints
   - Include appropriate error handling

3. **Test your changes**
   ```bash
   python -m src.orchestrator  # Test pipeline
   python analyze_output.py    # Test analysis
   ```

4. **Run code quality checks**
   ```bash
   black src/                  # Format code
   flake8 src/                # Lint code
   mypy src/                  # Type checking
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

6. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Code Style Guidelines

### Python Code Style
- Follow PEP 8 style guidelines
- Use Black for code formatting (line length: 88 characters)
- Include type hints for function parameters and return values
- Write comprehensive docstrings for all functions and classes

### Example Function Structure
```python
def process_tweets(tweets: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Process raw tweet data into a standardized DataFrame.
    
    Args:
        tweets: List of tweet dictionaries from scraper
        
    Returns:
        Processed DataFrame with cleaned tweet data
        
    Raises:
        ValueError: If tweets list is empty or malformed
    """
    # Implementation here
    pass
```

### Documentation
- Update README.md for user-facing changes
- Update technical documentation in docs/
- Include inline comments for complex logic
- Add examples for new features

## 🧪 Testing Guidelines

### Test Coverage
- Write tests for new functionality
- Maintain existing test coverage
- Include edge cases and error conditions

### Test Types
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete pipeline workflows

### Running Tests
```bash
pytest tests/                    # Run all tests
pytest tests/test_scraper.py     # Run specific test file
pytest --cov=src tests/          # Run with coverage report
```

## 📊 Performance Guidelines

### Optimization Principles
- Prioritize code readability over micro-optimizations
- Profile before optimizing
- Use appropriate data structures for the task
- Implement caching for expensive operations

### Memory Management
- Use generators for large datasets
- Clean up browser resources in scrapers
- Avoid loading entire datasets into memory when possible

## 🔒 Security Guidelines

### Data Handling
- Never commit sensitive data or credentials
- Sanitize all external inputs
- Follow responsible disclosure for security issues

### Dependencies
- Keep dependencies up to date
- Use virtual environments
- Scan for vulnerabilities regularly

## 🚀 Release Process

### Version Numbering
We use Semantic Versioning (SemVer):
- MAJOR.MINOR.PATCH (e.g., 1.2.3)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist
- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Test all functionality
- [ ] Update documentation
- [ ] Create release notes

## 🏷️ Commit Message Format

Use conventional commits format:
```
type(scope): description

[optional body]

[optional footer]
```

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(scraper): add support for Reddit data source
fix(analysis): handle empty datasets gracefully
docs(readme): update installation instructions
```

## 🌟 Recognition

Contributors will be recognized in:
- Project README.md
- Release notes
- Hall of Fame section (for significant contributions)

## ❓ Questions?

- Open a GitHub issue for technical questions
- Join our Discord community for real-time discussions
- Email the maintainers for private inquiries

Thank you for contributing! 🎉
