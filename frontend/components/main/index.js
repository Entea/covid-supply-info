import React, {Component} from 'react';
import {YMaps, Map, Placemark, Clusterer} from 'react-yandex-maps';

import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'
import HelpRequest from "../helpRequest";

import {
    fetchHospitals as fetchHospitalsAction,
    fetchHospital as fetchHospitalAction,
} from '../../actions/creators/hospitals';


const mapState = {
    center: [42.870026, 74.599795],
    zoom: 12,
};

class Main extends Component {

    constructor() {
        super();
        this.state = {
            openRightBlock: true,
            rightBlockTemplate: null,
            rightBlockStatus: ''
        };
        this.closeRightBlock.bind(this);
        this.getHospitalsInfo.bind(this);
        this.setWrapperRef = this.setWrapperRef.bind(this);
    }

    componentDidMount() {
        this.props.fetchHospitalsAction().then(() => {
            this.openHospitals()
        });
    }

    setWrapperRef(node) {
        this.wrapperRef = node;
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

    placeMarkerColor(percent) {
        switch (true) {
            case (39 > percent && percent >= 0):
                return '#EB5757';
            case (85 > percent && percent >= 39):
                return '#EBCA57';
            case (percent >= 85):
                return '#27AE60';
            default:
                return '#c2c2c2';
        }
    }

    onPlacemarkClick = hospital => () => {
        this.openHospital(hospital.id);
    };

    closeRightBlock() {
        this.setState({openRightBlock: false});
        this.openHospitals();
    }

    openHospital(hospitalId) {
        this.props.fetchHospitalAction(hospitalId).then(() => {
            const rightBlockTemplate = this.getHospitalInfo();
            this.setState({openRightBlock: true, rightBlockTemplate, rightBlockStatus: 'hospitalInfo'});
        });
    }

    openHospitals() {
        const rightBlockTemplate = this.getHospitalsInfo();
        this.setState({openRightBlock: true, rightBlockTemplate, rightBlockStatus: 'hospitalListInfo'})
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
                <div
                    className="coordinate">{hospital.full_location ? hospital.full_location.lat + ', ' + hospital.full_location.lng : ''}</div>
            </div>
            <ul className="phone">
                {hospital.phone_numbers.map((item, index) => <li key={index + 'phone'}>{item.value}</li>)}
            </ul>
            <h1>Статистика по мед.учреждению</h1>
            {hospital.statistics.length === 0 ? <p>Нет данных</p> : null}
            {hospital.statistics.map((item, index) => (
                <div key={index + 's'}
                     className={'circle ' + this.needHelpStatus(item.has_capacity ? (item.actual * 100 / item.capacity) : -1)}>
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
                {hospital.needs.length === 0 ? <tr>
                    <td colSpan={4}><p className="text-center">Нет данных</p></td>
                </tr> : null}
                </tbody>
            </table>
        </div>)
    }

    render() {
        const {rightBlockStatus} = this.state;

        let hospitals = (this.props.hospitals || [])
            .map(item => {
                return {...item, lat: item['full_location'].lat, lng: item['full_location'].lng}
            })
            .filter(item => item.lat && item.lng);

        return (
            <main>
                <div className="map-box">
                    <div className="map">
                        <div className="loader"></div>
                        <YMaps>
                            <Map defaultState={mapState} width='100%' height='100%'>
                                <Clusterer
                                    options={{
                                        preset: "islands#invertedDarkBlueClusterIcons",
                                    }}
                                >
                                    {hospitals.map((hospital, index) => (
                                        <Placemark
                                            modules={["geoObject.addon.hint"]}
                                            key={index}
                                            geometry={[hospital.lat, hospital.lng]}
                                            onClick={this.onPlacemarkClick(hospital)}
                                            properties={{
                                                item: index,
                                                hintContent: hospital.name,
                                            }}
                                            options={{
                                                preset: "islands#blueMedicalCircleIcon",
                                                iconColor: this.placeMarkerColor(hospital.indicator),
                                            }}
                                        />
                                    ))}
                                </Clusterer>
                            </Map>
                        </YMaps>
                      {rightBlockStatus !== 'hospitalInfo' ?
                        <div className="only-mobile button-help-map">
                          <HelpRequest/>
                        </div> : null}
                    </div>
                    <div ref={this.setWrapperRef}
                         className={this.state.openRightBlock ? 'open right-block' : 'right-block'}>
                        <a className="close" onClick={() => this.closeRightBlock()}>
                            <img src="x.svg" alt="close"/>
                        </a>
                        <div className="only-mobile curtain"></div>
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
