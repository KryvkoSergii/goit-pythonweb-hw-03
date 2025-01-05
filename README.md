# Project Title

This project is a Python web application that performs various tasks as defined in the `main.py` file.

## Requirements

- Python 3.13
- jinja2 3.1.5

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/goit-pythonweb-hw-03.git
    ```
2. Navigate to the project directory:
    ```sh
    cd goit-pythonweb-hw-03
    ```
3. Install the required dependencies:
    ```sh
    poetry install
    ```

## Usage

To run the application, execute the following command:
```sh
poetry run python ./app/main.py
```

## Build and run Docker image
1. In order to build docker image run
```sh
docker build -t goit-pythonweb-hw-03 .
```
2. Run docker container
```sh
docker run -d -p 3000:3000 -v <absolut path>:/app/storage/ goit-pythonweb-hw-03
```

## Features

- Feature 1: Adds message on message page.
- Feature 2: Gets list of messages.
- Feature 3: Has error handling for 404.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.