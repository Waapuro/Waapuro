FROM python:3.11

# 创建工作目录
RUN mkdir /app
WORKDIR /app

# Install Python Requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY . /app/

RUN python manage.py collectstatic --noinput

RUN apt-get update && apt-get install -y nginx
COPY .container_cfg/nginx.conf /etc/nginx

# Copy start script and make it executable
COPY configs_container/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Start Gunicorn and Nginx
CMD ["/app/start.sh"]
