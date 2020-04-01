import React, { Component } from 'react';
import GoogleMapReact from 'google-map-react';
import getConfig from 'next/config';
const { publicRuntimeConfig } = getConfig();

import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import {
  fetchHospitals as fetchHospitalsAction,
  fetchHospital as fetchHospitalAction,
} from '../../actions/creators/hospitals';

class Main extends Component {
	static defaultProps = {
		center: {
			lat: 41.822475,
			lng: 74.754128
		},
		zoom: 7,
	};
  constructor() {
    super();
    this.state = {
      openRightBlock: true,
      rightBlockTemplate: null
    }
    this.closeRightBlock.bind(this);
    this.getHospitalsInfo.bind(this);
    this.setWrapperRef = this.setWrapperRef.bind(this);
    this.handleClickOutside = this.handleClickOutside.bind(this);
  }

  componentDidMount() {
    this.props.fetchHospitalsAction().then(() => {
      this.openHospitals()
    });
    document.addEventListener('mousedown', this.handleClickOutside);
  }

  componentWillUnmount() {
    document.removeEventListener('mousedown', this.handleClickOutside);
  }

  setWrapperRef(node) {
    this.wrapperRef = node;
  }

  handleClickOutside(event) {
    if (this.wrapperRef && !this.wrapperRef.contains(event.target) && this.state.openRightBlock && event.target.className.indexOf('circle') === -1) {
      this.closeRightBlock();
    }
  }

  needHelpStatus(percent) {
    switch (percent) {
      case (39 < percent && percent > 0):
        return 'danger';
      case (85 < percent && percent > 39):
        return 'warning';
      default:
        return '';
    }
  }

  closeRightBlock() {
    this.setState({openRightBlock: false, rightBlockTemplate: null});
  }

  openHospital(m, props) {
    this.props.fetchHospitalAction(props.id).then(() => {
      this.state.rightBlockTemplate = this.getHospitalInfo();
      this.setState({openRightBlock: true})
    });
  }

  openHospitals() {
    this.state.rightBlockTemplate = this.getHospitalsInfo();
    this.setState({openRightBlock: true})
  }

  getHospitalsInfo() {
    const {hospitals} = this.props;
    return (<table key={hospitals} className="hospital-list">
              <thead>
              <tr>
                <th className="title">Больница</th>
                <th className="title">Уровень помощи</th>
              </tr>
              </thead>
              <tbody>
              {hospitals.map((item, index) =>
                (<tr key={index}>
                  <td>
                    {item.name}
                  </td>
                  <td>
                    <div className={'circle ' + this.needHelpStatus(item.request_amount)}/>
                    <div className="percentage">
                      {item.request_amount ? item.request_amount : 0}%
                    </div>
                  </td>
                </tr>))}
              </tbody>
            </table>)
  }

  getHospitalInfo() {
    const {hospital} = this.props;
    return (<div className="hospital-box">
      <h1>{hospital.name}</h1>
      <div className="address">
        {hospital.address}
        <div className="coordinate">{hospital.full_location ?  hospital.full_location.lat + ', ' +  hospital.full_location.lng : ''}</div>
      </div>
      <ul className="phone">
        {hospital.phone_numbers.map((item, index) => <li key={index + 'phone'}>{item.value}</li>)}
      </ul>
      <h1>Статистика по мед.учреждению</h1>
      {hospital.statistics.length === 0 ? <p>Нет данных</p> : null}
      {hospital.statistics.map((item, index) => (
        <div key={index + 's'} className="circle">
          <div className="name">{item.category}</div>
          <div className="count">{item.has_capacity ? item.actual + '/' + item.capacity : item.actual}</div>
        </div>
      ))}
      <h1>Продукция по спецодежде и оборудованию в больнице…</h1>
      <table>
        <thead>
        <tr>
          <th>Название</th>
          <th>Наличие</th>
          <th>Потребности</th>
          <th>Не хватает</th>
        </tr>
        </thead>
        <tbody>
        {hospital.needs.map((item, index) => (
          <tr key={index + 'n'}>
            <td>
              {index + 1}.{item.need_type ? item.need_type.name : ''}
            </td>
            <td>
              {item.reserve_amount}
            </td>
            <td>
              {item.request_amount}
            </td>
            <td>
              {item.request_amount - item.reserve_amount}
            </td>
          </tr>
        ))}
        {hospital.needs.length === 0 ? <tr><td colSpan={4}><p classsName="text-center">Нет данных</p></td></tr>: null}
        </tbody>
      </table>
    </div>)
  }

render() {
  const Mark = ({ name, percent }) => <div className="circle-mark">
    <div className={'circle ' + this.needHelpStatus(percent)} />
    <div className="name">{name}</div>
  </div>;

  let marks = (this.props.hospitals || [])
    .filter(item => item['full_location'].lat && item['full_location'].lng)
    .map((item, index) => (<Mark
      key={index + 'm'}
      lat={item['full_location'].lat}
      lng={item['full_location'].lng}
      name={item.name}
      id={item.id}
      percent={item.request_amount}
    />));

		return (
			<main>
				<div style={ { height: '100vh', width: '100%' } }>
          <GoogleMapReact
						bootstrapURLKeys={ { key: publicRuntimeConfig.mapKey } }
						defaultCenter={this.props.center}
						defaultZoom={this.props.zoom}
            onChildClick={this.openHospital.bind(this)}>
            {marks}
					</GoogleMapReact>
          <div ref={this.setWrapperRef} className={ this.state.openRightBlock ? 'open right-block' : 'right-block'}>
            <a className="close" onClick={() => this.closeRightBlock()}>
              <img src="x.svg" alt="close"/>
            </a>
            {this.state.rightBlockTemplate}
          </div>
       </div>
			</main>
		);
	}
}

const mapStateToProps = (state) => {
  return {
    hospitals: state.hospitals.results,
    hospital: state.hospitals.single
  }
};

const mapDispatchToProps = (dispatch) => bindActionCreators({
  fetchHospitalsAction,
  fetchHospitalAction,
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(Main);
