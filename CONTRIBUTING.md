# Contributing to Nurse Eval AI

Thank you for considering contributing to the Nurse Evaluation AI system! This document provides guidelines for contributing to the project.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check the existing issues to avoid duplicates
2. Collect information about the bug
3. Include steps to reproduce

Bug reports should include:
- Clear and descriptive title
- Steps to reproduce the behavior
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment details (OS, browser, versions)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:
- Clear and descriptive title
- Detailed description of the proposed functionality
- Explanation of why this enhancement would be useful
- Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
6. Update documentation
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+ (if running locally)

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/lankamar/nurse-eval-ai.git
cd nurse-eval-ai

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup frontend
cd ../frontend
npm install

# Setup environment
cp .env.example .env
# Edit .env with your local configuration
```

### Running Locally

```bash
# Start all services with Docker
docker-compose up -d

# Or run individually:

# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm start
```

## Development Guidelines

### Python Code Style

We follow PEP 8 style guide with some modifications:
- Maximum line length: 127 characters
- Use type hints where possible
- Document functions with docstrings

```python
from typing import Optional

def calculate_score(responses: list, max_score: int = 5) -> float:
    """
    Calculate average score from responses.
    
    Args:
        responses: List of response objects
        max_score: Maximum possible score (default: 5)
    
    Returns:
        Average score as percentage
    """
    if not responses:
        return 0.0
    
    total = sum(r.score for r in responses)
    return (total / (len(responses) * max_score)) * 100
```

### JavaScript/React Code Style

- Use functional components with hooks
- Use meaningful variable names
- Add PropTypes or TypeScript types
- Keep components small and focused

```javascript
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const EvaluationCard = ({ evaluation, onUpdate }) => {
  const [loading, setLoading] = useState(false);
  
  // Component logic here
  
  return (
    <div className="card">
      {/* Component JSX */}
    </div>
  );
};

EvaluationCard.propTypes = {
  evaluation: PropTypes.object.isRequired,
  onUpdate: PropTypes.func,
};

export default EvaluationCard;
```

### Testing

#### Backend Tests

```bash
# Run all tests
cd backend
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_api.py

# Run specific test
pytest app/tests/test_api.py::test_login_user
```

Write tests for:
- All API endpoints
- Business logic in services
- Security functions
- Database operations

Example:
```python
def test_create_evaluation():
    """Test evaluation creation with proper permissions."""
    # Setup
    token = login_as_supervisora()
    
    # Execute
    response = client.post(
        "/api/evaluations/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "evaluated_id": 2,
            "period": "2024-Q1",
            "consent_given": True
        }
    )
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["period"] == "2024-Q1"
    assert data["status"] == "draft"
```

#### Frontend Tests

```bash
# Run tests
cd frontend
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

### Database Migrations

We use Alembic for database migrations:

```bash
# Create new migration
cd backend
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Documentation

- Update README.md for user-facing changes
- Update API_EXAMPLES.md for new endpoints
- Add docstrings to all functions
- Update COMPLIANCE.md for regulatory changes
- Include inline comments for complex logic

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(api): add endpoint for evaluation export

Add new endpoint to export evaluations as CSV.
Includes filtering by date range and status.

Closes #123
```

```
fix(auth): resolve 2FA token validation issue

Fixed issue where valid TOTP tokens were being rejected
due to timing window misconfiguration.

Fixes #456
```

## Project Structure

```
nurse-eval-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── db/           # Database setup
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── tests/        # Tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── contexts/     # React contexts
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── utils/        # Utility functions
│   ├── Dockerfile
│   └── package.json
├── docs/                 # Documentation
├── .github/
│   └── workflows/        # CI/CD pipelines
└── docker-compose.yml
```

## Review Process

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] Backward compatibility maintained
- [ ] Performance impact considered
- [ ] Error handling is appropriate
- [ ] Logging is adequate

### Approval Requirements

- At least one approval from maintainers
- All CI checks passing
- No merge conflicts
- Documentation complete

## Security

### Reporting Security Issues

**DO NOT** open a public issue for security vulnerabilities.

Instead, email security@hospital.clinicas.uba.ar with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Security Best Practices

- Never commit secrets or credentials
- Use environment variables for configuration
- Validate all user inputs
- Sanitize data before database operations
- Use parameterized queries
- Keep dependencies updated
- Follow OWASP guidelines

## Getting Help

- 📖 Read the [documentation](README.md)
- 💬 Ask questions in GitHub Discussions
- 🐛 Report bugs via GitHub Issues
- 📧 Email: dev@hospital.clinicas.uba.ar

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to Nurse Eval AI! 🎉
