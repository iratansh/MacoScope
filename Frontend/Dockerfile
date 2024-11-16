# Use the official Node.js image for building the app
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json, then install dependencies
COPY package*.json ./
RUN npm ci  # Use 'ci' for a clean install based on package-lock.json

# Copy the rest of the application code
COPY . .

# Build the Vue.js application
RUN npm run build

# Use a lightweight Nginx image to serve the built files
FROM nginx:alpine

# Remove the default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom Nginx configuration (if you have one)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built application files to Nginx's html directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
