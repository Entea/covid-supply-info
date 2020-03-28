import * as Actions from '../actions/requests'

const initialState = {
	sending: false
};

export default function requests(state = initialState, action) {
	switch (action.type) {
		case Actions.CREATE_REQUEST:
			return {
				...state,
				sending: true
			};

		case Actions.SUCCESS_CREATE_REQUEST:
			return {
				...state,
				sending: false
			};

		case Actions.FAILURE_CREATE_REQUEST:
			return {
				...state,
				sending: false
			};

		default:
			return state;
	}
}