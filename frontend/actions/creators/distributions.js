import * as Actions from '../distributions';
import axios from 'axios/index';
import getConfig from 'next/config';
const { publicRuntimeConfig } = getConfig();

export const fetchDistributions = (donationId) => async dispatch => {
	dispatch({ type: Actions.FETCH_DISTRIBUTIONS });
	try {
		const { data } = await axios.get(`${publicRuntimeConfig.apiUrl}/distributions?donations=${donationId}`);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_DISTRIBUTIONS, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_DISTRIBUTIONS }));
	}
};
