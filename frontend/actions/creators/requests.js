import * as Actions from '../requests';
import axios from 'axios/index';
import getConfig from 'next/config';
const { publicRuntimeConfig } = getConfig();

export const createRequest = (_data) => async dispatch => {
	dispatch({ type: Actions.CREATE_REQUEST });
	try {
		const { data } = await axios.post(`${publicRuntimeConfig.apiUrl}/help-requests/`, _data);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_CREATE_REQUEST, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_CREATE_REQUEST }));
	}
};