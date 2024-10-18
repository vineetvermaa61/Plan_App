import Card from './Card';

// tours aur removeTour function bhi as a prop pass kiya hai
// ##3## Recieved prop - removeTour
function Tours({tours, removeTour}){
    return(
        <div className='container'>
            <div>
                <h2 className='title'>Plan With Love</h2>
            </div>
            {/* bahut saare cards banane ke liye kar rahe ye */}
            {/* data.js ke andar array mein jitne bhi elements/size hoga utne cards banenge, har data ke liye ek card */}
            {/* tours waale data ke liye, har ek data ko map kar diya card ke sath */}
            {/* har single tour ke liye card wala component return kar diya */}
            <div className='cards'>
                {

                    tours.map( (tour) =>{
                        {/* Is tarah object likhne ka matlab hai ki poore ke poore tour object ki copy pass kar di, ki isko clone kr do */}
                        {/* card display karne ke liye kuch data rewuire hoga wo data pass kar rahe hain */}
                        {/* ##4## removeTour sent as prop */}
                        return <Card key = {tour.id} {...tour} removeTour = {removeTour}></Card>
                        {/* ek acchi practice ye hoti hai ki jab bhi kisi list ke upar map function chala rahe hain, toh aapko 
                        hamesha wahan ek key pass karni chahiye, aur wo key ek UNIQUE IDENTIFIER honi chahiye, is case mein id ek
                        unique identifier hai toh wo pass kar rahe hain , agar kisi case mein koi U.I. nahi hai toh wahan par index
                        pass kar do, key = {index} , but this is not a good practice to pass index */}
                        {/* #RULE OF THUMB: Jab bhi map function ka use kar rahe hinge aise components ke sath toh unique_id/key  sath
                        mein as a prop bhejenge -oherwise app can't host*/}

                    } )
                }
            </div>

        </div>
    );
}

export default Tours;