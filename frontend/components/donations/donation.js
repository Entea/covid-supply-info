import {Button, Card, Table} from "react-bootstrap";
import React, {Fragment} from "react";
import Link from "../navigation/ActiveLink";

const Donation = (props) => {
    const hideLink = !!props.hideLink;
    const item = props.donation;
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

    const map = {
        ORGANIZATION: 'Организация',
        PERSONAL: 'Частное лицо',
        DONOR: 'Донор',
        GOVERNMENT: 'Государство',
    }


    return (
        <Card>
            <Card.Body>
                <Card.Title>
                    {item.donator_name}
                </Card.Title>
                <Card.Subtitle>
                    Тип: {map[item.donator_type] || 'Неизвестно'}<br/>
                    {item.description}
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

                {!hideLink &&
                <Link href="/donations/[id]" as={`/donations/${item.id}`}>
                    <Button>Информация по распределению</Button>
                </Link>
                }
            </Card.Body>
        </Card>
    )
}

export default Donation;