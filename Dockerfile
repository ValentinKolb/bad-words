# ---- Build Stage ----
FROM node:16 AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json for installing dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy local source code to the container
COPY src /app/src

# Copy tsconfig.json for compiling TypeScript to JavaScript
COPY tsconfig.json ./

# Compile TypeScript to JavaScript
RUN npm run build

# ---- Run Stage ----
FROM node:16

# Set working directory
WORKDIR /app

# Copy dependencies and built app from build stage
COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/dist /app/dist

# Set environment variables
ENV HOST=0.0.0.0

# Expose the port that your app runs on
EXPOSE 3000

# Command to run the application
CMD ["node", "dist/index.js"]