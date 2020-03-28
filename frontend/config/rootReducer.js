import { combineReducers } from 'redux';
import donateReducer from '../reducers/donatesReducer';
export default combineReducers({
	donates: donateReducer,
});