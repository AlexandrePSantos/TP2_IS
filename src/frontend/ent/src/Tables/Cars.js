import {useEffect, useState} from "react";
import {
    Button,
    CircularProgress,
    Pagination,
    Paper, 
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";

function Cars() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [data, setData] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(100000);

    useEffect(() => {
        fetch('http://localhost:20001/cars/pageCount')
        .then((response) => {
            if (response.status === 200) {
                response.json().then((res) => setMaxDataSize(res));
            }
        }
    )
        .catch((error) => {
            console.error("Fetch Error:", error);
        }
    );
}, []);

    useEffect(() => {
        setData(null);
    
        fetch(`http://localhost:20001/cars/?page=${page}`)
        .then((response) => {
            if (response.status === 200) {
                response.json().then((res) => setData(res));
            }
        })
        .catch((error) => {
            console.error("Fetch Error:", error);
        });

}, [page]);


const removeCar = (id) => {
    fetch(`http://localhost:20001/cars/remove?id=${id}`)
    .then((response) => {
        if (response.status === 200) {
            // Fetch data again after car is removed
            fetch(`http://localhost:20001/cars/?page=${page}`)
            .then((response) => {
                if (response.status === 200) {
                    response.json().then((res) => setData(res));
                }
            })
            .catch((error) => {
                console.error("Fetch Error:", error);
            });
        }
    })
    .catch((error) => {
        console.error("Fetch Error:", error);
    });
}

    return (
        <>
            <h1>Cars</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">Maker</TableCell>
                            <TableCell component="th" width={"1px"} align="center">Model</TableCell>
                            <TableCell component="th" width={"1px"} align="center">Type</TableCell>
                            <TableCell component="th" width={"1px"} align="center">DOL</TableCell>
                            <TableCell component="th" width={"1px"} align="center">VIN</TableCell>
                            <TableCell component="th" width={"1px"} align="center">Year</TableCell>
                            <TableCell component="th" width={"1px"} align="center">Range</TableCell>
                            <TableCell component="th" width={"1px"} align="center"></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            data ?
                                data.map((row) => (
                                    <TableRow key={row.id} style={{background: "gray", color: "black"}} >
                                        <TableCell component="td" scope="row" align="center">{row.maker}</TableCell>
                                        <TableCell component="td" scope="row" align="center">{row.model}</TableCell>
                                        <TableCell component="td" scope="row" align="center">{row.type}</TableCell>
                                        <TableCell component="td" scope="row" align="center">{row.dol}</TableCell>
                                        <TableCell component="td" scope="row" align="center">{row.vin}</TableCell>
                                        <TableCell component="td" scope="row" align="center">{row.year}</TableCell>
                                        <TableCell component="td" scope="row" align="center">{row.range}</TableCell>
                                        <TableCell component="td" scope="row" align="center">
                                            <Button size="small" variant="outlined" onClick={() => removeCar(row.id)}>Remove</Button>
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={3}>
                                        <CircularProgress/>
                                    </TableCell>
                                </TableRow>
                        }
                    </TableBody>
                </Table>
            </TableContainer>
            {
                maxDataSize && <div style={{background: "black", padding: "1rem"}}>
                    <Pagination style={{color: "black"}}
                                variant="outlined" shape="rounded"
                                color={"primary"}
                                onChange={(e, v) => {
                                    setPage(v)
                                }}
                                page={page}
                                count={Math.ceil(maxDataSize / PAGE_SIZE)}
                    />
                </div>
            }
        </>
    );
}

export default Cars;