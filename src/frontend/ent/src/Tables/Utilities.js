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
    const [pagesSize, setPagesSize] = useState(1);

    useEffect(() => {
        setData(null);
        console.log(page);
        fetch(`http://localhost:20001/api/utilities?page=${page}&page_size=${PAGE_SIZE}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(response.statusText);
                }
                return response.json();
            })
            .then(responseData => {
                console.log("%%%%$$$%$%$%#$%#$%#$%#$%#$%# Data before");
                console.log(responseData);
                console.log(responseData[0][0]['data']);
                setData(responseData[0][0]['data']);
                setPagesSize(responseData[0][0]['number_of_records']);
                console.log("%%%%$$$%$%$%#$%#$%#$%#$%#$%# Data after");
            })
            .catch(error => {
                console.error(error);
            });
    }, [page]);

    return (
        <>
            <h1>Utilities</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell align="center">Utilities</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            data ?
                                data.map((row, index) => (
                                    <TableRow key={row.id + '-' + index} style={{background: "gray", color: "black"}} >
                                        <TableCell component="td" align="center">{row.id}</TableCell>
                                        <TableCell component="td" scope="row">
                                                {row.name}
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
                data && <div style={{background: "black", padding: "1rem"}}>
                    <Pagination style={{color: "black"}}
                                variant="outlined" shape="rounded"
                                color={"primary"}
                                onChange={(e, v) => {
                                    setPage(v)
                                }}
                                page={page}
                                count={Math.floor(pagesSize / PAGE_SIZE) } // o -1 é .floor para mais baixo, ceil para maior
                    />
                </div>
            }


        </>
    );
}

export default Utilities;