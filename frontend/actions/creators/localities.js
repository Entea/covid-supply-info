import * as Actions from '../localities';
import axios from 'axios/index'

export const fetchLocalities = () => async dispatch => {
	dispatch({ type: Actions.FETCH_LOCALITIES });
	try {
		const { data } = await axios.get(`http://localhost:8000/api/v1/localities/`);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_LOCALITIES, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_LOCALITIES }));
	}
};

export const fetchLocality = (localityId) => async dispatch => {
	dispatch({ type: Actions.FETCH_LOCALITY });
	try {
		const { data } = await axios.get(`http://localhost:8000/api/v1/localities/${localityId}/`);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_LOCALITY, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_LOCALITY }));
	}
};