set -e

python3 -m src.main

python3 -m http.server 8888 --directory public