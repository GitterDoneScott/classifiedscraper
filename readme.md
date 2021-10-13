## VS Code on MacOS with a virtual env
### Start VS Code with virtual env

    python -m venv myvenv
    code .

### Run a terminal and install required packages in virtual environment
    command + shift + `
    pip install -r requirements.txt

### Update packages
    pip list --outdated
    pip-review --auto

### Export required environment variables to shell
create .env in current workspace

    export $(grep -v '^#' .env | xargs)

### Save latest package list to requirements.txt
    pip freeze > requirements.txt

### Debugging Scrapy
1. https://docs.scrapy.org/en/latest/topics/debug.html

### Building a multi-architecture container
    docker buildx create --use
    docker buildx build --platform linux/amd64,linux/arm64 --push --tag gitterdone/classifiedscraper:latest .
    

