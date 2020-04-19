import React, {Component} from 'react';
import {YMaps, Map, Placemark} from 'react-yandex-maps';

import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import {
  fetchHospitals as fetchHospitalsAction,
  fetchHospital as fetchHospitalAction,
} from '../../actions/creators/hospitals';

class Main extends Component {
  static defaultProps = {
    center: [42.870026, 74.599795],
    zoom: 12,
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
    switch (true) {
      case (39 > percent && percent >= 0):
        return 'danger';
      case (85 > percent && percent >= 39):
        return 'warning';
      case (percent >= 85):
        return 'success';
      default:
        return percent;
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
                    <div className={'circle ' + this.needHelpStatus(item.indicator)}/>
                    <div className="percentage">
                      {item.indicator > 0 ? item.indicator + '%' : <span>Нет данных</span>}
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
        <div key={index + 's'} className={'circle ' + this.needHelpStatus(item.has_capacity ? (item.actual * 100 / item.capacity) : -1)}>
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
    let marks = (this.props.hospitals || [])
      .filter(item => item['full_location'].lat && item['full_location'].lng)
      .map((item, index) => {
        return (
            <Placemark 
                key={index + 'm'} 
                geometry={[item['full_location'].lat, item['full_location'].lng]}
                options={{hint: item['name']}}
            />
        )
      });

    const center = Main.defaultProps.center;
    const zoom = Main.defaultProps.zoom;

	return (
      <main>
        <div style={ { height: '100vh', width: '100%' } }>
          <YMaps>
            <Map defaultState={{center: center, zoom: zoom}} width='100%' height='100%'>
              {marks}
            </Map>
          </YMaps>

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
