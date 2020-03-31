import React, { Component } from 'react';
import { Dropdown } from 'react-bootstrap';
import Link from 'next/link';

class Header extends Component {
	state = {
		selectedPlace: {},
		region: '',
		area: '',
		city: ''
	};

	select(name, value) {
		this.setState({ [name]: value });
	}

	render() {
		const { region, area, city } = this.state;

		return (
			<header className="fixed-top">
				<nav className="navbar navbar-expand-md center">
					<img src='logo.svg' className="logo" alt="logo"/>
					<a className="navbar-brand" href="/">HELPMAP</a>
					<button className="navbar-toggler" type="button" data-toggle="collapse"
					        data-target="#navbarCollapse"
					        aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
						<span className="navbar-toggler-icon"/>
					</button>
					<form className="form-inline search-box">
						<input className="form-control mr-sm-2 input-search" type="text" placeholder="Поиск больницы"
						       aria-label="Search"/>
						<button className="search-btn" type="submit"><img src='mdi_search.svg' alt=""/></button>
					</form>
					<div className="collapse navbar-collapse" id="navbarCollapse">
						<ul className="navbar-nav mr-auto">
							<li className="nav-item active">
								<a className="nav-link active" href="/">Карта</a>
							</li>
							<li className="nav-item">
								<Link href="/donates">
									<a className="nav-link">Список пожертований</a>
								</Link>

							</li>
							<li className="nav-item">
								<a className="nav-link" href="http://test.kg/">Контакты</a>
							</li>
							<li className="nav-item float-right">
								<a className="btn btn-primary" href="http://test.kg/">ПОДАТЬ ЗАЯВКУ</a>
							</li>
						</ul>
					</div>
				</nav>
				<div className="center">
					<div className="row">
						<div className="filters-box">
							<Dropdown>
								<Dropdown.Toggle id="dropdown-basic">
									{ region !== '' ? region : 'Область' }
								</Dropdown.Toggle>
								<Dropdown.Menu>
									<Dropdown.Item
										onClick={ () => this.select('region', 'Чуйская') }>Чуйская</Dropdown.Item>
									<Dropdown.Item
										onClick={ () => this.select('region', 'Баткенская') }>Баткенская</Dropdown.Item>
									<Dropdown.Item onClick={ () => this.select('region', 'Something else') }>Something
										else</Dropdown.Item>
								</Dropdown.Menu>
							</Dropdown>
							<Dropdown>
								<Dropdown.Toggle id="dropdown-basic">
									{ city !== '' ? city : 'Город' }
								</Dropdown.Toggle>
								<Dropdown.Menu>
									<Dropdown.Item
										onClick={ () => this.select('city', 'Бишкек') }>Бишкек</Dropdown.Item>
									<Dropdown.Item onClick={ () => this.select('city', 'Кант') }>Кант</Dropdown.Item>
									<Dropdown.Item onClick={ () => this.select('city', 'Something else') }>Something
										else</Dropdown.Item>
								</Dropdown.Menu>
							</Dropdown>
							<Dropdown>
								<Dropdown.Toggle id="dropdown-basic">
									{ area !== '' ? area : 'Район' }
								</Dropdown.Toggle>
								<Dropdown.Menu>
									<Dropdown.Item
										onClick={ () => this.select('area', 'Октябрьский') }>Октябрьский</Dropdown.Item>
									<Dropdown.Item
										onClick={ () => this.select('area', 'Ленинский') }>Ленинский</Dropdown.Item>
									<Dropdown.Item onClick={ () => this.select('area', 'Something else') }>Something
										else</Dropdown.Item>
								</Dropdown.Menu>
							</Dropdown>
						</div>
					</div>
				</div>
			</header>
		);
	}
}

export default Header;
