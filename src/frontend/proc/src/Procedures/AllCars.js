import {useEffect, useState} from "react";
import {
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";

function AllCars() {
    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [car, setCar] = useState([]);

    /* Updates the data for the current bounds */
    useEffect(() => {
        const url = `http://localhost:20003/api/makers?page=${page}&size=${PAGE_SIZE}`; 

        fetch(url)
            .then(res => res.json())
            .then(data => setCar(data))
            .catch(err => console.log(err))
    }, [page])

    return (
        <>
            <h1>Cars</h1>
            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"300px"} align="center">ID</TableCell>
                            <TableCell>Maker</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>{
                        car.map((row, index) => ( 
                            <TableRow key={row.id + '-' + index} style={{background: "gray", color: "black"}}>
                                <TableCell component="td" align="center">{row.id}</TableCell>
                                <TableCell component="td" scope="row">
                                    {row.name}
                                </TableCell>
                            </TableRow>
                        ))
                    }
                    </TableBody>
                </Table>
            </TableContainer>
            {
                car.length > 0 && <div style={{background: "black", padding: "1rem"}}>
                    <Pagination style={{color: "black"}}
                                variant="outlined" shape="rounded"
                                color={"primary"}
                                onChange={(e, v) => {
                                    setPage(v)
                                }}
                                page={page}
                                count={Math.ceil(car.length / PAGE_SIZE)}
                    />
                </div>
            }
        </>
    );
}

export default AllCars;