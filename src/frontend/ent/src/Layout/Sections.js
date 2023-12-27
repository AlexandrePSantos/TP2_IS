// import Players from "../Tables/Players";
// import Cars from "../Tables/Cars"; // Import Cars component
// import Locations from "../Tables/Locations"; // Import Locations component
import CAFV from "../Tables/CAFV"; // Import CAFV component
import Utilities from "../Tables/Utilities"; // Import Utilities component

const Sections = [

    // {
    //     id: "players",
    //     label: "Players",
    //     content: <Players/>
    // },
    // {
    //     id: "cars", 
    //     label: "Cars",
    //     content: <Cars/>
    // },
    // {
    //     id: "locations",
    //     label: "Locations",
    //     content: <Locations/> 
    // },
    {
        id: "cafv", 
        label: "CAFV",
        content: <CAFV/> 
    },
    {
        id: "utilities",
        label: "Utilities",
        content: <Utilities/> 
    }
];

export default Sections;