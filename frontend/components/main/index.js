import React, {Component, Fragment} from 'react';
import GoogleMapReact from 'google-map-react';
import getConfig from 'next/config';
const { publicRuntimeConfig } = getConfig();

import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import {
  fetchHospitals as fetchHospitalsAction,
} from '../../actions/creators/hospitals'


class Main extends Component {

  componentDidMount() {
    this.props.fetchHospitalsAction();
  }

	render() {
    const { fetching, hospitals } = this.props;

    const Mark = ({name}) => <div className="circle-mark"><div className="circle"/><div className="name">{name}</div></div>;
    let Marks = [];
    hospitals.forEach((item, index) => {
      if (item.full_location.latitude && item.full_location.longitude) {
        Marks.push(<Mark
          key={index + 'm'}
          lat={ item.full_location.longitude }
          lng={ item.full_location.latitude }
          name={item.name}
        />)
      }

    })
		return (
			<main>
				<div style={ { height: '100vh', width: '100%' } }>
          {Marks.length !==0 ? <GoogleMapReact
						bootstrapURLKeys={ { key: publicRuntimeConfig.mapKey } }
						defaultCenter={ { lat: 41.822475, lng: 74.754128 } }
						defaultZoom={ 7 }
					>
            {Marks.map((item) => item)}
					</GoogleMapReact> : null}
				</div>
			</main>
		);
  }
};

const mapStateToProps = (state) => {
  return {
    fetching: state.hospitals.fetching,
    hospitals: state.hospitals.results
  }
};

const mapDispatchToProps = (dispatch) => bindActionCreators({
  fetchHospitalsAction,
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(Main)
