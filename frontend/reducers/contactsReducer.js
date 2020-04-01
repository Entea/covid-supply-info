import * as Actions from '../actions/contacts'
import * as status from '../constants/messageStatus'

const initialState = {
    sending: false,
    status: status.INIT,
    fetching: false,
    data: {}
};

export default function districts(state = initialState, action) {
    switch (action.type) {
        case Actions.FETCH_CONTACTS:
            return {
                ...state,
                fetching: true
            };

        case Actions.SUCCESS_FETCH_CONTACTS:
            return {
                ...state,
                fetching: false,
                data: action.data
            };

        case Actions.FAILURE_FETCH_CONTACTS:
            return {
                ...state,
                fetching: false
            };

        case Actions.SEND_MESSAGE:
            return {
                ...state,
                sending: true
            };

        case Actions.SUCCESS_SEND_MESSAGE:
            return {
                ...state,
                sending: false,
                status: status.SUCCESS
            };

        case Actions.FAILURE_SEND_MESSAGE:
            return {
                ...state,
                sending: false,
                status: status.FAILURE
            };

        case Actions.INIT_CONTACT_FORM:
            return {
                ...state,
                status: status.INIT
            };

        default:
            return state;
    }
}
