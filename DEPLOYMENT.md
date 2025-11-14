# Deployment Guide for Vercel

## Prerequisites
1. Install Vercel CLI: `npm install -g vercel`
2. Create a Vercel account at https://vercel.com

## Deployment Steps

### 1. Login to Vercel
```bash
vercel login
```

### 2. Deploy the application
From your project directory:
```bash
vercel
```

### 3. Environment Variables (Optional)
Set these in Vercel dashboard if needed:
- `SECRET_KEY`: A secure random key for Flask sessions
- `DATABASE_URL`: If using external database (optional, defaults to SQLite)

## Important Notes

### Database
- The app uses SQLite by default in `/tmp/` on Vercel
- Data is ephemeral (resets on each deployment)
- For persistent data, consider using a cloud database like PlanetScale, Supabase, or Railway

### File Uploads
- Files are uploaded to `/tmp/uploads` on Vercel
- Files are ephemeral (lost on server restart)
- For persistent file storage, consider using cloud storage like AWS S3, Cloudinary, or Vercel Blob

### SocketIO
- Real-time features (SocketIO) are disabled in production
- This is due to Vercel's serverless architecture
- Consider using alternatives like Server-Sent Events if real-time features are needed

## Production Considerations

1. **Database**: Consider migrating to a persistent database service
2. **File Storage**: Implement cloud storage for uploads
3. **Secret Key**: Use a strong, unique secret key in production
4. **Error Handling**: Monitor logs through Vercel dashboard
5. **Performance**: Database operations might be slower in serverless environment

## Troubleshooting

If deployment fails:
1. Check logs in Vercel dashboard
2. Ensure all dependencies are in `requirements-vercel.txt`
3. Verify Python version compatibility
4. Check for missing imports or syntax errors

## Local Testing with Production Config
```bash
export FLASK_ENV=production
python app.py
```