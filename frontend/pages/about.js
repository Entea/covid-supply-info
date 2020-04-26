import React, {Component} from 'react';
import Layout from '../components/layout/Layout';
import AboutComponent from '../components/about';

class About extends Component {
    render() {
        return (
            <Layout>
                <AboutComponent/>
            </Layout>
        );
    }
}

export default About
