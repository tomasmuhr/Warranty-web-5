"# Warranty App 5" 
1. Change .env to production and no debug
2. docker build -t warranty .
3. docker run --name warranty_app -d -p 8000:8000 -v warranty:/app/instance/ warranty:latest
4. docker-compose up (if preferred) #TODO