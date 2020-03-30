import * as Actions from '../localities';
import axios from 'axios/index';
import getConfig from 'next/config';

const {publicRuntimeConfig} = getConfig();

export const fetchLocalities = (districtId) => async dispatch => {
    dispatch({type: Actions.FETCH_LOCALITIES});
    try {
        const params = {};
        if (districtId) {
            params['district'] = districtId;
        }
        const {data} = await axios.get(`${publicRuntimeConfig.apiUrl}/localities/`, {
            params: params
        });
        return Promise.resolve(dispatch({type: Actions.SUCCESS_FETCH_LOCALITIES, data}));
    } catch (err) {
        return Promise.resolve(dispatch({type: Actions.FAILURE_FETCH_LOCALITIES}));
    }
};

export const fetchLocality = (localityId) => async dispatch => {
    dispatch({type: Actions.FETCH_LOCALITY});
    try {
        const {data} = await axios.get(`${publicRuntimeConfig.apiUrl}/localities/${localityId}/`);
        return Promise.resolve(dispatch({type: Actions.SUCCESS_FETCH_LOCALITY, data}));
    } catch (err) {
        return Promise.resolve(dispatch({type: Actions.FAILURE_FETCH_LOCALITY}));
    }
};
