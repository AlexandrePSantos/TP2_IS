import React, { useEffect, useState } from 'react';
import { Box, CircularProgress, Container, FormControl, InputLabel, Select, MenuItem } from "@mui/material";

function MakerCars() {
    const [cars, setCars] = useState([]);
    const [makers, setMakers] = useState([]);
    const [selectedMaker, setSelectedMaker] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`${process.env.REACT_APP_API_PROC_URL}/api/makers`)
            .then(response => response.json())
            .then(data => {
                setMakers(data);
                console.log(data);  
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
                setLoading(false);
            });
    }, []);
    
    useEffect(() => {
        if (selectedMaker) {
            setLoading(true);
            fetch(`${process.env.REACT_APP_API_PROC_URL}/api/maker?maker=${selectedMaker}`)
                .then(response => response.json())
                .then(data => {
                    setCars(data);
                    console.log(data);
                    setLoading(false);
                })
                .catch(error => {
                    console.error('Error fetching data: ', error);
                    setLoading(false);
                });
        }
    }, [selectedMaker]);

    if (loading) {
        return <CircularProgress />;
    }

    return (
        <>
            <h1>Maker Cars</h1>
    
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
                <h2>Results <small>(PROC)</small></h2>
                {cars.map(car => (
                    <Box key={car.id}>
                        <h3>{car.model}</h3>
                        <p>Year: {car.year}</p>
                    </Box>
                ))}
            </Container>
        </>
    );
}

export default MakerCars;