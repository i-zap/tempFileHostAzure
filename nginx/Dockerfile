FROM nginx:alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy custom configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static frontend files
COPY static/ /usr/share/nginx/html/

EXPOSE 80 443
