# Deployment Checklist for Skin Disease Detection on Render

## Pre-Deployment Checklist

### ✅ Project Structure
- [x] Django project is properly structured
- [x] All required files are present (settings.py, urls.py, wsgi.py, manage.py)
- [x] Model files are in the correct location (SkinDisease/model/)
- [x] Templates are created and properly configured
- [x] Static files are organized

### ✅ Configuration Files
- [x] `render.yaml` is configured correctly
- [x] `build.sh` is executable and contains proper commands
- [x] `requirements.txt` includes all necessary dependencies
- [x] `runtime.txt` specifies Python version
- [x] `.gitignore` excludes unnecessary files

### ✅ Settings Configuration
- [x] `settings.py` uses environment variables for production
- [x] Database configuration supports PostgreSQL
- [x] Static files configuration is production-ready
- [x] Security settings are enabled for production
- [x] Allowed hosts are configured properly

### ✅ Dependencies
- [x] Django 3.2.13
- [x] TensorFlow 2.6.0
- [x] Keras 2.6.0
- [x] OpenCV 4.5.5.64
- [x] Gunicorn 20.1.0
- [x] Whitenoise 5.3.0
- [x] psycopg2-binary 2.9.3
- [x] dj-database-url 0.5.0

## Render Deployment Steps

### 1. Database Setup
1. [ ] Go to Render Dashboard
2. [ ] Click "New +" → "Database"
3. [ ] Select "PostgreSQL"
4. [ ] Name: `skindisease`
5. [ ] Choose Free tier
6. [ ] Click "Create Database"
7. [ ] Wait for provisioning (2-3 minutes)

### 2. Web Service Setup
1. [ ] Go to Render Dashboard
2. [ ] Click "New +" → "Web Service"
3. [ ] Connect GitHub repository
4. [ ] Select your repository
5. [ ] Configure settings:
   - Name: `skin-disease-detection`
   - Environment: `Python`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn SkinDisease.wsgi:application --bind 0.0.0.0:$PORT`
6. [ ] Click "Create Web Service"

### 3. Environment Variables (Automatic)
The following environment variables will be set automatically by render.yaml:
- [x] `DATABASE_URL` - from PostgreSQL database
- [x] `SECRET_KEY` - auto-generated
- [x] `DEBUG` - set to "False"
- [x] `WEB_CONCURRENCY` - set to 4
- [x] `ALLOWED_HOSTS` - set to ".onrender.com"

### 4. Build Process
The build script will automatically:
- [x] Install Python dependencies
- [x] Create necessary directories
- [x] Collect static files
- [x] Run database migrations

### 5. Testing
1. [ ] Wait for build to complete (5-10 minutes)
2. [ ] Visit the provided URL
3. [ ] Test the home page loads
4. [ ] Test image upload functionality
5. [ ] Verify disease detection works
6. [ ] Check static files are loading

## Troubleshooting

### Common Issues and Solutions

#### Build Failures
- **Issue**: TensorFlow installation fails
- **Solution**: Check Python version compatibility (3.9.16)

#### Database Connection Issues
- **Issue**: Cannot connect to database
- **Solution**: Verify DATABASE_URL is set correctly

#### Static Files Not Loading
- **Issue**: CSS/JS files not found
- **Solution**: Check collectstatic ran successfully

#### Model Loading Issues
- **Issue**: Model files not found
- **Solution**: Verify model files are in SkinDisease/model/

#### Memory Issues
- **Issue**: Application crashes due to memory
- **Solution**: Consider upgrading to paid tier for more memory

## Post-Deployment

### Monitoring
- [ ] Check application logs regularly
- [ ] Monitor database usage
- [ ] Test functionality periodically
- [ ] Update dependencies as needed

### Maintenance
- [ ] Keep Django and dependencies updated
- [ ] Monitor for security vulnerabilities
- [ ] Backup database regularly
- [ ] Test after any updates

## Support Resources

- Render Documentation: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/3.2/howto/deployment/
- TensorFlow Serving: https://www.tensorflow.org/tfx/guide/serving

## Notes

- The free tier has limitations on build time and memory
- Database will sleep after 90 days of inactivity (free tier)
- Consider upgrading to paid tier for production use
- Always test thoroughly before deploying to production
