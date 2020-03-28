import * as Actions from '../districts';
import axios from 'axios/index'

export const fetchDistricts = () => async dispatch => {
	dispatch({ type: Actions.FETCH_DISTRICTS });
	try {
		const { data } = await axios.get(`http://localhost:8000/api/v1/districts/`);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_DISTRICTS, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_DISTRICTS }));
	}
};

export const fetchDistrict = (districtId) => async dispatch => {
	dispatch({ type: Actions.FETCH_DISTRICT });
	try {
		const { data } = await axios.get(`http://localhost:8000/api/v1/districts/${districtId}/`);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_DISTRICT, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_DISTRICT }));
	}
};