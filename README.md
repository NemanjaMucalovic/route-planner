# Route Planner

## Introduction

Route Planner is a simple FastAPI backend application that communicates with the Google Maps API to provide information about nearby places filtered by type. It can also generate routes using the Directions API and create PDFs with route information.

## Deployment

To deploy this application, follow these steps:

1. Edit the `env.example` file and rename it to `.env`. In this file, you must provide your Google API key. Other configurations are optional.

2. Build the Docker image:

   ```bash
   docker-compose build
   docker-compose up





