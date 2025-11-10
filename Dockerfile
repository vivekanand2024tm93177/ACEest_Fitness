FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Build-time arg to choose which app file to copy
ARG APP_FILE="app/ACEest_Fitness.py"

# Copy only the selected app file into the image as ACEest_Fitness.py
COPY ${APP_FILE} /app/ACEest_Fitness.py

EXPOSE 5000

# Run the app
CMD ["python", "ACEest_Fitness.py"]
