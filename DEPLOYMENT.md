# AWS EC2 Deployment Guide for Flask Portfolio

This guide explains how to deploy your Flask portfolio to an AWS EC2 instance using Gunicorn and Nginx.

## 1. Launch EC2 Instance
- Launch a `t2.micro` (Free Tier) instance with **Ubuntu Server 22.04 LTS**.
- In **Security Groups**, allow:
  - SSH (Port 22)
  - HTTP (Port 80)
  - HTTPS (Port 443)

## 2. Server Setup
Connect via SSH:
```sh
ssh -i "your-key.pem" ubuntu@your-ec2-ip
```
Update and install dependencies:
```sh
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

## 3. Clone and Prepare App
```sh
git clone https://github.com/nivedvc/my_portfolio.git
cd my_portfolio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

## 4. Configure Environment
Create a `.env` file on the server:
```sh
nano .env
# Paste: SECRET_KEY=your_production_secret_key
```

## 5. Configure Gunicorn
Test gunicorn:
```sh
gunicorn --bind 0.0.0.0:5000 app:app
```

## 6. Configure Nginx
Create a configuration file:
```sh
sudo nano /etc/nginx/sites-available/portfolio
```
Paste this configuration:
```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /home/ubuntu/my_portfolio/static;
    }
}
```
Enable the site:
```sh
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 7. Run Gunicorn as a Service (Recommended)
Use `systemd` to keep the app running in the background.
