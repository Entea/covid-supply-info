import React, {Fragment} from "react";
import { Col, Row } from 'react-bootstrap'

const BlockHeader = (props) => {
    return (
        <Row className="justify-content-md-center">
            <Col md="auto" className="about__block_header">
                {props.children}

            </Col>
        </Row>
    );
}
export default BlockHeader;