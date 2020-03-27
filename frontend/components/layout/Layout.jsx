import React from 'react';
import Head from 'next/head';
import Header from './Header';

class Layout extends React.Component {
	render() {
		const { children } = this.props;

		return (
			<div className='layout'>
				<Head>
					<title>COVID 19</title>
					<link rel="icon" href="/favicon.ico"/>
				</Head>
				<Header/>
				{ children }
			</div>
		);
	}
}

export default Layout;