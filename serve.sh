#!/bin/bash
# Local preview server for the Overloop blog
# Run: ./serve.sh
# Then open: http://localhost:8000/blog/en/

echo "Starting local preview at http://localhost:8000"
echo "  Blog EN: http://localhost:8000/blog/en/"
echo "  Blog DE: http://localhost:8000/blog/de/"
echo "  Blog FR: http://localhost:8000/blog/fr/"
echo "  Blog ES: http://localhost:8000/blog/es/"
echo "  Tools:   http://localhost:8000/tools/"
echo ""
echo "Press Ctrl+C to stop."
python3 -m http.server 8000
