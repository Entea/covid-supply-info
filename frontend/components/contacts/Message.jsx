import React, {Component, Fragment} from "react";
import PropTypes from 'prop-types';
import {Alert, Button, Form} from "react-bootstrap";
import * as _status from '../../constants/messageStatus'
import Reaptcha from "reaptcha";
import getConfig from 'next/config';

const {publicRuntimeConfig} = getConfig();

class Message extends Component {
    state = {
        fullName: "",
        phoneNumber: "",
        email: "",
        title: "",
        body: "",
        validated: false,
        verified: false,
        recaptcha: null,
    };

    onChange = (e) => {
        this.setState({
            [e.target.name]: e.target.value
        })
    };

    onSubmit = (e) => {
        const {fullName, phoneNumber, email, title, body, recaptcha} = this.state;
        const form = e.currentTarget;
        e.preventDefault();
        e.stopPropagation();
        if (form.checkValidity()) {
            this.props.sendMessage(
                {'full_name': fullName, 'phone_number': phoneNumber, email, title, body, recaptcha}
            ).then(() => {
                this.setState({
                    fullName: "",
                    phoneNumber: "",
                    email: "",
                    title: "",
                    body: "",
                    validated: false,
                    verified: false,
                    recaptcha: null
                });
                this.captcha.reset()
            });
        }
        this.setState({
            validated: true
        })
    };

    onVerify = (recaptcha) => {
        this.setState({
            verified: true,
            recaptcha
        })
    };

    render() {
        const {fullName, phoneNumber, email, title, body, verified, validated} = this.state;
        const {sending, status} = this.props;

        return (
            <Fragment>
                <h2 className='h2'>Напишите нам</h2>
                <br/><br/>
                <Form onSubmit={this.onSubmit} noValidate validated={validated}>
                    <Form.Group>
                        <Form.Label>ФИО</Form.Label>
                        <Form.Control required name="fullName" value={fullName} onChange={this.onChange}/>
                        <Form.Control.Feedback type="invalid">
                            Введите Ваше имя
                        </Form.Control.Feedback>
                    </Form.Group>

                    <Form.Group>
                        <Form.Label>Телефон</Form.Label>
                        <Form.Control required name="phoneNumber" value={phoneNumber} type='phone'
                                      onChange={this.onChange}/>
                        <Form.Control.Feedback type="invalid">
                            Введите номер телефона
                        </Form.Control.Feedback>
                    </Form.Group>

                    <Form.Group>
                        <Form.Label>Email</Form.Label>
                        <Form.Control required name="email" value={email} type='email' onChange={this.onChange}/>
                        <Form.Control.Feedback type="invalid">
                            Введите E-mail
                        </Form.Control.Feedback>
                    </Form.Group>

                    <Form.Group>
                        <Form.Label>Тема сообщения</Form.Label>
                        <Form.Control required name="title" value={title} onChange={this.onChange}/>
                        <Form.Control.Feedback type="invalid">
                            Введите тему сообщения
                        </Form.Control.Feedback>
                    </Form.Group>

                    <Form.Group>
                        <Form.Label>Сообщение</Form.Label>
                        <Form.Control required name="body" value={body} as="textarea" rows="3"
                                      onChange={this.onChange}/>
                        <Form.Control.Feedback type="invalid">
                            Введите сообщение
                        </Form.Control.Feedback>
                    </Form.Group>

                    <Form.Group>
                        <Reaptcha
                            ref={e => (this.captcha = e)}
                            sitekey={publicRuntimeConfig.recaptchaSiteKey}
                            onVerify={this.onVerify}
                        />
                    </Form.Group>
                    <Button variant="primary" type="submit" disabled={!verified || sending}>
                        Отправить
                    </Button>
                    <br/><br/>
                    {
                        status === _status.SUCCESS && <Alert variant='success'>
                            Сообщение отправлено успешно
                        </Alert>
                    }
                    {
                        status === _status.FAILURE && <Alert variant='danger'>
                            Произошла ошибка, повторите позднее
                        </Alert>
                    }
                </Form>
            </Fragment>
        );
    }
}

Message.propTypes = {
    sending: PropTypes.bool.isRequired,
    status: PropTypes.number.isRequired,
    sendMessage: PropTypes.func.isRequired
};

export default Message
