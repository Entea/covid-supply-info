import React, {Component} from 'react';
import Layout from '../components/layout/Layout';
import ContactsComponent from '../components/contacts';

class Contacts extends Component {
    render() {
        return (
            <Layout>
                <ContactsComponent/>
            </Layout>
        );
    }
}

export default Contacts
