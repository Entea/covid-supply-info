import ReactGA from 'react-ga'
import getConfig from 'next/config';

const {publicRuntimeConfig} = getConfig();

export const initGA = () => {
    console.log(publicRuntimeConfig)
    if (publicRuntimeConfig.gaKey) {
        ReactGA.initialize(publicRuntimeConfig.gaKey)
    } else {
        console.log('Skipping GA init');
    }
}

export const logPageView = () => {
    if (publicRuntimeConfig.gaKey) {
        ReactGA.set({page: window.location.pathname})
        ReactGA.pageview(window.location.pathname)
    }
}

export const logEvent = (category = '', action = '') => {
    if (publicRuntimeConfig.gaKey) {
        if (category && action) {
            ReactGA.event({category, action})
        }
    }
}

export const logException = (description = '', fatal = false) => {
    if (publicRuntimeConfig.gaKey) {
        if (description) {
            ReactGA.exception({description, fatal})
        }
    }
}