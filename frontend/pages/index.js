import React, {Component} from 'react';
import Layout from '../components/layout/Layout';
import dynamic from 'next/dynamic'

const MainComponent = dynamic(() => import('../components/main'), {ssr: false});

class Home extends Component {
    render() {
        return (
            <Layout>
                <MainComponent/>
            </Layout>
        );
    }
}

export default Home
