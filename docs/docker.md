# Trying it out with Docker

A sample project is available along with a Dockerfile to make it easy to try
out django-watchman. It includes examples of how to write simple custom checks.

One of the custom checks will always fail, so if you want to see what responses
look like with 100% succeeding checks, add `?skip=sample_project.checks.fail_custom_check`

## Requirements

- [Docker](https://www.docker.com/get-docker)

## Instructions

1. Build and run the Docker image with the current local code: `just run`
2. Visit watchman json endpoint in your browser: <http://127.0.0.1:8000/watchman/>
3. Visit watchman json endpoint in your browser: <http://127.0.0.1:8000/watchman/?skip=sample_project.checks.fail_custom_check>
4. Visit watchman dashboard in your browser: <http://127.0.0.1:8000/watchman/dashboard/>
5. Visit watchman dashboard in your browser: <http://127.0.0.1:8000/watchman/dashboard/?skip=sample_project.checks.fail_custom_check>
6. Visit watchman ping in your browser: <http://127.0.0.1:8000/watchman/ping/>
7. Visit watchman bare status in your browser: <http://127.0.0.1:8000/watchman/bare/>
