import React from 'react';
import GoogleMapReact from 'google-map-react';

const AnyReactComponent = ({ text }) => <div>{ text }</div>;

const Main = () => {
	return (
		<main>
			<div style={ { height: '100vh', width: '100%' } }>
				<GoogleMapReact
					bootstrapURLKeys={ { key: 'AIzaSyAF8JOh1t7ykVm5kyzKBpm4lUcsjeG0qOM' } }
					defaultCenter={ { lat: 42.882004, lng: 74.582748 } }
					defaultZoom={ 14 }
				>
					<AnyReactComponent
						lat={ 42.955413 }
						lng={ 74.337844 }
						text="My Marker"
					/>
				</GoogleMapReact>
			</div>
		</main>
	);
};

export default Main;