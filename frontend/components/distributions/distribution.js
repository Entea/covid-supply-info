import {Card, Table} from "react-bootstrap";
import React, {Fragment} from "react";

const Distribution = (props) => {
    const item = props.item;
    const details = (item.details || []).map(detail => {
        const key = `${item.id} ${detail.id}`
        return (
            <tr key={key}>
                <td>
                    <Fragment>
                        <span>{detail.need_type.name}</span>
                    </Fragment>
                </td>
                <td>
                    <Fragment>
                        <span>{detail.amount} {detail.need_type.measure.name}</span>
                    </Fragment>
                </td>
            </tr>
        )
    });

    return (
        <Card>
            <Card.Body>
                <Card.Title>
                    {item.hospital.name}
                </Card.Title>
                <Card.Subtitle>
                    Получено: {item.receiver} {item.distributed_at}
                </Card.Subtitle>

                <Table hover responsive>
                    <thead>
                    <tr>
                        <th>Наименование</th>
                        <th>Кол-во</th>
                    </tr>
                    </thead>
                    <tbody>
                    {details}
                    </tbody>
                </Table>
            </Card.Body>
        </Card>
    )
}

export default Distribution;