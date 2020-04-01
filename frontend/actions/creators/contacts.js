import * as Actions from '../contacts';
import axios from 'axios/index';
import getConfig from 'next/config';

const {publicRuntimeConfig} = getConfig();

export const fetchContacts = () => async dispatch => {
    dispatch({type: Actions.FETCH_CONTACTS});
    try {
        const {data} = await axios.get(`${publicRuntimeConfig.apiUrl}/contact-info/`);
        return Promise.resolve(dispatch({type: Actions.SUCCESS_FETCH_CONTACTS, data}));
    } catch (err) {
        return Promise.resolve(dispatch({type: Actions.FAILURE_FETCH_CONTACTS}));
    }
};

export const sendMessage = (_data) => async dispatch => {
    dispatch({type: Actions.SEND_MESSAGE});
    try {
        await axios.post(`${publicRuntimeConfig.apiUrl}/contact-messages/`, _data);
        return Promise.resolve(dispatch({type: Actions.SUCCESS_SEND_MESSAGE}));
    } catch (err) {
        return Promise.resolve(dispatch({type: Actions.FAILURE_SEND_MESSAGE}));
    }
};

export const init = () => async dispatch => {
    dispatch({type: Actions.INIT_CONTACT_FORM});
};
