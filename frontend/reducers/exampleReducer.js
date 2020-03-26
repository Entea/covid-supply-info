import * as Actions from '../actions/example'

const initialState = '';

export default function bonus(state = initialState, action) {
    switch (action.type) {
        case Actions.CLICK_EXAMPLE:
            return action.data;

        default:
            return state;
    }
}