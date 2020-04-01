import React, {Component} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {
    fetchContacts as fetchContactsAction,
    sendMessage as sendMessageAction,
    init as initAction
} from '../../actions/creators/contacts';
import {Col, Container, Row} from 'react-bootstrap'
import Info from "./Info";
import Message from "./Message";

class Contacts extends Component {
    componentDidMount() {
        this.props.fetchContactsAction();
        this.props.initAction();
    }

    render() {
        const {data, sending, status, sendMessageAction} = this.props;

        return (
            <main className='contact'>
                <Container>
                    <Row style={{marginTop: 150}}>
                        <Col xl={6} lg={6} md={6} sm={12} xs={12}>
                            <Info data={data}/>
                        </Col>
                        <Col xl={6} lg={6} md={6} sm={12} xs={12}>
                            <Message
                                sending={sending}
                                status={status}
                                sendMessage={sendMessageAction}
                            />
                        </Col>
                    </Row>
                </Container>
            </main>
        );
    }
}


const mapStateToProps = (state) => {
    return {
        sending: state.contacts.sending,
        status: state.contacts.status,
        data: state.contacts.data,
    }
};

const mapDispatchToProps = (dispatch) => bindActionCreators({
    fetchContactsAction,
    sendMessageAction,
    initAction
}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(Contacts)