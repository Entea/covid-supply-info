import React from 'react';
import Layout from '../components/layout/Layout';
import DonationsComponent from '../components/donations'

const Donations = (props) => (
    <Layout>
        <DonationsComponent id={props.id}/>
    </Layout>
);

Donations.getInitialProps = ({ query }) => {
    let data = {};
    if (query.id) {
        data.id = query.id;
    }

    return data;
}

export default Donations;