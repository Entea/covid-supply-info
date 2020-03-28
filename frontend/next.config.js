const withSass = require('@zeit/next-sass')
const withFonts = require('next-fonts')
const withPlugins = require('next-compose-plugins');
const webpack = require('webpack');
require('dotenv').config();

const nextConfig = {
    publicRuntimeConfig: {
        apiUrl: process.env.API_URL
    }
};

module.exports = withPlugins([
    [withFonts(withSass())]
], nextConfig)
