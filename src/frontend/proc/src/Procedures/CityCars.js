import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";

function CityCars() {
    const [cities, setCities] = useState([]);
    const [selectedCity, setSelectedCity] = useState("");
    const [cars, setCars] = useState(null);

    useEffect(() => {
        fetch('http://localhost:20004/api/cities')
            .then(response => response.json())
            .then(data => {
                setCities(data);
            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    }, []);

    useEffect(() => {
        if (selectedCity) {
            fetch(`http://localhost:20004/api/city?city=${selectedCity}`)
                .then(response => response.json())
                .then(data => {
                    setCars(data);
                })
                .catch(error => {
                    console.error('There was an error!', error);
                });
        }
    }, [selectedCity]);

    return (
        <>
            <h1>City</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="cities-select-label">City</InputLabel>
                        <Select
                            labelId="cities-select-label"
                            id="demo-simple-select"
                            value={selectedCity}
                            label="Elegible"
                            onChange={(e) => {
                                setSelectedCity(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {
                                cities.map(city => <MenuItem key={city.id} value={city.id}>{city.name}</MenuItem>)
                            }
                        </Select>
                    </FormControl>
                </Box>
            </Container>

            <Container maxWidth="100%" sx={{
                backgroundColor: 'info.dark',
                padding: "2rem",
                marginTop: "2rem",
                borderRadius: "1rem",
                color: "white"
            }}>
                <h2>Results - PROC</h2>
                {
                    cars ?
                        <ul>
                            {
                                cars.map(car => 
                                    <li key={car.id}>
                                        {car.DOL}
                                        <ul>
                                            <li>VIN: {car.VIN}</li>
                                            <li>CAFV: {car.cafv_ref}</li>
                                            <li>ID: {car.id}</li>
                                            <li>Model: {car.model}</li>
                                            <li>Range: {car.range}</li>
                                            <li>Type: {car.type}</li>
                                            <li>Utility Reference: {car.utility_ref}</li>
                                            <li>Year: {car.year}</li>
                                        </ul>
                                    </li>)
                            }
                        </ul> :
                        selectedCity ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default CityCars;
