# Use the official Node.js image for building the app
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json, then install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Vue.js application
RUN npm run build

# Use Nginx to serve the built files
FROM nginx:alpine

# Copy the built application files to Nginx's html directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy a custom Nginx configuration if you have one
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80
