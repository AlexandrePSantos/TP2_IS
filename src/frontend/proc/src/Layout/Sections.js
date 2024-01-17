import MakerCars from "../Procedures/MakerCars";
import YearCars from "../Procedures/YearCars";
import ElegibleCars from "../Procedures/ElegibleCars";
import CityCars from "../Procedures/CityCars";

const Sections = [
    {
        id: "maker-cars",
        label: "Cars by maker",
        content: <MakerCars/>
    },

    {
        id: "year-cars",
        label: "Cars by year",
        content: <YearCars/>
    },

    {
        id: "elegible-cars",
        label: "Cars by elegibility",
        content: <ElegibleCars/>
    },

    {
        id: "city-cars",
        label: "Cars by city",
        content: <CityCars/>
    }

];

export default Sections;