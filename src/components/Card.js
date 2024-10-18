import { useState } from "react";

// removeTour function bhi as a prop recieve hua hai
// ##5## Recieved prop - removeTour
function Card({id, image, info, price, name, removeTour}){

    const[readmore, setReadmore] = useState(false);
    // agar readmore true hai toh description 200 charactors jitna dikha rahe hai, else poora content dikha rahe
    const description = readmore ? info : `${info.substring(0, 200)}...`

    function readmoreHandler(){
        setReadmore(!readmore);
    }

    return(
        <div className="card">
            <img src={image} className="image"></img>
            <div className="tour-info">
                <div className="tour-details">
                    <h4 className="tour-price">₹{price}</h4>
                    <h4 className="tour-name">{name}</h4>
                </div>
                <div className="description">
                    {description}
                    <span className="read-more" onClick={readmoreHandler}>
                        {readmore ? 'Show less' : 'Read more'}
                    </span>
                </div>
            </div>
            
            {/* onclick par removeTour funtion call kar rahe hain, aur uske andar id as parameter pass kar rahe hain */}
            {/* ##5## Function used - removeTour */}
            <button className="btn-red" onClick={ ()=>removeTour(id) }>Not Interested</button>
        </div>
    );
}

export default Card;