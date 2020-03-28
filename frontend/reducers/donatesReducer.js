import * as Actions from '../actions/donates'

const initialState = {
	fetching: false,
	data: {results:[]},
};

export default function bonus(state = initialState, action) {
	switch (action.type) {
		case Actions.FETCH_DONATES:
			return {
				...state,
				fetching: true
			};

		case Actions.SUCCESS_FETCH_DONATES:
			return {
				...state,
				fetching: false,
				data: action.data
			};

		default:
			return state;
	}
}