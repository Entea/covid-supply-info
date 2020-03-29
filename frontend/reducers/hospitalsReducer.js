import * as Actions from '../actions/hospitals'

const initialState = {
	fetching: false,
	count: 0,
	results: [],
	single: {}
};

export default function hospitals(state = initialState, action) {
	switch (action.type) {
		case Actions.FETCH_HOSPITALS:
			return {
				...state,
				fetching: true
			};

		case Actions.SUCCESS_FETCH_HOSPITALS:
			return {
				...state,
				fetching: false,
				count: action.data.count,
				results: action.data
			};

		case Actions.FAILURE_FETCH_HOSPITALS:
			return {
				...state,
				fetching: false
			};

		case Actions.FETCH_HOSPITAL:
			return {
				...state,
				fetching: true
			};

		case Actions.SUCCESS_FETCH_HOSPITAL:
			return {
				...state,
				fetching: false,
				single: action.data
			};

		case Actions.FAILURE_FETCH_HOSPITAL:
			return {
				...state,
				fetching: false
			};

		default:
			return state;
	}
}
