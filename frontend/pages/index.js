import React, {Component} from 'react';
import Layout from '../components/layout/Layout';
import MainComponent from '../components/main'

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
