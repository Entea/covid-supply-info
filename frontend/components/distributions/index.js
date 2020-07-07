import React, {Component} from 'react';
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'
import Donation from '../donations/donation'
import Distribution from './distribution'
import {Alert, Col, Container, Row, Spinner} from 'react-bootstrap'
import {fetchDistributions} from '../../actions/creators/distributions'
import {fetchDonation} from '../../actions/creators/donations'
import Link from "next/link";


class DistributionsComponent extends Component {
    componentDidMount() {
        this.props.fetchDistributions(this.props.id);
        this.props.fetchDonation(this.props.id);
    }

    render() {
        const {fetching, donationFetching, results, donation} = this.props;
        return (
            <main>
                <Container>
                    <Row style={{marginTop: 150}}>
                        <Col>
                            <Link href='/donations'><a>&lt;&lt; Назад к списку</a></Link>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <h2 className='h2'>Информация о пожертвовании</h2>
                            {
                                donationFetching ? (<div className="loader"></div>) :
                                    <Donation hideLink={true} donation={donation}/>
                            }
                        </Col>
                    </Row>


                    <Row style={{marginTop: 20}}>
                        <Col>
                            <h2 className='h2'>Информация по распределению</h2>
                            {
                                !fetching && results.length > 0 &&
                                results.map(item => (
                                    <div key={item.id}>
                                        <Distribution item={item}/>
                                        <br/>
                                    </div>
                                ))
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
        fetching: state.distributions.fetching,
        results: state.distributions.results,
        donation: state.donations.single,
        donationFetching: state.donations.fetching,
    }
};

const mapDispatchToProps = (dispatch) => bindActionCreators({fetchDistributions, fetchDonation}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(DistributionsComponent)
