import * as Actions from '../actions/distributions'

const initialState = {
    fetching: false,
    count: 0,
    results: []
};

export default function distributions(state = initialState, action) {
    switch (action.type) {
        case Actions.FETCH_DISTRIBUTIONS:
            return {
                ...state,
                fetching: true
            };

        case Actions.SUCCESS_FETCH_DISTRIBUTIONS:
            return {
                ...state,
                fetching: false,
                count: action.data.count,
                results: action.data.results
            };

        case Actions.FAILURE_FETCH_DISTRIBUTIONS:
            return {
                ...state,
                fetching: false
            };

        default:
            return state;
    }
}