import React, {Fragment} from "react";

const Info = (props) => {
    const {data} = props;
    return (
        <Fragment>
            <h1 className='h2'>Контакты</h1>
            <br/><br/>
            <p>
                {data.text_ru}:
            </p>
            <ul className={'contact__phones'}>
                {
                    data.phone_numbers && data.phone_numbers.map(number =>
                        <li>
                            {number}
                        </li>
                    )
                }
            </ul>

            <p>
                Email: {
                data.emails && data.emails.map(email => <a href={`mailto:${email}`}>{email}</a>)
            }
            </p>
        </Fragment>
    )
};

export default Info