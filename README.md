# Title: Warranty Tracker App

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

The Warranty Tracker App allows you to store information about your purchased items and tracks their warranties. The app is supposed to be used within the Docker container.

## Features

1. Shops: You can store information about the shops you are purchasing in.

2. Items: You can store information about the goods you are purchasing and the length of its warranty.

3. Database: You can backup your database to a local file and restore it later.

4. Search: You can search items and shops based on their names, comments, addresses etc.


## Requirements

You must have Docker installed. You can install it from https://www.docker.com/

## Installation and Configuration

To install and use this project, please follow the steps below:

1. Clone the project by running the following command in your terminal:
   `git clone https://github.com/tomasmuhr/Warranty-web-5.git`

3. Navigate to the project's directory structure

4. Rename '.env-sample' to '.env'

5. Build the docker image by running the command:
   `docker build -t warranty .`

5. Run the Docker container by running it directly or using docker-compose command:
   - run it directly: `docker run --name warranty_app -d -p 8000:8000 -v warranty:/app/instance/ warranty:latest` or 
   - run it using docker-compose: `docker-compose up`

6. Navigate your browser to `localhost:8000` and the Warranty Tracker App should appear

## Contributing

I have no experience with anyone contributing to my project - if you'd like to contribute to this project, please follow these guidelines and we´ll see what happens:)

- Fork the repository
- Create a new branch
- Make your changes
- Submit a pull request

## License

This project is licensed under the [MIT License](LICENSE).

## Contact
- LinkedIn: <i class="fab fa-linkedin"></i>https://www.linkedin.com/in/tomas-muhr/