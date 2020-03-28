import * as Actions from '../actions/localities'

const initialState = {
	fetching: false,
	count: 0,
	results: [],
	single: {}
};

export default function hospitals(state = initialState, action) {
	switch (action.type) {
		case Actions.FETCH_LOCALITIES:
			return {
				...state,
				fetching: true
			};

		case Actions.SUCCESS_FETCH_LOCALITIES:
			return {
				...state,
				fetching: false,
				count: action.data.count,
				results: action.data.results
			};

		case Actions.FAILURE_FETCH_LOCALITIES:
			return {
				...state,
				fetching: false
			};

		case Actions.FETCH_LOCALITY:
			return {
				...state,
				fetching: true
			};

		case Actions.SUCCESS_FETCH_LOCALITY:
			return {
				...state,
				fetching: false,
				single: action.data
			};

		case Actions.FAILURE_FETCH_LOCALITY:
			return {
				...state,
				fetching: false
			};

		default:
			return state;
	}
}