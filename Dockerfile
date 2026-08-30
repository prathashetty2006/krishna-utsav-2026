# Use lightweight official Nginx image
FROM nginx:alpine

# Remove default Nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy custom Nginx server configuration
COPY ["Data and Config/nginx.conf", "/etc/nginx/conf.d/default.conf"]

# Copy all project assets and folders to Nginx html directory
COPY [".", "/usr/share/nginx/html/"]

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
