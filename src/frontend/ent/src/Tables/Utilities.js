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

function Utilities() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [data, setData] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(100000);

    useEffect(() => {
        fetch('http://localhost:20001/utilities/pageCount')
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
    
        fetch(`http://localhost:20001/utilities/?page=${page}`)
        .then((response) => {
            if (response.status === 200) {
                response.json().then((res) => setData(res));
            }
        })
        .catch((error) => {
            console.error("Fetch Error:", error);
        });

}, [page]);

    return (
        <>
            <h1>Cars</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell component="th" width={"1px"} align="center">Name</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            data ?
                                data.map((row) => (
                                    <TableRow
                                        key={row.id}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" scope="row" align="center">{row.id}</TableCell>
                                        <TableCell component="td" scope="row" align="center">{row.name}</TableCell>
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

export default Utilities;