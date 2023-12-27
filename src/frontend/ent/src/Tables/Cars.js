import {useEffect, useState} from "react";
import {
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
    const [maxDataSize, setMaxDataSize] = useState(0);

    useEffect(() => {
        setData(null);
        fetch(`http://localhost:20001/api/cars`)
        .then(response => response.json())
        .then(data => {
            setData(data);
            setMaxDataSize(data.length);
        })
        .catch(error => console.error('Error:', error));
    }, [page]);

    return (
        <>
            <h1>Cars</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell align="center">Maker</TableCell>
                            <TableCell align="center">Model</TableCell>
                            <TableCell align="center">Type</TableCell>
                            <TableCell align="center">DOL</TableCell>
                            <TableCell align="center">VIN</TableCell>
                            <TableCell align="center">Year</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            data ?
                                data.map((row) => (
                                    <TableRow key={row.id} style={{background: "gray", color: "black"}} >
                                        <TableCell component="th" scope="row">{row.id}</TableCell>
                                        <TableCell align="center">{row.maker}</TableCell>
                                        <TableCell align="center">{row.model}</TableCell>
                                        <TableCell align="center">{row.type}</TableCell>
                                        <TableCell align="center">{row.DOL}</TableCell>
                                        <TableCell align="center">{row.VIN}</TableCell>
                                        <TableCell align="center">{row.year}</TableCell>
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