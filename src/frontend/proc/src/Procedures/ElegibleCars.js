import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";

function ElegibleCars() {
    const [elegibles, setElegibles] = useState([]);
    const [selectedElegible, setSelectedElegible] = useState("");
    const [cars, setCars] = useState(null);

    useEffect(() => {
        fetch('http://localhost:20004/api/elegibles')
            .then(response => response.json())
            .then(data => {
                setElegibles(data);
            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    }, []);

    useEffect(() => {
        if (selectedElegible) {
            fetch(`http://localhost:20004/api/elegible?elegible=${selectedElegible}`)
                .then(response => response.json())
                .then(data => {
                    setCars(data);
                })
                .catch(error => {
                    console.error('There was an error!', error);
                });
        }
    }, [selectedElegible]);

    return (
        <>
            <h1>Elegibility</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="elegibles-select-label">Elegible</InputLabel>
                        <Select
                            labelId="elegibles-select-label"
                            id="demo-simple-select"
                            value={selectedElegible}
                            label="Elegible"
                            onChange={(e) => {
                                setSelectedElegible(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {
                                elegibles.map(elegible => <MenuItem key={elegible.id} value={elegible.id}>{elegible.name}</MenuItem>)
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
                                            <li>City Reference: {car.city_ref}</li>
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
                        selectedElegible ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default ElegibleCars;