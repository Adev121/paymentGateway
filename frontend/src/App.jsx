import { useState } from 'react'
import './App.css'
import axios from "axios"
import swal from "sweetalert"
function App() {
  const [amount,setAmount ] = useState(0)

  const handlepayment=async ()=>{
    try {
      const response = await axios.post("http://localhost:5000/payment",{amount})
      console.log(response.data)
      const options = {
        key : "rzp_test_f8Y5JFvsPLL5sN",
        amount:response.data.amount,
        currency:response.data.currency,
        order_id:response.data.id,
        name:"Abhishek Kr Ram",
        description:"This is a test transaction",
        handler:async (res)=>{
          console.log(res)
          const response = await axios.post("http://localhost:5000/verify",res)
          console.log(response.data)
          if(response.status==200)
          {
            swal(`Payment_Id: ${response.data.message}`,`${res.razorpay_payment_id}`,'success')
          }else
          swal(`${response.data.message}`,`Something went wrong`,'error')
        }
      }

      const rpz = new window.Razorpay(options)
      rpz.open()
    } catch (error) {
      console.log(error)
      swal(`Something went wrong`,`${error.message}`,'error')
    }

  }

  return (
    <>
      <h1>Payment Page</h1>
      <input type="number" style={{fontSize:"25px"}} onChange={(e)=>setAmount(e.target.value)}/>
      {
        amount>0 && (
          <div>
            <button style={{backgroundColor:'blue',margin:"25px"}} onClick={handlepayment}>Pay now</button>
          </div>
        )
      }
    </>
  )
}

export default App
