## Project Description
This repository contains a set of **automated API tests** to test the operation of the online store service.
The tests are implemented in **Python 3.9** using **pytest**, and also have integration with **Allure** for building detailed reports.
**Docker** is used for ease of launch and environment isolation.

## Goal and objectives
The goal is to verify the stability and correctness of the REST API.
Main tasks:
- testing CRUD operations for `pet`, `store`, `files` resources;
- checking positive and negative scenarios;
- generating structured reports for analyzing results;
- the ability to run tests locally and in CI/CD.

This project **does not include**:
- UI testing;
- load testing.



## Technologies used
- Python 3.9
- Pytest
- Faker (data generation)
- Allure (reporting)
- Docker



## Install and Run 
**Local**
`git clone https://github.com/username/testProject2.git `# Clone the repository
**cd testProject2**


Create a virtual environment and install dependencies
``python3 -m venv .venv``
``source .venv/bin/activate``
``pip install -r requirements.txt``

Run tests with Allure report generation
``pytest --alluredir=allure_report``




## Docker

Build the image
``docker build -t pytest_runner .``

Run tests with result mapping
``docker run -v $(pwd)/output/test_result:/output/test_result pytest_runner``


## Reports

The execution results are stored in the following directories:

``allure_report``/ — when running locally

`test_result`/ — when running in Docker

`allure serve allure_report`/ — You can open the report with the command:

`./output/scripts/run_tests.sh`/- run a script to generate allure report


## 🚀 CI/CD with GitHub Actions

This repository has GitHub Actions configured to automatically run tests:

- ✅ Run automatically on every `push` to `master`

- ✅ Can be run manually via **Actions → Run workflow**
- ✅ Test results are stored as artifacts:
- JUnit XML (`results.xml`)
- HTML report (`report.html`)
- Allure results

Workflow configuration file: 
[.github/workflows/pytest.yml](.github/workflows/pytest.yml) 


### How to run tests manually

1. Go to the **Actions** tab in the repository.
2. Select `Pytest Workflow`.
3. Click the **Run workflow** button.
4. (Optional) enter the Python version (`3.9` or `3.10`).
5. Wait for completion, the results are available in the **Artifacts** tab.

## Test Reports
- [Allure Report](https://kovalillia.github.io/testProject2/)
## 📊 Test Reports

Current test results are available on GitHub Pages:

- [Allure Report](https://kovalillia.github.io/petstore-api-tests/)
- [Pytest HTML Report](https://kovalillia.github.io/testProject2/pytest-report.html)

---

### How to update the report:
1. Run **Pytest Workflow** manually or do a `git push` to the `main` branch.
2. Wait for CI to complete.
3. Reports will be automatically generated and deployed to `gh-pages`.
4. Open [Allure Report](https://kovalillia.github.io/testProject2/) or [Pytest Report](https://kovalillia.github.io/testProject2/pytest-report.html) to view the current results.

---

**Tip:**
You can also download reports as artifacts directly from the **Actions → Run details** tab.