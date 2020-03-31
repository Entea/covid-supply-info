import * as Actions from '../actions/requests'
import * as RegionsActions from '../actions/regions'
import * as DistrictsActions from '../actions/districts'
import * as LocalitiesActions from '../actions/localities'

const initialState = {
	sending: false,
	regionFetching: false,
	districtFetching: false,
	localityFetching: false,
	districts:[],
	regions:[],
	localities:[],
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
		case DistrictsActions.FETCH_DISTRICTS:
			return {
				...state,
				districtFetching: true
			};

		case DistrictsActions.SUCCESS_FETCH_DISTRICTS:
			return {
				...state,
				districtFetching: false,
				count: action.data.length,
				districts: action.data
			};

		case DistrictsActions.FAILURE_FETCH_DISTRICTS:
			return {
				...state,
				districtFetching: false
			};
		case LocalitiesActions.FETCH_LOCALITIES:
			return {
				...state,
				localityFetching: true
			};

		case LocalitiesActions.SUCCESS_FETCH_LOCALITIES:
			return {
				...state,
				localityFetching: false,
				count: action.data.length,
				localities: action.data
			};

		case LocalitiesActions.FAILURE_FETCH_LOCALITIES:
			return {
				...state,
				localityFetching: false
			};
		case RegionsActions.FETCH_REGIONS:
			return {
				...state,
				regionFetching: true
			};

		case RegionsActions.SUCCESS_FETCH_REGIONS:
			return {
				...state,
				regionFetching: false,
				count: action.data.length,
				regions: action.data
			};

		case RegionsActions.FAILURE_FETCH_REGIONS:
			return {
				...state,
				regionFetching: false
			};


		default:
			return state;
	}
}