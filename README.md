# YouTube Data API ETL Pipeline
## Overview
This project implements an ETL (Extract, Transform, Load) pipeline to extract data from the YouTube Data API, transform it into a relational format, and load it into an Oracle database for business analysts to be able to implement dashboards using the data for market trend analysis.
## Features
- Extracts channel statistics, video details, and comments from the YouTube Data API.
- Transforms JSON data into a relational format suitable for data warehousing.
- Loads data into staging and warehouse tables in an Oracle database.
- Implements a CI/CD pipeline using GitHub Actions for automated testing and deployment.
- Provides data analysis and reporting capabilities using Oracle APEX.
## Technologies Used
- Python
- Oracle PL/SQL
- YouTube Data API v3
- cx_Oracle
- GitHub Actions
- pytest
## Prerequisites
- Python 3.7+
- Oracle SQL Developer
- Git
- GitHub account
## Setup
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure database connection:
   - Create a `config/.env` file with the following variables:
     ```
     ORACLE_USER=your_oracle_user
     ORACLE_PASSWORD=your_oracle_password
     ORACLE_HOST=your_oracle_host
     ORACLE_PORT=your_oracle_port
     ORACLE_SID=your_oracle_sid
     YOUTUBE_API_KEY=your_youtube_api_key
     ```
   - Ensure `config/.env` is added to `.gitignore`.

5. Set up Oracle database:
   - Run the PL/SQL scripts in the `oracle` directory to create the necessary tables and procedures.

## Usage
This section explains how to run the ETL pipeline and analyze the data.

1. Run the Python scripts in the python directory to extract, transform, and load data.
python python/etl.py
2. Use the PL/SQL scripts in the oracle directory to analyze the data and generate reports.
This project uses GitHub Actions to automate the testing and deployment process. The CI/CD pipeline is defined in the [.github/workflows](.github/workflows) directory.

### Example Workflow File
Below is an example of a GitHub Actions workflow file (`.github/workflows/ci-cd.yml`):
## CI/CD Pipeline
This project uses GitHub Actions to automate the testing and deployment process. The CI/CD pipeline is defined in the .github/workflows directory.
## Contributing
Contributions are welcome! Please submit a pull request with your changes.
## License
This project is licensed under the MIT License - see the LICENSE file for details.
