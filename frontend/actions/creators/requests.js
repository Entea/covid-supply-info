import * as Actions from '../requests';
import axios from 'axios/index'

export const createRequest = (_data) => async dispatch => {
	dispatch({ type: Actions.CREATE_REQUEST });
	try {
		const { data } = await axios.post(`http://localhost:8000/api/v1/help-requests/`, _data);
		return Promise.resolve(dispatch({ type: Actions.SUCCESS_CREATE_REQUEST, data }));
	} catch (err) {
		return Promise.resolve(dispatch({ type: Actions.FAILURE_CREATE_REQUEST }));
	}
};