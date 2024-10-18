import "./App.css";
import { useState } from "react";
import data from './data';
import Tours from "./components/Tours";

function App() {

  const[tours, setTours] = useState(data);

  //  on the basis of id, jis tour ki id match nahi ho rahi wo saare newTours mein ja rahe hain,
  //  aur jis tour ki id match ho rahi wo saare tours mein remove kar rahe
  // ##1## Function made - removeTour
  function removeTour(id){
    const newTours = tours.filter( (tour) => tour.id !== id );
    setTours(newTours);
  }

  // agar koi tours nahi hai toh ek new UI banao, jismein refresh button par click karne par ek function call hogi jismein tours
  // initial data se set ho jayega
  if(tours.length === 0){
    return(
      <div className="refresh">
          <h2>No more tours available</h2>
          <button className="btn-white" onClick={ ()=>setTours(data) }>
          Refresh
          </button>
      </div>
    );
  }

  // tour ke sath-2 removeTour function bhi as a prop pass kiya hai taaki Tours component ke andar call/use kar sakte hain
  return (
    <div className="App">
    {/* ##2## Passed as prop -removeTour */}
      <Tours tours = {tours} removeTour = {removeTour}></Tours>
    </div>
  );
}

export default App;
