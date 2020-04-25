import React from 'react';
import Layout from '../../components/layout/Layout';
import DistributionsComponent from '../../components/distributions'

const Distributions = (props) => {
    return (
        <Layout>
            <DistributionsComponent id={props.id} />
        </Layout>
    );
}

Distributions.getInitialProps = ({ query }) => {
    let data = {};
    if (query.id) {
        data.id = query.id;
    }

    return data;
}

export default Distributions;