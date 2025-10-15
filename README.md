# PetStore API Tests

## Project Description

This repository contains a comprehensive set of **automated API tests** for the PetStore service REST API. 
The tests are implemented in **Python 3.9** using **pytest** framework and integrated with **Allure** for detailed test reporting. 
The project supports both local execution and **CI/CD via GitHub Actions** with automatic report deployment.

## Goal and Objectives

The primary goal is to ensure the stability, reliability, and correctness of the PetStore REST API.

**Main objectives:**
- Comprehensive testing of CRUD operations for `pet` and `store` resources
- Validation of both positive and negative test scenarios
- Automated generation of structured test reports for result analysis
- Support for local test execution and continuous integration
- Historical tracking of test results through Allure trends

**This project does not include:**
- UI testing
- Load testing
- Mobile application testing

## Technologies Used

- **Python 3.9** - Core programming language
- **Pytest** - Test framework and runner
- **Requests** - HTTP library for API calls
- **Faker** - Test data generation
- **Allure Framework** - Test reporting and visualization
- **GitHub Actions** - CI/CD automation
- **Docker** - Environment containerization
- **Yamllint** - YAML syntax validation
- **Act** - Local GitHub Actions testing

## 📋 Installation and Local Setup

### Prerequisites
- Python 3.9+
- Git
- Java Runtime Environment (for Allure reports)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KovalIllia/petstore-api-tests.git
   cd petstore-api-tests
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python3 -m venv .venv2
   
   # Activate virtual environment
   source .venv2/bin/activate
   
   # On Windows use:
   # .venv2\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Allure (for report generation)**
   ```bash
   # Install Java
   sudo apt-get update
   sudo apt-get install -y default-jre
   
   # Download and install Allure
   wget https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz
   sudo tar -xzf allure-2.27.0.tgz -C /opt/
   sudo ln -sf /opt/allure-2.27.0/bin/allure /usr/bin/allure
   ```

## 🔍 Syntax Validation and Pre-commit Checks

### YAML Syntax Validation

Before committing changes to the GitHub Actions workflow, always validate the YAML syntax:

```bash
# Install yamllint
pip install yamllint

# Validate workflow file syntax
yamllint .github/workflows/pytest.yml

# Validate all YAML files in project
yamllint .
```

**Expected Output:** No errors (warnings about truthy values can be ignored for GitHub Actions syntax)

### Local GitHub Actions Testing with Act

Test your GitHub Actions workflows locally before pushing:

1. **Install Act**
   ```bash
   # On macOS (using Homebrew)
   brew install act
   
   # On Linux (using curl)
   curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
   
   # On Windows (using Chocolatey)
   choco install act
   ```

2. **Test workflow locally**
   ```bash
   # List available workflows
   act -l
   
   # Dry run to see what would be executed
   act -n
   
   # Run specific workflow locally
   act -j test
   
   # Run with specific event
   act push -W .github/workflows/pytest.yml
   ```

3. **Using specific Python version**
   ```bash
   # Run with custom image and bind mount
   act -P ubuntu-latest=node:12-buster-slim -j test
   ```

### Pre-push Validation Script

Create a pre-push validation script (optional):

```bash
#!/bin/bash
# pre-push-check.sh

echo "Running pre-push validation..."

# Check YAML syntax
echo "🔍 Validating YAML syntax..."
yamllint .github/workflows/pytest.yml
YAML_EXIT_CODE=$?

# Run tests locally
echo "🧪 Running local tests..."
source .venv2/bin/activate
pytest --alluredir=allure-results -v
TEST_EXIT_CODE=$?

# Summary
if [ $YAML_EXIT_CODE -eq 0 ] && [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All checks passed! Ready to push."
    exit 0
else
    echo "❌ Some checks failed. Please fix before pushing."
    echo "YAML check: $YAML_EXIT_CODE, Tests: $TEST_EXIT_CODE"
    exit 1
fi
```

Make it executable and run:
```bash
chmod +x pre-push-check.sh
./pre-push-check.sh
```

## 🚀 Running Tests

### Local Execution

**Run tests with Allure results:**
```bash
# Make sure virtual environment is activated
source .venv2/bin/activate

# Run tests and generate Allure results
pytest --alluredir=allure-results -v
```

**Generate and view Allure report:**
```bash
# Generate HTML report
allure generate allure-results --clean -o allure-report

# Serve report locally
allure serve allure-results

# Quick test run with report
./output/scripts/run_tests.sh

# Serve existing results
allure serve output/allure/allure-results

# Generate HTML report
allure generate output/allure/allure-results --clean

# Check history status
ls -la output/allure/history/
```

### Docker Execution

**Build and run with Docker:**
```bash
# Build Docker image
docker build -t petstore-tests .

# Run tests with volume mapping for results
docker run -v $(pwd)/allure-results:/app/allure-results petstore-tests
```

## 🔄 CI/CD with GitHub Actions

This repository is configured with **GitHub Actions** for automated testing and reporting.

### Automated Triggers
- ✅ **Automatic execution** on every `push` to `main` branch
- ✅ **Manual trigger** available via GitHub Actions interface
- ✅ **Automatic report deployment** to GitHub Pages

### How to Run Tests via GitHub Actions

1. **Navigate to Actions tab** in your repository
2. **Select "Pytest Allure Report"** workflow
3. **Click "Run workflow"** button
4. **Monitor execution** in real-time
5. **View results** after completion

### Workflow Configuration
- Configuration file: [.github/workflows/pytest.yml](.github/workflows/pytest.yml)
- Python version: 3.9
- Test results: Allure reports with historical trends
- Automatic deployment: GitHub Pages

## 📊 Test Results and Reports

### Accessing Reports

**Live Allure Report:**
- **Main URL**: https://kovalillia.github.io/petstore-api-tests/
- **Features**: Historical trends, detailed test cases, environment info

**Local Reports:**
- **Allure results**: `allure-results/` directory
- **HTML report**: `allure-report/` directory (after generation)

### Report Features

- **Historical Trends**: Track test execution over time
- **Detailed Test Cases**: Step-by-step test execution
- **Environment Information**: Test execution context
- **Attachments**: Request/response data, screenshots (if applicable)

### How to View Updated Reports

1. **After CI/CD execution**, reports are automatically updated
2. **Open the main URL**: https://kovalillia.github.io/petstore-api-tests/
3. **If seeing cached data**, use `Ctrl+F5` (hard refresh) in your browser
4. **Check "Trends" tab** in Allure for historical data


```

## 🛠 Troubleshooting

### Common Issues

**Virtual Environment Activation:**
```bash
# If activation fails, check Python version
python --version

# Recreate virtual environment if needed
deactivate
rm -rf .venv2
python3 -m venv .venv2
source .venv2/bin/activate
```

**YAML Validation Warnings:**
```bash
# Ignore truthy value warnings for GitHub Actions
yamllint .github/workflows/pytest.yml --no-warnings

# Or disable specific rule
yamllint -d "{extends: relaxed, rules: {truthy: disable}}" .github/workflows/pytest.yml
```

**Act Installation Issues:**
```bash
# Alternative installation method for act
# Using Go (if installed)
go install github.com/nektos/act@latest

# Check act version and requirements
act --version
```

**Allure Report Not Updating:**
- Use `Ctrl+F5` for hard refresh in browser
- Clear browser cache for the site
- Check GitHub Actions workflow status

**Dependencies Issues:**
```bash
# Update pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. **Run validation checks:**
   ```bash
   yamllint .github/workflows/pytest.yml
   ./pre-push-check.sh  # if using validation script
   ```
5. Run tests locally
6. Submit a pull request


---

**Development Workflow:**
1. 🔧 Make changes to code or workflow
2. 🔍 Run `yamllint .github/workflows/pytest.yml` to validate syntax
3. 🧪 Test locally with `act -j test` (optional)
4. 🚀 Run `./pre-push-check.sh` for comprehensive validation
5. 📤 Push changes to repository
6. ✅ Monitor GitHub Actions execution
7. 📊 Check updated reports at https://kovalillia.github.io/petstore-api-tests/

**Note**: Always activate your virtual environment (`.venv2`) before running tests or installing dependencies to maintain environment isolation.
