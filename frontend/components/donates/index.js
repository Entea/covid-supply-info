import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import {
    fetchDonates as fetchDonatesAction,
} from '../../actions/creators/donates'

import {Table} from 'react-bootstrap'
class DonatesContainer extends Component {
    componentDidMount() {
      this.props.fetchDonatesAction();
    }
    render() {
        const { fetching, donates } = this.props;
        return (
            <main>
                <div className='container'>
                    <div className='row' style={{marginTop:150}}>
                        <h3>Пожертвования</h3>
                        <Table striped bordered hover size="sm">
                            <thead>
                            <tr>
                                <th>#</th>
                                <th>Имя</th>
                                <th>Тип</th>
                                <th>Описание</th>
                                <th>Детали</th>
                            </tr>
                            </thead>
                            <tbody>
                            {
                                fetching ? 'Загрузка...' :
                                    donates.length > 0 ?
                                donates.map( item => (
                                <tr>
                                    <td>{item.id}</td>
                                    <td>{item.donator_name}</td>
                                    <td>{item.donator_type}</td>
                                    <td>{item.description}</td>
                                    <td>{item.details.map( detail =>(
                                        <Fragment>
                                            <span>{detail.need_type.name } - {detail.amount} {detail.need_type.measure.name }</span>
                                            <br/>
                                        </Fragment>
                                    ))}</td>
                                </tr>
                            )):''}
                            </tbody>
                        </Table>

                    </div>
                </div>
            </main>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        fetching: state.donations.fetching,
        donates: state.donations.results
    }
};

const mapDispatchToProps = (dispatch) => bindActionCreators({
    fetchDonatesAction,
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(DonatesContainer)
