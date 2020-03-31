import React, {Component} from 'react';
import Layout from '../components/layout/Layout';
import { Button, Col, Container, Form, FormControl, InputGroup, Row } from 'react-bootstrap'

class Contact extends Component {
    render() {
        return (
            <Layout>
                <main className='contact'>
                    <Container>
                        <Row style={{ marginTop: 150 }}>
                            <Col xl={6} lg={6} md={6} sm={12} xs={12}>
                                <h1 className='h2'>Контакты</h1>
                                <br/><br/>
                                <p>
                                    По всем вопросам вы можете с нами связаться по ТЕЛЕФОНАМ:
                                    <ul className={'contact__phones'}>
                                        <li>
                                            0700 00 00 00
                                            <a className='contact__whatsapp' href="whatsapp://x"/>
                                        </li>
                                        <li>
                                            0700 00 00 00
                                        </li>
                                        <li>
                                            0700 00 00 00
                                        </li>
                                    </ul>
                                </p>
                                <p>Email: <a href="mailto:aaronson@gmail.com">aaronson@gmail.com</a></p>
                            </Col>
                            <Col xl={6} lg={6} md={6} sm={12} xs={12}>
                                <h2 className='h2'>Напишите нам</h2>
                                <br/><br/>
                                <Form>
                                    <Form.Group>
                                        <Form.Label>ФИО</Form.Label>
                                        <Form.Control />
                                    </Form.Group>

                                    <Form.Group>
                                        <Form.Label>Телефон</Form.Label>
                                        <Form.Control />
                                    </Form.Group>

                                    <Form.Group>
                                        <Form.Label>Email</Form.Label>
                                        <Form.Control type='email' />
                                    </Form.Group>

                                    <Form.Group>
                                        <Form.Label>Тема сообщения</Form.Label>
                                        <Form.Control />
                                    </Form.Group>

                                    <Form.Group>
                                        <Form.Label>Сообщение</Form.Label>
                                        <Form.Control as="textarea" rows="3" />
                                    </Form.Group>
                                    <Button variant="primary" type="submit">
                                        Отправить
                                    </Button>
                                </Form>
                            </Col>
                        </Row>
                    </Container>
                </main>
            </Layout>
        );
    }
}

export default Contact
