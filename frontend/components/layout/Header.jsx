import React, {Component} from 'react';
import Link from 'next/link';

import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import Select from 'react-select'

import {
    fetchRegions as fetchRegionsAction,
} from '../../actions/creators/regions'

import {
    fetchDistricts as fetchDistrictsAction,
} from '../../actions/creators/districts'

import {
    fetchLocalities as fetchLocalitiesAction,
} from '../../actions/creators/localities'


class Header extends Component {
    state = {
        regionValue: null,
        districtValue: null,
        localityValue: null
    };

    updateFilterValues() {
        const regionId = this.state.regionValue ? this.state.regionValue.value : null;
        const districtId = this.state.districtValue ? this.state.districtValue.value : null;
        const localityId = this.state.localityValue ? this.state.localityValue.value : null;
        this.props.onFilterChange(regionId, districtId, localityId);
    }

    onRegionChange(region) {
        if ('value' in region) {
            this.props.fetchDistrictsAction(region.value);

            this.setState(
                (state) => ({regionValue: region, districtValue: null, localityValue: null}),
                () => this.updateFilterValues()
            );
        }
    }

    onDistrictChange(district) {
        if ('value' in district) {
            this.props.fetchLocalitiesAction(district.value);

            this.setState(
                (state) => ({districtValue: district}),
                () => {
                    this.setState(
                        (state) => ({localityValue: null}),
                        () => this.updateFilterValues()
                    );
                }
            );
        }
    }

    onLocalityChange(locality) {
        if ('value' in locality) {
            this.setState(
                (state) => ({localityValue: locality}),
                () => this.updateFilterValues()
            );
        }
    }

    componentDidMount() {
        this.props.fetchRegionsAction();
    }

    onRegionOptionsMessage() {
        return "Область";
    }

    onDistrictOptionsMessage() {
        return "Город";
    }

    onLocalityOptionsMessage() {
        return "Район";
    }

    render() {

        const {localities, districts, regions} = this.props;

        const regionOptions = (regions || []).map((region, index) => {
            return {value: region.id, label: region.name};
        });

        const districtOptions = (districts || []).map((district, index) => {
            return {value: district.id, label: district.name};
        });

        const localityOptions = (localities || []).map((locality, index) => {
            return {value: locality.id, label: locality.name};
        });

        return (
            <header className="fixed-top">
                <nav className="navbar navbar-expand-md center">
                    <img src='logo.png' className="logo" alt="logo"/>
                    <a className="navbar-brand" href="/">HELPMAP</a>
                    <button className="navbar-toggler" type="button" data-toggle="collapse"
                            data-target="#navbarCollapse"
                            aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"/>
                    </button>
                    <form className="form-inline search-box">
                        <input className="form-control mr-sm-2 input-search" type="text" placeholder="Поиск больницы"
                               aria-label="Search"/>
                        <button className="search-btn" type="submit"><img src='mdi_search.svg' alt=""/></button>
                    </form>
                    <div className="collapse navbar-collapse" id="navbarCollapse">
                        <ul className="navbar-nav mr-auto">
                            <li className="nav-item active">
                                <a className="nav-link active" href="/">Карта</a>
                            </li>
                            <li className="nav-item">
                                <Link href="/donations">
                                    <a className="nav-link">Список пожертований</a>
                                </Link>

                            </li>
                            <li className="nav-item">
                                <a className="nav-link" href="http://test.kg/">Контакты</a>
                            </li>
                            <li className="nav-item float-right">
                                <a className="btn btn-primary" href="http://test.kg/">ПОДАТЬ ЗАЯВКУ</a>
                            </li>
                        </ul>
                    </div>
                </nav>
                <div className="center">
                    <div className="row">
                        <div className="filters-box">
                            {<Select instanceId={'region-id'}
                                     isLoading={this.props.regionFetching}
                                     placeholder={'Область'}
                                     className={'dropdown'}
                                     onChange={this.onRegionChange.bind(this)}
                                     noOptionsMessage={this.onRegionOptionsMessage.bind(this)}
                                     options={regionOptions}/>}

                            {<Select instanceId={'district-id'}
                                     isLoading={this.props.districtFetching}
                                     placeholder={'Город'}
                                     value={this.state.districtValue}
                                     className={'dropdown'}
                                     onChange={this.onDistrictChange.bind(this)}
                                     noOptionsMessage={this.onDistrictOptionsMessage.bind(this)}
                                     options={districtOptions}/>}

                            {<Select instanceId={'locality-id'}
                                     isLoading={this.props.localityFetching}
                                     placeholder={'Район'}
                                     noOptionsMessage={this.onLocalityOptionsMessage.bind(this)}
                                     value={this.state.localityValue}
                                     className={'dropdown'}
                                     onChange={this.onLocalityChange.bind(this)}
                                     options={localityOptions}/>}
                        </div>
                    </div>
                </div>
            </header>
        );
    }
}


const mapStateToProps = (state) => {
    return {
        regionFetching: state.regions.fetching,
        regions: state.regions.results,
        districtFetching: state.districts.fetching,
        districts: state.districts.results,
        localityFetching: state.localities.fetching,
        localities: state.localities.results,
    }
};

const mapDispatchToProps = (dispatch) => bindActionCreators({
    fetchRegionsAction,
    fetchDistrictsAction,
    fetchLocalitiesAction
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(Header)
