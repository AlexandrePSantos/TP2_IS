import Cars from "../Tables/Cars"; // Import Cars component
import CAFV from "../Tables/CAFV"; // Import CAFV component
import Utilities from "../Tables/Utilities"; // Import Utilities component

const Sections = [

    {
        id: "cars",
        label: "Cars",
        content: <Cars/>
    },
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