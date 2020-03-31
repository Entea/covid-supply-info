import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { Alert, Col, Container, Row, Spinner, Table } from 'react-bootstrap'
import {
	fetchDonations as fetchDonationsAction,
} from '../../actions/creators/donations'

class Donations extends Component {
	componentDidMount() {
		this.props.fetchDonationsAction();
	}

	render() {
		const { fetching, results } = this.props;
		return (
			<main>
				<Container>
					<Row style={{ marginTop: 150 }}>
						<Col xs={12}>
							<h3 className='h3'>Пожертвования</h3>
						</Col>
						<Col xs={12}>
							{
								fetching && <Spinner animation="border" role="status">
									<span className="sr-only">Loading...</span>
								</Spinner>
							}
							{
								!fetching && results.length > 0 ?
									<Table bordered hover size="sm">
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
											results.map(item => (
												<tr>
													<td>{item.id}</td>
													<td>{item.donator_name}</td>
													<td>{item.donator_type}</td>
													<td>{item.description}</td>
													<td>{item.details.map(detail => (
														<Fragment>
															<span>{detail.need_type.name} - {detail.amount} {detail.need_type.measure.name}</span>
															<br/>
														</Fragment>
													))}</td>
												</tr>
											))
										}
										</tbody>
									</Table>
									:
									<Alert variant='danger'>
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