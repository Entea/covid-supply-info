import React, {Fragment} from "react";
import { Col, Row, Container } from 'react-bootstrap'

const Block = (props) => {
    const className = props.className ? props.className : 'about__block';
    const filledClassName = props.filled ? `about__block_filled` : ''
    return (
        <div className={filledClassName}>
            <Container>
                <Row>
                    <Col xs className={className}>
                    {props.children}
                    </Col>
                </Row>
            </Container>
        </div>
    );
}
export default Block;