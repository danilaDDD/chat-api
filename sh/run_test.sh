./sh/migrate.sh
pytest -v ./test --cov=app \
                 --cov=settings \
                  --cov=db \
                 --cov-report=xml:/app/reports/xml \
                 --cov-report=html:/app/reports/html