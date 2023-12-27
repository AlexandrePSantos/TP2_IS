import React, {useEffect, useState} from 'react';
import {LayerGroup, useMap} from 'react-leaflet';
import {ObjectMarker} from "./ObjectMarker";


function ObjectMarkersGroup() {

    const map = useMap();
    const [geom, setGeom] = useState([]);
    const [bounds, setBounds] = useState(map.getBounds());

    /**
     * Setup the event to update the bounds automatically
     */
    useEffect(() => {
        const cb = () => {
            setBounds(map.getBounds());
        }
        map.on('moveend', cb);

        return () => {
            map.off('moveend', cb);
        }
    }, []);

    /* Updates the data for the current bounds */
    useEffect(() => {
        const{_northEast: {lat: neLat, lng: neLng}, _southWest: {lat: swLat, lng: swLng}} = bounds; 
        const url = `http://localhost:20002/api/markers?neLng=${neLng}&neLat=${neLat}&swLng=${swLng}&swLat=${swLat}`; 

        fetch(url)
            .then(res => res.json())
            .then(data => setGeom(data))
            .catch(err => console.log(err))
    }, [bounds])

    return (
        <LayerGroup>
            {
                geom.map(geoJSON => <ObjectMarker key={geoJSON.properties.id} geoJSON={geoJSON}/>)
            }
        </LayerGroup>
    );
}

export default ObjectMarkersGroup;
