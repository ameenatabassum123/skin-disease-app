# Skin Disease Detection using CNN - Render Deployment

This is a Django web application for skin disease detection using Convolutional Neural Networks (CNN). This README provides instructions for deploying the application to Render.

## Prerequisites

1. A GitHub account
2. A Render account (free tier available)

## Deployment Steps

### 1. Prepare Your Repository

1. Ensure all your code is pushed to a GitHub repository
2. The repository should have the following structure:
   ```
   your-repo/
   ├── SkinDisease/
   │   ├── manage.py
   │   ├── requirements.txt
   │   ├── settings.py
   │   ├── urls.py
   │   ├── wsgi.py
   │   ├── model/
   │   │   ├── model.json
   │   │   ├── model_weights.h5
   │   │   ├── X.txt.npy
   │   │   └── Y.txt.npy
   │   └── SkinDiseaseApp/
   │       ├── views.py
   │       ├── urls.py
   │       ├── templates/
   │       └── static/
   ├── render.yaml
   ├── build.sh
   ├── runtime.txt
   └── README.md
   ```

### 2. Create Render Account

1. Go to [https://render.com](https://render.com)
2. Sign up for a free account
3. Verify your email address

### 3. Deploy Database

1. In your Render dashboard, click "New +" and select "Database"
2. Choose "PostgreSQL" as the database type
3. Give it a name (e.g., "skindisease-db")
4. Choose the free tier if available
5. Click "Create Database"
6. Wait for the database to be provisioned (this may take a few minutes)
7. Once created, note down:
   - Database name (should be "skindisease")
   - Host
   - Port (usually 5432 for PostgreSQL)
   - User
   - Password

### 4. Deploy Web Service

1. In the Render dashboard, click "New +" and select "Web Service"
2. Connect your GitHub account when prompted
3. Select your repository
4. Configure the service:
   - Name: skin-disease-detection (or any name you prefer)
   - Region: Choose the region closest to you
   - Branch: main (or master, depending on your default branch)
   - Root Directory: Leave empty
   - Environment: Python
   - Build Command: `./build.sh`
   - Start Command: `gunicorn SkinDisease.wsgi:application`
5. Click "Create Web Service"

### 5. Configure Environment Variables

1. In your Render dashboard, go to your newly created web service
2. Click on "Environment" in the sidebar
3. Add the following environment variables:
   ```
   SECRET_KEY=django-insecure-7#&_8v5j!zq6%k3*+z2@^+z$5#&*z8z$5#&*z8z$5#&*z8z$5#&*
   DEBUG=False
   DATABASE_HOST=your-database-host
   DATABASE_PORT=5432
   DATABASE_NAME=skindisease
   DATABASE_USER=your-database-user
   DATABASE_PASSWORD=your-database-password
   ```

### 6. Run Initial Setup

1. After the first deployment completes, you'll need to run initial setup commands
2. In your Render dashboard, go to your web service
3. Click on "Shell" in the sidebar
4. Run the following commands:
   ```bash
   python SkinDisease/manage.py migrate
   python SkinDisease/manage.py collectstatic --noinput
   ```

### 7. Test Your Application

1. Once deployment is complete, Render will provide a URL for your application
2. Visit the URL to test your application
3. Try uploading a skin image to test the disease detection feature

## Troubleshooting

### Common Issues

1. **Build Failures**: Check the build logs in your Render dashboard for specific error messages
2. **Database Connection Issues**: Ensure all database environment variables are correctly set
3. **Static Files Not Loading**: Make sure you ran `collectstatic` in the shell
4. **ML Model Issues**: Ensure the model files are in the correct location and accessible

### Checking Logs

1. In your Render dashboard, go to your web service
2. Click on "Logs" in the sidebar to view real-time logs
3. Check for any error messages that might indicate what's going wrong

## Updating Your Application

To update your application after making changes:

1. Push your changes to GitHub
2. Render will automatically start a new deployment
3. Monitor the deployment progress in your dashboard

## Support

For issues with this deployment, please check:
1. Render documentation: https://render.com/docs
2. Django documentation: https://docs.djangoproject.com/
3. This project's issue tracker (if available)