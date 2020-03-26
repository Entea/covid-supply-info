import { combineReducers } from 'redux';
import exampleReducer from '../reducers/exampleReducer';

export default combineReducers({
	example: exampleReducer,
});