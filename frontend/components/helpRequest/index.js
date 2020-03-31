import React, {Fragment} from 'react';
import {Button, FormControl, InputGroup, Modal, Form, Toast} from "react-bootstrap";
import {bindActionCreators} from "redux";
import {fetchRegions as fetchRequestRegionsAction} from "../../actions/creators/regions";
import {fetchDistricts as fetchRequestDistrictsAction} from "../../actions/creators/districts";
import {fetchLocalities as fetchRequestLocalitiesAction} from "../../actions/creators/localities";
import {createRequest as createRequestAction} from "../../actions/creators/requests";
import {connect} from "react-redux";
import Select from "react-select";
import Reaptcha from "reaptcha";
import getConfig from 'next/config';

const {publicRuntimeConfig} = getConfig();

const inputStyle = {
    marginLeft: 8,
    marginRight: 8,
};

const defaultState = {
    visible: false,
    firstName: '',
    firstNameError: false,
    lastName: '',
    lastNameError: false,
    position: '',
    positionError: false,
    hospitalName: '',
    hospitalNameError: false,
    phoneNumber: '',
    phoneNumberError: false,
    description: '',
    districts: [],
    localities: [],
    regionValue: null,
    districtValue: null,
    localityValue: null,
    localityValueError: false,
    resultModal: false,
    verified: false
}

class HelpRequest extends React.Component {
    state = {
        ...defaultState
    };

    handleInputChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value,
            [e.target.name + 'Error']: false
        })
    }
    handleSubmit = (e) => {
        e.preventDefault();
        const {
            firstName, lastName, verified,
            hospitalName, phoneNumber, position, localityValue, description
        } = this.state;
        this.setState({
            lastNameError: lastName === '',
            firstNameError: firstName === '',
            positionError: position === '',
            hospitalNameError: hospitalName === '',
            phoneNumberError: phoneNumber === '',
            localityValueError: localityValue === null,
        });
        firstName !== '' &&
        lastName !== '' &&
        position !== '' &&
        hospitalName !== '' &&
        phoneNumber !== '' &&
        localityValue !== null &&
        verified &&
        this.props.createRequestAction({
            first_name: firstName,
            last_name: lastName,
            position,
            hospital_name: hospitalName,
            phone_number: phoneNumber,
            locality_id: localityValue.value,
            description
        }).then(() => this.hideModal()).then(() => this.showResultModal(true))
    }
    hideModal = () => {
        this.setState({
            ...defaultState
        })
    };
    showModal = () => {
        this.setState({
            visible: true
        })
    };

    componentDidMount() {
        this.props.fetchRequestRegionsAction();
    };

    onRegionChange(region) {
        if (region) {
            this.props.fetchRequestDistrictsAction(region.value).then(() => this.setState({districts: this.props.districts}));

            this.setState({regionValue: region, districtValue: null, localityValue: null});
        } else {
            this.setState({
                districts: [],
                regionValue: null,
                districtValue: null,
                localityValue: null
            })
        }
    };

    onDistrictChange(district) {
        if (district) {
            this.props.fetchRequestLocalitiesAction(district.value).then(() => this.setState({localities: this.props.localities}));

            this.setState({districtValue: district});
        } else {
            this.setState({localities: [], districtValue: null, localityValue: null})
        }
    };

    onLocalityChange(locality) {
        if (locality) {
            this.setState({localityValue: locality, localityValueError: false});
        } else {
            this.setState({localityValue: null, localityValueError: true});
        }
    };

    regionOptionsMessage() {
        return 'Область';
    };

    districtOptionsMessage() {
        return 'Район';
    };

    localityOptionsMessage() {
        return 'Город';
    };

    showResultModal = (resultModal) => {
        this.setState({
            resultModal
        })
    }
    onVerify = recaptchaResponse => {
        this.setState({
            verified: true
        });
    };

    render() {
        const {regions} = this.props;
        const {localities, districts} = this.state;

        const {
            visible, firstName, lastName, description, verified,
            hospitalName, phoneNumber, position, firstNameError, localityValueError,
            lastNameError, hospitalNameError, phoneNumberError, positionError, resultModal
        } = this.state;
        const regionOptions = (regions || []).map((region, index) => {
            return {value: region.id, label: region.name};
        });
        const districtOptions = (districts || []).map((district, index) => {
            return {value: district.id, label: district.name};
        });

        const localityOptions = (localities || []).map((locality, index) => {
            return {value: locality.id, label: locality.name};
        });
        const errorStyle = {
            control: base => ({
                ...base,
                borderColor: 'red',
                boxShadow: 'none',
                '&:hover': {
                    borderColor: 'red',
                },
            })
        };
        return (
            <Fragment>

                <Modal
                    onHide={this.hideModal}
                    animation={true}
                    show={visible}
                    size="md"
                    aria-labelledby="contained-modal-title-vcenter"
                    centered
                >
                    <Modal.Header closeButton>
                        <Modal.Title id="contained-modal-title-vcenter">
                            Форма заявки для больниц и врачей
                        </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form>
                            <InputGroup className="mb-3">
                                <FormControl
                                    isInvalid={firstNameError}
                                    onChange={this.handleInputChange}
                                    placeholder="Имя"
                                    value={firstName}
                                    name='firstName'
                                    style={inputStyle}/>
                                <FormControl
                                    isInvalid={lastNameError}
                                    onChange={this.handleInputChange}
                                    value={lastName}
                                    name='lastName'
                                    placeholder="Фамилия"
                                    aria-label="last_name"
                                    style={inputStyle}/>
                            </InputGroup>
                            <InputGroup className="mb-3">
                                <FormControl
                                    isInvalid={positionError}
                                    onChange={this.handleInputChange}
                                    value={position}
                                    placeholder="Должность"
                                    name="position"
                                    style={inputStyle}/>
                            </InputGroup>
                            <div className="mb-3"
                                 style={inputStyle}
                            >
                                <Select instanceId={'region-id'}
                                        isClearable
                                        isLoading={this.props.regionFetching}
                                        placeholder={'Область'}
                                        className={'dropdown'}
                                        onChange={this.onRegionChange.bind(this)}
                                        noOptionsMessage={this.regionOptionsMessage.bind(this)}
                                        options={regionOptions}

                                />
                            </div>
                            <div className="mb-3"
                                 style={inputStyle}
                            >
                                <Select instanceId={'district-id'}
                                        isClearable
                                        isLoading={this.props.districtFetching}
                                        placeholder={'Район'}
                                        value={this.state.districtValue}
                                        className={'dropdown'}
                                        onChange={this.onDistrictChange.bind(this)}
                                        noOptionsMessage={this.districtOptionsMessage.bind(this)}
                                        options={districtOptions}/>
                            </div>
                            <div className="mb-3"
                                 style={inputStyle}
                            >
                                <Select instanceId={'locality-id'}
                                        styles={localityValueError ? errorStyle : ''}
                                        isClearable
                                        isLoading={this.props.localityFetching}
                                        placeholder={'Город'}
                                        noOptionsMessage={this.localityOptionsMessage.bind(this)}
                                        value={this.state.localityValue}
                                        className={'dropdown'}
                                        onChange={this.onLocalityChange.bind(this)}
                                        options={localityOptions}/>
                            </div>
                            <InputGroup className="mb-3">
                                <FormControl
                                    isInvalid={hospitalNameError}
                                    value={hospitalName}
                                    onChange={this.handleInputChange}
                                    placeholder="Больница"
                                    name="hospitalName"
                                    style={inputStyle}
                                />
                            </InputGroup>
                            <InputGroup className="mb-3">
                                <FormControl
                                    isInvalid={phoneNumberError}
                                    value={phoneNumber}
                                    type='phone'
                                    onChange={this.handleInputChange}
                                    placeholder="Номер телефона"
                                    name="phoneNumber"
                                    style={inputStyle}
                                />
                            </InputGroup>
                            <InputGroup className="mb-3">
                                <FormControl
                                    onChange={this.handleInputChange}
                                    rows="5"
                                    as='textarea'
                                    value={description}
                                    placeholder="Какая вам нужна помощь ?"
                                    name="description"
                                    style={inputStyle}
                                />
                            </InputGroup>
                            <InputGroup className="recaptcha-container">
                                <Reaptcha
                                    sitekey={publicRuntimeConfig.recaptchaSiteKey}
                                    onVerify={this.onVerify}
                                />
                            </InputGroup>
                            <InputGroup>
                                <Button variant={'info'} onClick={this.handleSubmit}
                                        style={{marginLeft: 8, marginRight: 8, width: '100%'}}>Отправить</Button>
                            </InputGroup>

                        </Form>
                    </Modal.Body>
                </Modal>
                <li className="nav-item float-right">
                    <Button variant={'primary'} onClick={this.showModal}>ПОДАТЬ ЗАЯВКУ</Button>
                </li>

                <Modal
                    onHide={() => this.showResultModal(false)}
                    animation={true}
                    show={resultModal}
                    size="sm"
                    aria-labelledby="contained-modal-title-vcenter"
                    centered
                >
                    <Modal.Body>
                        <p>Заявка успешно подана</p>
                    </Modal.Body>
                </Modal>
            </Fragment>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        regionFetching: state.requests.regionFetching,
        regions: state.requests.regions,
        districtFetching: state.requests.districtFetching,
        districts: state.requests.districts,
        localityFetching: state.requests.localityFetching,
        localities: state.requests.localities,
    }
};

const mapDispatchToProps = (dispatch) => bindActionCreators({
    fetchRequestRegionsAction,
    fetchRequestDistrictsAction,
    fetchRequestLocalitiesAction,
    createRequestAction,
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(HelpRequest)