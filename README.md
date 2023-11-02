

<div align="center">
  <img src="https://res.cloudinary.com/murste/image/upload/v1698907632/stevolve_x8ioeu.png" alt="Stephen Murichu's Logo" width="100" />
</div>

# Django-based Authentication Service with RESTful API

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.10-green)


This Django-based Authentication Service provides a RESTful API for user management, including user registration, login, token-based authentication, password reset, and email services. It's built using Django Rest Framework, equipped with unit tests for secure user management.

## Table of Contents

1. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
2. [Features](#features)
3. [Usage](#usage)
4. [Testing](#testing)
5. [Contributing](#contributing)
6. [License](#license)
7. [Contact Information](#contact-information)

## Getting Started

### Prerequisites

Before running the Authentication Service, make sure you have the following installed:

- [Python](https://www.python.org/) (3.10 or higher)
- [Docker](https://www.docker.com/)

### Installation

To set up and run the service, you can use the provided setup script:

```bash
chmod +x bin/setup.sh
./bin/setup.sh
```

This script does the following:

1. Sets up a virtual environment.
2. Builds the Docker image for the Django Authentication Service.
3. Runs the Docker container on port 8000.

Make sure to configure environment variables in a `.env` file.
```
   EMAIL_HOST=your-smtp-host
   EMAIL_PORT=your-smtp-port
   EMAIL_USE_TLS=True  # Change to False if not using TLS
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-email-password
   DEFAULT_FROM_EMAIL=your-sender@example.com
```
## Features

- User registration with email and password.
- User login with token-based authentication.
- Password reset functionality.
- Email services for registration and password reset.

## Usage

1. Register a new user:
   - Send a POST request to `/api/register/` with a JSON body containing `username`, `email`, and `password`.
2. Login to get an access token:
   - Send a POST request to `/api/login/` with `username` and `password` in the request body. The response will contain an access token.
3. Request a password reset:
   - Send a POST request to `/api/password-reset-request/` with the user's `email`. This will send a password reset email with a reset token.
4. Reset the password:
   - Use the reset token received in the email to reset the user's password by sending a POST request to `/api/reset-password/{token}/{user_id}/`.


## Testing

The service includes unit tests for secure user management. You can run the tests with the following command:

```bash
python manage.py test authentication
```

## Contributing

I welcome contributions to this project. To contribute, please follow these guidelines:
1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Write tests for your changes.
5. Ensure your changes pass the tests.
6. Create a pull request.

## License

This Authentication Service is licensed under the [MIT License](LICENSE).

## Contact Information

For questions or suggestions, please visit my [GitHub profile](https://github.com/munuhee).
