import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";

function YearCars() {
    const [years, setYears] = useState([]);
    const [selectedYear, setSelectedYear] = useState("");
    const [cars, setCars] = useState(null);

    useEffect(() => {
        fetch('http://localhost:20004/api/years')
            .then(response => response.json())
            .then(data => {
                setYears(data);
            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    }, []);

    useEffect(() => {
        if (selectedYear) {
            fetch(`http://localhost:20004/api/year?year=${selectedYear}`)
                .then(response => response.json())
                .then(data => {
                    setCars(data);
                })
                .catch(error => {
                    console.error('There was an error!', error);
                });
        }
    }, [selectedYear]);

    return (
        <>
            <h1>Year</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="years-select-label">Year</InputLabel>
                        <Select
                            labelId="years-select-label"
                            id="demo-simple-select"
                            value={selectedYear}
                            label="Year"
                            onChange={(e) => {
                                setSelectedYear(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {
                                years.map(year => <MenuItem key={year} value={year}>{year}</MenuItem>)
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
                                        </ul>
                                    </li>)
                            }
                        </ul> :
                        selectedYear ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default YearCars;
