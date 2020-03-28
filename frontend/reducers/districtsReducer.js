import * as Actions from '../actions/districts'

const initialState = {
	fetching: false,
	count: 0,
	results: [],
	single: {}
};

export default function districts(state = initialState, action) {
	switch (action.type) {
		case Actions.FETCH_DISTRICTS:
			return {
				...state,
				fetching: true
			};

		case Actions.SUCCESS_FETCH_DISTRICTS:
			return {
				...state,
				fetching: false,
				count: action.data.count,
				results: action.data.results
			};

		case Actions.FAILURE_FETCH_DISTRICTS:
			return {
				...state,
				fetching: false
			};

		case Actions.FETCH_DISTRICT:
			return {
				...state,
				fetching: true
			};

		case Actions.SUCCESS_FETCH_DISTRICT:
			return {
				...state,
				fetching: false,
				single: action.data
			};

		case Actions.FAILURE_FETCH_DISTRICT:
			return {
				...state,
				fetching: false
			};

		default:
			return state;
	}
}