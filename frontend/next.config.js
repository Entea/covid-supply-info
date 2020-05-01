require('dotenv').config();

const nextConfig = {
	publicRuntimeConfig: {
		apiUrl: process.env.API_URL,
		recaptchaSiteKey: process.env.RECAPTCHA_SITE_KEY,
		recaptchaSecretKey: process.env.RECAPTCHA_SECRET_KEY,
		gaKey: process.env.GA_KEY,
	},
};

module.exports = nextConfig;
