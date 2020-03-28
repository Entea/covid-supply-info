import * as Actions from '../donations';
import axios from 'axios/index';
import getConfig from 'next/config';
const { publicRuntimeConfig } = getConfig();

export const fetchDonations = () => async dispatch => {
	dispatch({ type: Actions.FETCH_DONATIONS });
	try {
		const { data } = await axios.get(`${publicRuntimeConfig.apiUrl}/donations/`);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_DONATIONS, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_DONATIONS }));
	}
};

export const fetchDonation = (donationId) => async dispatch => {
	dispatch({ type: Actions.FETCH_DONATION });
	try {
		const { data } = await axios.get(`${publicRuntimeConfig.apiUrl}/donations/${donationId}/`);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_DONATION, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_DONATION }));
	}
};