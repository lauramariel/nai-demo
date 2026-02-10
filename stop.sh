set -euo pipefail

if [ "$1" = "local" ]; then
	docker compose  down
elif [ "$1" = "prod" ]; then
	docker compose -f docker-compose.prod.yaml down
else
	echo "Error: Please specify 'local' or 'prod' as the argument."
	exit 1
fi