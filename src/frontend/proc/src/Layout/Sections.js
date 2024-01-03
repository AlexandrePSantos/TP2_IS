import TopTeams from "../Procedures/TopTeams";
import MakerCars from "../Procedures/MakerCars";
import YearCars from "../Procedures/YearCars";
import ElegibleCars from "../Procedures/ElegibleCars";
import TypeCars from "../Procedures/TypeCars";
import CityCars from "../Procedures/CityCars";

const Sections = [

    {
        id: "top-teams",
        label: "Top Teams",
        content: <TopTeams/>
    },

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
        id: "type-cars",
        label: "Cars by type",
        content: <TypeCars/>
    },

    {
        id: "city-cars",
        label: "Cars by city",
        content: <CityCars/>
    }

];

export default Sections;