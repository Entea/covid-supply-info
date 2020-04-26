import * as Actions from '../regions';
import axios from 'axios/index';
import getConfig from 'next/config';
const { publicRuntimeConfig } = getConfig();

export const fetchRegions = () => async dispatch => {
	dispatch({ type: Actions.FETCH_REGIONS });
	try {
		const { data } = await axios.get(`${publicRuntimeConfig.apiUrl}/regions/`);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_REGIONS, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_REGIONS }));
	}
};

export const fetchRegion = (regionId) => async dispatch => {
	dispatch({ type: Actions.FETCH_REGION });
	try {
		const { data } = await axios.get(`${publicRuntimeConfig.apiUrl}/regions/${regionId}/`);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_REGION, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_REGION }));
	}
};
