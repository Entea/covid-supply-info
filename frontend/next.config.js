require('dotenv').config();

const nextConfig = {
	publicRuntimeConfig: {
		apiUrl: process.env.API_URL,
		mapKey: process.env.MAP_KEY,
	},
};

module.exports = nextConfig;
