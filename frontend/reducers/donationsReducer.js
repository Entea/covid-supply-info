import * as Actions from '../actions/donations'

const initialState = {
	fetching: false,
	count: 0,
	results: [],
	single: {}
};

export default function donations(state = initialState, action) {
	switch (action.type) {
		case Actions.FETCH_DONATIONS:
			return {
				...state,
				fetching: true
			};

		case Actions.SUCCESS_FETCH_DONATIONS:
			return {
				...state,
				fetching: false,
				results: action.data
			};

		case Actions.FAILURE_FETCH_DONATIONS:
			return {
				...state,
				fetching: false
			};

		case Actions.FETCH_DONATION:
			return {
				...state,
				fetching: true
			};

		case Actions.SUCCESS_FETCH_DONATION:
			return {
				...state,
				fetching: false,
				single: action.data
			};

		case Actions.FAILURE_FETCH_DONATION:
			return {
				...state,
				fetching: false
			};

		default:
			return state;
	}
}