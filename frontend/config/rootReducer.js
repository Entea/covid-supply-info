import { combineReducers } from 'redux';
import districtsReducer from '../reducers/districtsReducer';
import donationsReducer from '../reducers/donationsReducer';
import hospitalsReducer from '../reducers/hospitalsReducer';
import localitiesReducer from '../reducers/localitiesReducer';
import regionsReducer from '../reducers/regionsReducer';
import requestsReducer from '../reducers/requestsReducer';

export default combineReducers({
	districts: districtsReducer,
	donations: donationsReducer,
	hospitals: hospitalsReducer,
	localities: localitiesReducer,
	regions: regionsReducer,
	requests: requestsReducer
});