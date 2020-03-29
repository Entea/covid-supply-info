import React, {Component} from 'react';
import Layout from '../components/layout/Layout';
import MainComponent from '../components/main'

import axios from 'axios/index';
import getConfig from 'next/config';

const {publicRuntimeConfig} = getConfig();

import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'

import {
    fetchHospitals as fetchHospitalsAction,
} from '../actions/creators/hospitals'

class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {
            hospitals: []
        };
    }

    componentDidMount() {
        axios.get(`${publicRuntimeConfig.apiUrl}/all_hospitals/`).then(function (response) {
            this.setState({hospitals: response.data});
        }.bind(this));
    }

    updateFilterValues(regionId, districtId, localityId) {
        let params = {};
        if (regionId) {
            params['search_region_id'] = regionId;
        }

        if (districtId) {
            params['search_district_id'] = districtId;
        }

        if (localityId) {
            params['search_locality_id'] = localityId;
        }
        axios
            .get(`${publicRuntimeConfig.apiUrl}/all_hospitals/?`, {
                params: params
            })
            .then(function (response) {
                this.setState({hospitals: response.data});
            }.bind(this));
    }

    render() {
        return (
            <Layout onFilterValuesChange={this.updateFilterValues.bind(this)}>
                <MainComponent filteredHospitals={this.state.hospitals}/>
            </Layout>
        );
    }
}


// const mapStateToProps = (state) => {
//     return {
//         fetching: state.hospitals.fetching,
//         hospitals: state.hospitals.results
//     }
// };
//
// const mapDispatchToProps = (dispatch) => bindActionCreators({
//     fetchHospitalsAction,
// }, dispatch);

// export default connect(mapStateToProps, mapDispatchToProps)(Home)
export default Home;
