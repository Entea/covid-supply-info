import React, {Fragment} from "react";
import { Col, Row } from 'react-bootstrap'

const BlockHeader = (props) => {
    return (
        <Row className="justify-content-xs-center">
            <Col xs="auto" className="about__block_header">
                {props.children}

            </Col>
        </Row>
    );
}
export default BlockHeader;