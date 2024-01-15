import {useEffect, useState} from "react";
import {
    Button,
    CircularProgress,
    Pagination,
    Paper, Stack,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow, TextField
} from "@mui/material";

function Artists() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [data, setData] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(100000);
    const [newArtist, setNewArtist] = useState("");

    useEffect(() => {
        fetch(`http://0.0.0.0:20001/artists/pageCount`)
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

            fetch(`http://0.0.0.0:20001/artists/?page=${page}`)
                .then((response) => {
                    if (response.status === 200) {
                        response.json().then((res) => setData(res));
                    }
                })
                .catch((error) => {
                    console.error("Fetch Error:", error);
                });

    }, [page]);

    const handleAddArtist = async () => {
        const [id, name, company_name] = newArtist.split(",");
        if (id !== "" && name !== "" && company_name !== "") {
            try {
                const response = await fetch('http://0.0.0.0:20001/artist', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id: Number(id), name})
                });

                if (!response.ok) {
                    throw new Error('Failed to create artist');
                }

                setNewArtist("")

            } catch (error) {
                console.error('Error creating artist:', error);
            }
        }
    }

    return (
        <>
            <h1>Artists</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell align="left">Name</TableCell>
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

            <Stack direction="row" sx={{mt: 4}} gap={2}>
            <TextField
                fullWidth
                label="Insert Label, format: (id, name)"
                value={newArtist}
                onChange={(e) => setNewArtist(e.target.value)}

                variant="filled"
                color="primary"
            />
                <Button
                    variant="contained"
                    onClick={() => handleAddArtist()}
                    >
                    Insert!
                        </Button>
            </Stack>

        </>
    );
}

export default Artists;