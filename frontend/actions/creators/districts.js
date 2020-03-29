import * as Actions from '../districts';
import axios from 'axios/index';
import getConfig from 'next/config';

const {publicRuntimeConfig} = getConfig();

export const fetchDistricts = (regionId) => async dispatch => {
    const params = {};
    if (regionId) {
        params['region'] = regionId;
    }
    dispatch({type: Actions.FETCH_DISTRICTS});
    try {
        const {data} = await axios.get(`${publicRuntimeConfig.apiUrl}/districts/`, {
            params: params
        });
        return Promise.resolve(dispatch({type: Actions.SUCCESS_FETCH_DISTRICTS, data}));
    } catch (err) {
        return Promise.resolve(dispatch({type: Actions.FAILURE_FETCH_DISTRICTS}));
    }
};

export const fetchDistrict = (districtId) => async dispatch => {
    dispatch({type: Actions.FETCH_DISTRICT});
    try {
        const {data} = await axios.get(`${publicRuntimeConfig.apiUrl}/districts/${districtId}/`);
        return Promise.resolve(dispatch({type: Actions.SUCCESS_FETCH_DISTRICT, data}));
    } catch (err) {
        return Promise.resolve(dispatch({type: Actions.FAILURE_FETCH_DISTRICT}));
    }
};
