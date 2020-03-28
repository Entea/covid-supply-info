import * as Actions from '../donates'
import axios from 'axios/index'
import getConfig from 'next/config';
const { publicRuntimeConfig } = getConfig();

export const fetchDonates = () => async dispatch => {
    dispatch({ type: Actions.FETCH_DONATES });
    try {
        const { data } = await axios.get(`${publicRuntimeConfig.apiUrl}/donations/`);
        return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_DONATES, data }));
    } catch (err) {
        return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_DONATES }));
    }
}