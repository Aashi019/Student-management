# 🚀 Vercel Deployment Guide

## Prerequisites
- Your app is configured with Neon PostgreSQL ✅
- Updated `requirements.txt` ✅ 
- Created `vercel.json` configuration ✅

## Step 1: Install Vercel CLI (if not already installed)
```bash
npm install -g vercel
```

## Step 2: Login to Vercel
```bash
vercel login
```

## Step 3: Set Environment Variables

### Option A: Using Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Find your project (or import it)
3. Go to **Settings** → **Environment Variables**
4. Add:
   - **Name**: `DATABASE_URL`
   - **Value**: `postgresql://neondb_owner:npg_XCrcYpHg9SO8@ep-blue-snow-ah4jpxiz-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require`
   - **Environment**: Production

### Option B: Using Vercel CLI
```bash
vercel env add DATABASE_URL
# When prompted, paste your Neon database URL
```

## Step 4: Deploy to Vercel

### First Time Deployment:
```bash
# In your project directory
vercel

# Follow the prompts:
# - Set up and deploy? [Y/n] Y
# - Which scope? [Your username/org]
# - Link to existing project? [Y/n] N (if new project)
# - What's your project's name? student-management
# - In which directory is your code located? ./
```

### Subsequent Deployments:
```bash
# Deploy to production
vercel --prod
```

## Step 5: Access Your Deployed App

After deployment, Vercel will provide you with URLs:
- **Preview URL**: For testing
- **Production URL**: Your live app

## 🎯 Test Your Deployment

### Login Credentials:
- **Admin**: `admin` / `admin123`
- **Teacher**: `teacher1` / `teacher123`
- **Student**: `STU000001` / `student1`

### Test These Features:
1. Login with different user types
2. View dashboard with charts
3. Add/edit students
4. Record attendance
5. Manage grades
6. Fee management
7. Export functionality

## 🛠️ Troubleshooting

### Common Issues:

#### 1. Build Fails
```bash
# Check your requirements.txt has all dependencies
# Ensure vercel.json is properly configured
```

#### 2. Database Connection Error
```bash
# Verify DATABASE_URL is set in Vercel environment variables
# Check Neon database is active
```

#### 3. Import Errors
```bash
# Make sure all dependencies are in requirements.txt
# Check file paths are correct (case-sensitive)
```

#### 4. Large Bundle Size
```bash
# The vercel.json already sets maxLambdaSize to 15mb
# If still too large, consider removing unused dependencies
```

### Debugging Commands:
```bash
# Check deployment logs
vercel logs

# View environment variables
vercel env ls

# Check project details
vercel inspect
```

## 📊 Monitoring

After deployment, monitor:
1. **Vercel Dashboard**: Function execution, errors
2. **Neon Dashboard**: Database connections, queries
3. **Application Logs**: Use `vercel logs` for runtime issues

## 🔄 Updates

To update your deployed app:
```bash
# Make your changes
git add .
git commit -m "Update description"

# Deploy updates
vercel --prod
```

## 📝 Environment Variables Reference

Required environment variables in Vercel:
- `DATABASE_URL`: Your Neon PostgreSQL connection string

Optional:
- `SECRET_KEY`: Flask secret key (defaults to the one in app.py)
- `FLASK_ENV`: Set to "production" (already configured in vercel.json)

## 🎉 Success!

Your Student Management System is now deployed on Vercel with:
- ✅ Neon PostgreSQL database
- ✅ Real-time features (SocketIO)
- ✅ File uploads
- ✅ PDF/Excel exports
- ✅ Complete fee management
- ✅ Multi-role authentication