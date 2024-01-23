import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";

function MakerCars() {
    const [makers, setMakers] = useState([]);
    const [selectedMaker, setSelectedMaker] = useState("");
    const [cars, setCars] = useState(null);

    useEffect(() => {
        fetch('http://localhost:20004/api/makers')
            .then(response => response.json())
            .then(data => {
                setMakers(data);
            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    }, []);

    useEffect(() => {
        if (selectedMaker) {
            fetch(`http://localhost:20004/api/maker?maker=${selectedMaker}`)
                .then(response => response.json())
                .then(data => {
                    setCars(data);
                })
                .catch(error => {
                    console.error('There was an error!', error);
                });
        }
    }, [selectedMaker]);

    return (
        <>
            <h1>Makers</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="makers-select-label">Maker</InputLabel>
                        <Select
                            labelId="makers-select-label"
                            id="demo-simple-select"
                            value={selectedMaker}
                            label="Maker"
                            onChange={(e) => {
                                setSelectedMaker(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {
                                makers.map(maker => <MenuItem key={maker} value={maker}>{maker}</MenuItem>)
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
                                        DOL: {car.DOL}
                                        <ul>
                                            <li>VIN: {car.VIN}</li>
                                            <li>CAFV: {car.cafv_ref}</li>
                                            <li>City: {car.city_ref}</li>
                                            <li>ID: {car.id}</li>
                                            <li>Model: {car.model}</li>
                                            <li>Range: {car.range}</li>
                                            <li>Type: {car.type}</li>
                                            <li>Utility: {car.utility_ref}</li>
                                            <li>Year: {car.year}</li>
                                        </ul>
                                    </li>)
                            }
                        </ul> :
                        selectedMaker ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default MakerCars;


