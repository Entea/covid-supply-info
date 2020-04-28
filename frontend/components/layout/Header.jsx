import React, {Component, Fragment} from 'react';
import Link from '../navigation/ActiveLink';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import Select from 'react-select';
import {Navbar, Form, FormControl, NavDropdown, Nav, Button, Modal} from 'react-bootstrap'
import {
	fetchRegions as fetchRegionsAction,
} from '../../actions/creators/regions'
import {
	fetchDistricts as fetchDistrictsAction,
} from '../../actions/creators/districts'
import {
	fetchLocalities as fetchLocalitiesAction,
} from '../../actions/creators/localities'
import {
	fetchHospitals as fetchHospitalsAction
} from '../../actions/creators/hospitals'
import HelpRequest from "../helpRequest";

class Header extends Component {
	state = {
		districts: [],
		localities: [],
		regionValue: null,
		districtValue: null,
		localityValue: null,
		search: '',
		searchMenu: false
	};

	onChange = (e) => {
		this.setState({
			[e.target.name]: e.target.value
		})
	};

	updateFilterValues = (e) => {
		e && e.preventDefault();
		const {regionValue, districtValue, localityValue, search} = this.state;
		const regionId = regionValue ? regionValue.value : null;
		const districtId = districtValue ? districtValue.value : null;
		const localityId = localityValue ? localityValue.value : null;
		this.props.fetchHospitalsAction(regionId, districtId, localityId, search);
        this.setState({searchMenu: false})
	};

	onRegionChange(region) {
		if (region) {
			this.props.fetchDistrictsAction(region.value).then(() => this.setState({ districts: this.props.districts }));

			this.setState({ regionValue: region, districtValue: null, localityValue: null },
				() => this.updateFilterValues()
			);
		} else {
			this.setState({ districts: [], regionValue: null, districtValue: null, localityValue: null }, () => this.updateFilterValues())
		}
	};

	onDistrictChange(district) {
		if (district) {
			this.props.fetchLocalitiesAction(district.value).then(() => this.setState({ localities: this.props.localities }));

			this.setState({ districtValue: district },
				() => this.updateFilterValues()
			);
		} else {
			this.setState({ localities: [], districtValue: null, localityValue: null }, () => this.updateFilterValues())
		}
	};

	onLocalityChange(locality) {
		if (locality) {
			this.setState({ localityValue: locality },
				() => this.updateFilterValues()
			);
		} else {
			this.setState({ localityValue: null }, () => this.updateFilterValues());
		}
	};

	componentDidMount() {
		this.props.fetchHospitalsAction();
		this.props.fetchRegionsAction();
	};

	onRegionOptionsMessage() {
		return 'Область';
	};

	onDistrictOptionsMessage() {
		return 'Город';
	};

	onLocalityOptionsMessage() {
		return 'Район';
	};

	toggleSearchMenu(e) {
		e.preventDefault();
		this.setState({searchMenu: !this.state.searchMenu})
	};

	render() {
		const { regions } = this.props;
		const { localities, districts, searchMenu } = this.state;

		const regionOptions = (regions || []).map((region, index) => {
			return { value: region.id, label: region.name };
		});

		const districtOptions = (districts || []).map((district, index) => {
			return { value: district.id, label: district.name };
		});

		const localityOptions = (localities || []).map((locality, index) => {
			return { value: locality.id, label: locality.name };
		});

		return (
			<header className="fixed-top">
        <Navbar className="center only-mobile" expand="lg">
          <Navbar.Toggle aria-controls="menu" >
            <img src="/mdi_menu.svg" alt="menu"/>
					</Navbar.Toggle>
          <Navbar.Brand href="/">
            <img src='/tirek_logo.png' className="logo" alt="logo"/>
            <span>ТИРЕК</span>
        </Navbar.Brand>
          <a href="#" onClick={this.toggleSearchMenu.bind(this)}>
            <img src="mdi_search.svg" alt="search"/>
          </a>
          <Navbar.Collapse id="menu">
            <div className="menu-box">
							<Nav className="mr-auto">
								<Nav.Link href="/" className="map">Карта с больницами</Nav.Link>
								<Nav.Link href="/about" className="map">О нас</Nav.Link>
								<Nav.Link href="/donations" className="list">Список пожертований</Nav.Link>
								<Nav.Link href="/contact" className="contacts">Контакты</Nav.Link>
								<HelpRequest/>
							</Nav>
            </div>
						<Navbar.Toggle className="shadow" aria-controls="menu" />
          </Navbar.Collapse>
          <div className={searchMenu ? 'search-menu open' : 'search-menu close'} >
            <a href="#" className="close" onClick={this.toggleSearchMenu.bind(this)}>
              <img src="x.svg" alt="close"/>
            </a>
            <form className="form-inline search-box" onSubmit={this.updateFilterValues}>
              <input name='search' className="form-control mr-sm-2 input-search" type="text" placeholder="Поиск больницы"
                     aria-label="Search" onChange={this.onChange}/>
              <button className="search-btn" type="submit"><img src='mdi_search.svg' alt=""/></button>
            </form>
            <div className="filters-box">
              {<Select instanceId={'region-id'}
                       isClearable
                       isLoading={this.props.regionFetching}
                       placeholder={'Область'}
                       className={'dropdown'}
                       onChange={this.onRegionChange.bind(this)}
                       noOptionsMessage={this.onRegionOptionsMessage.bind(this)}
                       options={regionOptions}/>}

              {<Select instanceId={'district-id'}
                       isClearable
                       isLoading={this.props.districtFetching}
                       placeholder={'Район'}
                       value={this.state.districtValue}
                       className={'dropdown'}
                       onChange={this.onDistrictChange.bind(this)}
                       noOptionsMessage={this.onDistrictOptionsMessage.bind(this)}
                       options={districtOptions}/>}

              {<Select instanceId={'locality-id'}
                       isClearable
                       isLoading={this.props.localityFetching}
                       placeholder={'Населенный пункт'}
                       noOptionsMessage={this.onLocalityOptionsMessage.bind(this)}
                       value={this.state.localityValue}
                       className={'dropdown'}
                       onChange={this.onLocalityChange.bind(this)}
                       options={localityOptions}/>}
            </div>
          </div>
        </Navbar>
				<nav className="navbar navbar-expand-md center hide-mobile">
					<img src='/tirek_logo.png' className="logo" alt="logo"/>
					<a className="navbar-brand" href="/">ТИРЕК</a>
					<button className="navbar-toggler" type="button" data-toggle="collapse"
							data-target="#navbarCollapse"
							aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
						<span className="navbar-toggler-icon"/>
					</button>
					<form className="form-inline search-box" onSubmit={this.updateFilterValues}>
						<input name='search' className="form-control mr-sm-2 input-search" type="text" placeholder="Поиск больницы"
							   aria-label="Search" onChange={this.onChange}/>
						<button className="search-btn" type="submit"><img src='mdi_search.svg' alt=""/></button>
					</form>
					<div className="collapse navbar-collapse" id="navbarCollapse">
						<ul className="navbar-nav mr-auto">
                            <li className="nav-item">
								<Link activeClassName="active" href="/about">
									<a className="nav-link">О нас</a>
								</Link>
							</li>
							<li className="nav-item active">
								<Link activeClassName="active" href="/">
									<a className="nav-link">Карта</a>
								</Link>
							</li>
							<li className="nav-item">
								<Link activeClassName="active" href="/donations">
									<a className="nav-link">Пожертвования</a>
								</Link>

							</li>
							{/*<li className="nav-item">*/}
							{/*	<Link activeClassName="active" href="/contact">*/}
							{/*		<a className="nav-link">Контакты</a>*/}
							{/*	</Link>*/}
							{/*</li>*/}
              <li className="nav-item float-right">
                <HelpRequest/>
              </li>
						</ul>
					</div>
				</nav>
				<div className="center hide-mobile">
					<div className="row">
						<div className="filters-box">
							{<Select instanceId={'region-id'}
									 isClearable
									 isLoading={this.props.regionFetching}
									 placeholder={'Область'}
									 className={'dropdown'}
									 onChange={this.onRegionChange.bind(this)}
									 noOptionsMessage={this.onRegionOptionsMessage.bind(this)}
									 options={regionOptions}/>}

							{<Select instanceId={'district-id'}
									 isClearable
									 isLoading={this.props.districtFetching}
									 placeholder={'Район'}
									 value={this.state.districtValue}
									 className={'dropdown'}
									 onChange={this.onDistrictChange.bind(this)}
									 noOptionsMessage={this.onDistrictOptionsMessage.bind(this)}
									 options={districtOptions}/>}

							{<Select instanceId={'locality-id'}
									 isClearable
									 isLoading={this.props.localityFetching}
									 placeholder={'Населенный пункт'}
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
	fetchLocalitiesAction,
	fetchHospitalsAction
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(Header)
