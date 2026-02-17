set -euo pipefail

if [[ -f ".env" ]]; then
    source .env
fi

MODE="${1:-}"
CLEAN=false

# Detect --clean flag
for arg in "$@"; do
    if [[ "$arg" == "--clean" ]]; then
        CLEAN=true
    fi
done

if [[ "$MODE" == "local" ]]; then
    if [[ "$CLEAN" == true ]]; then
        docker compose down -v
        docker compose build --no-cache
    else
        docker compose build
    fi

    docker compose up -d
    echo "access at http://localhost:8000/"

elif [[ "$MODE" == "prod" ]]; then
    if [[ "$CLEAN" == true ]]; then
        docker compose -f docker-compose.prod.yaml down -v
        docker compose -f docker-compose.prod.yaml build --no-cache
    else
        docker compose -f docker-compose.prod.yaml build
    fi

    docker compose -f docker-compose.prod.yaml up -d

else
    echo "Error: Please specify 'local' or 'prod' as the argument."
    exit 1
fi