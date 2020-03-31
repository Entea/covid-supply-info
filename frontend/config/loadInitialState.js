import * as status from '../constants/messageStatus';

export default () => {
	return {
		districts: {
			fetching: false,
			count: 0,
			results: [],
			single: {}
		},
		donations: {
			fetching: false,
			count: 0,
			results: [],
			single: {}
		},
		hospitals: {
			fetching: false,
			count: 0,
			results: [],
			single: {}
		},
		localities: {
			fetching: false,
			count: 0,
			results: [],
			single: {}
		},
		regions: {
			fetching: false,
			count: 0,
			results: [],
			single: {}
		},
		requests: {
			sending: false,
			regionFetching: false,
			districtFetching: false,
			localityFetching: false,
			districts:[],
			regions:[],
			localities:[],
		},
		contacts: {
			sending: false,
			status: status.INIT,
			fetching: false,
			data: {}
		}
	}
}