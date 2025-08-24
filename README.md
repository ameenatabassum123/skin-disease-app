# Skin Disease Detection using CNN - Render Deployment

This is a Django web application for skin disease detection using Convolutional Neural Networks (CNN). The application can detect 9 different types of skin diseases from uploaded images.

## Features

- **AI-Powered Detection**: Uses CNN model to analyze skin images
- **9 Disease Categories**: 
  - Actinic Keratosis
  - Basal Cell Carcinoma
  - Dermatofibroma
  - Melanoma
  - Nevus
  - Pigmented Benign Keratosis
  - Seborrheic Keratosis
  - Squamous Cell Carcinoma
  - Vascular Lesion
- **Web Interface**: User-friendly web interface for image upload and analysis
- **Confidence Scoring**: Provides confidence percentage for predictions

## Prerequisites

1. A GitHub account
2. A Render account (free tier available)

## Project Structure

```
skin.project/
├── SkinDisease/
│   ├── manage.py
│   ├── requirements.txt
│   ├── SkinDisease/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── SkinDiseaseApp/
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── templates/
│   │   └── static/
│   └── model/
│       ├── model.json
│       ├── model_weights.h5
│       ├── X.txt.npy
│       └── Y.txt.npy
├── render.yaml
├── build.sh
├── runtime.txt
└── README.md
```

## Deployment Steps

### 1. Prepare Your Repository

1. Ensure all your code is pushed to a GitHub repository
2. The repository should have the structure shown above

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
   - Start Command: `gunicorn SkinDisease.wsgi:application --bind 0.0.0.0:$PORT`
5. Click "Create Web Service"

### 5. Automatic Configuration

The application is configured to automatically:
- Use the PostgreSQL database from Render
- Set up environment variables
- Collect static files
- Run database migrations

### 6. Test Your Application

1. Once deployment is complete, Render will provide a URL for your application
2. Visit the URL to test your application
3. Try uploading a skin image to test the disease detection feature

## Local Development

To run the application locally:

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r SkinDisease/requirements.txt
   ```
3. Run migrations:
   ```bash
   python SkinDisease/manage.py migrate
   ```
4. Start the development server:
   ```bash
   python SkinDisease/manage.py runserver
   ```

## Important Notes

- **Medical Disclaimer**: This application is for educational and research purposes only. It should not replace professional medical diagnosis. Always consult with a healthcare professional for accurate diagnosis and treatment.
- **Model Accuracy**: The CNN model has been trained on a specific dataset and may not be 100% accurate for all skin conditions.
- **Image Requirements**: For best results, upload clear, well-lit images of the skin area.

## Troubleshooting

### Common Issues

1. **Build Failures**: Check the build logs in your Render dashboard for specific error messages
2. **Database Connection Issues**: Ensure the database is properly provisioned and the DATABASE_URL is set
3. **Static Files Not Loading**: The build script automatically runs collectstatic
4. **ML Model Issues**: Ensure the model files are in the correct location (SkinDisease/model/)

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

## License

This project is for educational purposes. Please ensure you have proper licenses for any datasets or models used.