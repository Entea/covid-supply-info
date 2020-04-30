import React, {Component} from 'react';
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'
import Donation from './donation'
import {Alert, Col, Container, Row, Spinner} from 'react-bootstrap'
import {fetchDonations as fetchDonationsAction,} from '../../actions/creators/donations'

class Donations extends Component {
    componentDidMount() {
        this.props.fetchDonationsAction();
    }

    render() {
        const {fetching, results} = this.props;

        return (
            <main>

                <Container>
                    <Row style={{marginTop: 150}}>
                        <Col xs={12}>
                            <h3 className='h3'>Список пожертвований</h3>
                        </Col>
                        <Col xs={12}>
                            {
                                fetching && <div className="loader"></div>
                            }
                            {
                                !fetching && results.length > 0 &&
                                results.map(item =>
                                    <div key={item.id}>
                                        <Donation donation={item}/>
                                        <br/>
                                    </div>
                                )
                            }
                            {
                                !fetching && !results.length && <Alert variant='danger'>
                                    Нет данных
                                </Alert>
                            }
                        </Col>
                    </Row>
                </Container>
            </main>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        fetching: state.donations.fetching,
        results: state.donations.results
    }
};

const mapDispatchToProps = (dispatch) => bindActionCreators({
    fetchDonationsAction,
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(Donations)
