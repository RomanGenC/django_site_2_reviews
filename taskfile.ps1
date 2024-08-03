param (
    [string]$Command
)

function Run-Server {
    Write-Host "Starting server with poetry..."
    poetry run python3 manage.py runserver
}

function Run-Linters {
    Write-Host "Running ruff..."
    ruff check . --fix

    Write-Host "Running mypy..."
    mypy .

    Write-Host "Running flake8..."
     flake8 . --max-line-length=100
}

switch ($Command) {
    "run" {
        Run-Server
        break
    }
    "lint" {
        Run-Linters
        break
    }
    default {
        Write-Host "Unknown command: $Command"
        break
    }
}
