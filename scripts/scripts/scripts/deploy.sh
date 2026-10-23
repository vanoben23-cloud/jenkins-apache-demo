
#!/bin/bash
set -e

echo "Starting Jenkins deployment..."

sudo cp index.html /var/www/html/index.html

sudo systemctl reload apache2

echo "Apache website deployed successfully!"
