import { createStore, applyMiddleware, compose } from 'redux';
import loadInitialState from './loadInitialState';

import thunkMiddleware from 'redux-thunk';
import rootReducer from './rootReducer';

const initialState = loadInitialState();

const middleware = [thunkMiddleware];
const composedEnhancers = compose(
	applyMiddleware(...middleware)
);

export function initializeStore() {
	let store;

	store = createStore(
        rootReducer,
		initialState,
		composedEnhancers
	);

	return store;
}