import * as Actions from '../hospitals';
import axios from 'axios/index'

export const fetchHospitals = () => async dispatch => {
	dispatch({ type: Actions.FETCH_HOSPITALS });
	try {
		const { data } = await axios.get(`http://localhost:8000/api/v1/hospitals/`);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_HOSPITALS, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_HOSPITALS }));
	}
};
export const fetchHospital = (hospitalId) => async dispatch => {
	dispatch({ type: Actions.FETCH_HOSPITAL });
	try {
		const { data } = await axios.get(`http://localhost:8000/api/v1/hospitals/${hospitalId}/`);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_HOSPITAL, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_HOSPITAL }));
	}
};