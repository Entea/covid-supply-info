import * as Actions from '../donates'
import * as Constants from '../../constants'
import axios from 'axios/index'

export const fetchDonates = () => async dispatch => {
    dispatch({ type: Actions.FETCH_DONATES });
    try {
        const { data } = await axios.get(`${Constants.API_URL}donations/`);
        return Promise.resolve(dispatch({ type: Actions.SUCCESS_FETCH_DONATES, data }));
    } catch (err) {
        return Promise.resolve(dispatch({ type: Actions.FAILURE_FETCH_DONATES }));
    }
}