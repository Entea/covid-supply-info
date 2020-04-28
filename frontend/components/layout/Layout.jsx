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
                    <title>{'COVID 19'}</title>
                    <link rel="icon" href="/tirek_logo.png"/>
                </Head>
                <Header onFilterChange={this.updateFilterValues.bind(this)}/>
                {children}
            </div>
        );
    }
}

export default Layout;
