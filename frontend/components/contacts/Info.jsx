import React, {Fragment} from "react";

const Info = (props) => {
    const {data} = props;
    const whatsAppFormat = (number) => {
        const oldNumber = number.replace(/\s+/g, '').replace(/-/g, '')
        const newNumber = oldNumber.indexOf('0') == 0 ? '996'+oldNumber.substring(1) : oldNumber;
        return newNumber
    };

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
                        <li key={number.value}>
                            {number.value}
                            {number.is_whats_app && <a target='_blank' className='contact__whatsapp' href={`https://wa.me/${whatsAppFormat(number.value)}`}/>}
                        </li>
                    )
                }
            </ul>

            <p>
                Email: {
                data.emails && data.emails.map(email =>
                <Fragment key={email.value} >
                    <a href={`mailto:${email.value}`}>{email.value}</a>
                    &nbsp;
                </Fragment>
                )
            }
            </p>
        </Fragment>
    )
};

export default Info
