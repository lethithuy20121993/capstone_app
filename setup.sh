#!/bin/bash

# Auth0 Configuration
export AUTH0_DOMAIN='dev-thuyle.us.auth0.com'
export API_IDENTIFIER='http://localhost:5000'
export ALGORITHMS='RS256'

# JWT Code Signing Secret (This should be a secret string or your Auth0 signing secret)
export JWT_SECRET='93lq0zKmkuh4owUTajEe4KRIuI2PvfnFpW_bPN2uHRnHKeFDzf13k43BOOeG-gqJ'

# Auth0 Client ID (Replace with your actual Client ID)
export AUTH0_CLIENT_ID='u29Xzy2umyacXkoRiZZOcEhV1H74BAat'

# Database Configuration
export DATABASE_URL='postgresql://postgres:1@localhost:5433/mydb'

echo "Environment variables set!"
