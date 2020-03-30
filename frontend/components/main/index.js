import React, { Component } from 'react';
import GoogleMapReact from 'google-map-react';
import getConfig from 'next/config';
import { connect } from 'react-redux';

const { publicRuntimeConfig } = getConfig();

class Main extends Component {
	static defaultProps = {
		center: {
			lat: 41.822475,
			lng: 74.754128
		},
		zoom: 7,
	};

	render() {
		const Mark = ({ name }) => <div className="circle-mark">
			<div className="circle"/>
			<div className="name">{name}</div>
		</div>;

		let marks = (this.props.hospitals || [])
			.filter(item => item['full_location'].lat && item['full_location'].lng)
			.map((item, index) => (<Mark
				key={index + 'm'}
				lat={item['full_location'].lat}
				lng={item['full_location'].lng}
				name={item.name}
			/>));

		return (
			<main>
				<div style={{ height: '100vh', width: '100%' }}>
					<GoogleMapReact
						bootstrapURLKeys={{ key: publicRuntimeConfig.mapKey }}
						defaultCenter={this.props.center}
						defaultZoom={this.props.zoom}>
						{marks}
					</GoogleMapReact>
				</div>
			</main>
		);
	}
}

const mapStateToProps = (state) => {
	return {
		fetching: state.hospitals.fetching,
		hospitals: state.hospitals.results
	}
};

export default connect(mapStateToProps, null)(Main)
