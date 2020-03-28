import * as Actions from '../donates'
import axios from 'axios/index'

export const fetchDonates = () => async dispatch => {
    dispatch({ type: Actions.FETCH_DONATES });
    try {
        const { data } = await axios.get(`http://localhost:8000/api/v1/donations/`);
        return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_DONATES, data }));
    } catch (err) {
        return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_DONATES }));
    }
}