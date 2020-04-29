import React from 'react';
import Head from 'next/head';
import Header from './Header';

class Layout extends React.Component {

    constructor(props) {
        super(props);
    }

    updateFilterValues(regionId, districtId, localityId) {
        this.props.onFilterValuesChange(regionId, districtId, localityId);
    }

    render() {
        const {children} = this.props;

        return (
            <div className='layout'>
                <Head>
                    <title>{'Тирек'}</title>
                    <link rel="icon" href="/favicon.ico"/>
                </Head>
                <Header onFilterChange={this.updateFilterValues.bind(this)}/>
                {children}
            </div>
        );
    }
}

export default Layout;
